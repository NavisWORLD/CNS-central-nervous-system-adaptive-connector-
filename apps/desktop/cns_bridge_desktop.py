from __future__ import annotations

import argparse
import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from cns_bridge import CNSHarness, SensorySnapshot


APP_TITLE = "CNS Bridge // Adaptive Connector"


def build_snapshot(values: dict[str, str]) -> SensorySnapshot:
    def f(name: str, default: float = 0.0) -> float:
        try:
            return float(values.get(name, default))
        except (TypeError, ValueError):
            return default

    return SensorySnapshot(
        audio_rms=f("audio_rms"),
        dominant_frequency_hz=f("frequency_hz"),
        spectral_flatness=f("spectral_flatness"),
        geometric_phase_rad=f("phase_rad"),
        phase_velocity=f("phase_velocity"),
        av_coherence=f("av_coherence"),
        pleasure=f("pleasure"),
        arousal=f("arousal"),
        dominance=f("dominance"),
        motion_energy=f("motion_energy"),
        luminance=f("luminance", 0.5),
    )


def self_test() -> int:
    harness = CNSHarness(seed=707)
    result = harness.run_step(
        "desktop package self test",
        SensorySnapshot(
            audio_rms=0.2,
            dominant_frequency_hz=220.0,
            arousal=0.4,
            av_coherence=0.8,
        ),
        {"coherence": 0.8},
    )
    payload = {
        "ok": bool(result.response),
        "response": result.response,
        "shapes": {
            "sensory_12d": list(result.packet.sensory_12d.shape),
            "context_42d": list(result.packet.context_42d.shape),
            "adaptive_54d": list(result.packet.adaptive_54d.shape),
        },
        "memory_items": result.status.get("memory_items"),
        "hebbian_updates": result.status.get("hebbian_updates"),
    }
    print(json.dumps(payload, indent=2))
    return 0 if payload["ok"] and payload["shapes"] == {
        "sensory_12d": [12], "context_42d": [42], "adaptive_54d": [54]
    } else 1


class CNSBridgeDesktop(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1000x720")
        self.minsize(860, 620)
        self.configure(bg="#0b1020")
        self.harness = CNSHarness(seed=707)
        self.last_payload: dict | None = None
        self._configure_style()
        self._build_ui()

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#0b1020")
        style.configure("Card.TFrame", background="#11182c")
        style.configure("TLabel", background="#0b1020", foreground="#dbe7ff")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#ffffff")
        style.configure("Muted.TLabel", foreground="#93a4c7")
        style.configure("Card.TLabel", background="#11182c", foreground="#dbe7ff")
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=20)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="CNS BRIDGE", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            root,
            text="Local 12D → 42D → 54D adaptive connector console",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(2, 16))

        body = ttk.Frame(root)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        left = ttk.Frame(body, style="Card.TFrame", padding=16)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        right = ttk.Frame(body, style="Card.TFrame", padding=16)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ttk.Label(left, text="Prompt", style="Card.TLabel").pack(anchor="w")
        self.prompt = tk.Text(
            left,
            height=6,
            wrap="word",
            bg="#0d1426",
            fg="#eef4ff",
            insertbackground="#ffffff",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.prompt.insert("1.0", "Choose the next action.")
        self.prompt.pack(fill="x", pady=(6, 14))

        self.entries: dict[str, tk.StringVar] = {}
        fields = [
            ("audio_rms", "Audio RMS (0–1)", "0.20"),
            ("frequency_hz", "Dominant frequency Hz", "220"),
            ("spectral_flatness", "Spectral flatness (0–1)", "0.25"),
            ("phase_rad", "Geometric phase radians", "0.0"),
            ("phase_velocity", "Phase velocity", "0.0"),
            ("av_coherence", "A/V coherence (0–1)", "0.80"),
            ("pleasure", "Pleasure (-1–1)", "0.0"),
            ("arousal", "Arousal (0–1)", "0.40"),
            ("dominance", "Dominance (0–1)", "0.50"),
            ("motion_energy", "Motion energy (0–1)", "0.20"),
            ("luminance", "Luminance (0–1)", "0.50"),
        ]
        grid = ttk.Frame(left, style="Card.TFrame")
        grid.pack(fill="x")
        for i, (key, label, default) in enumerate(fields):
            row, col = divmod(i, 2)
            box = ttk.Frame(grid, style="Card.TFrame")
            box.grid(row=row, column=col, sticky="ew", padx=(0, 8) if col == 0 else (8, 0), pady=4)
            grid.columnconfigure(col, weight=1)
            ttk.Label(box, text=label, style="Card.TLabel").pack(anchor="w")
            var = tk.StringVar(value=default)
            self.entries[key] = var
            ttk.Entry(box, textvariable=var).pack(fill="x", pady=(3, 0))

        actions = ttk.Frame(left, style="Card.TFrame")
        actions.pack(fill="x", pady=(16, 0))
        self.run_button = ttk.Button(actions, text="Run CNS Cycle", command=self.run_cycle, style="Accent.TButton")
        self.run_button.pack(side="left")
        ttk.Button(actions, text="Copy JSON", command=self.copy_json).pack(side="left", padx=8)

        self.status_label = ttk.Label(right, text="Ready", style="Card.TLabel")
        self.status_label.pack(anchor="w")
        self.dim_label = ttk.Label(right, text="12D  •  42D  •  54D", style="Card.TLabel")
        self.dim_label.pack(anchor="w", pady=(4, 14))

        ttk.Label(right, text="Response", style="Card.TLabel").pack(anchor="w")
        self.output = tk.Text(
            right,
            height=11,
            wrap="word",
            bg="#0d1426",
            fg="#eef4ff",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.output.pack(fill="both", expand=False, pady=(6, 14))

        ttk.Label(right, text="State / telemetry", style="Card.TLabel").pack(anchor="w")
        self.telemetry = tk.Text(
            right,
            wrap="none",
            bg="#0d1426",
            fg="#b7d0ff",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.telemetry.pack(fill="both", expand=True, pady=(6, 0))

    def _values(self) -> dict[str, str]:
        return {k: v.get() for k, v in self.entries.items()}

    def run_cycle(self) -> None:
        prompt = self.prompt.get("1.0", "end").strip()
        if not prompt:
            messagebox.showwarning(APP_TITLE, "Enter a prompt first.")
            return
        self.run_button.configure(state="disabled")
        self.status_label.configure(text="Running local CNS cycle…")
        snapshot = build_snapshot(self._values())
        context = {"coherence": snapshot.av_coherence}
        threading.Thread(target=self._worker, args=(prompt, snapshot, context), daemon=True).start()

    def _worker(self, prompt: str, snapshot: SensorySnapshot, context: dict[str, float]) -> None:
        try:
            result = self.harness.run_step(prompt, snapshot, context)
            payload = {
                "response": result.response,
                "coherence": result.coherence,
                "accepted_native": result.accepted_native,
                "status": result.status,
                "entropy": result.packet.entropy,
                "uncertainty": result.packet.uncertainty,
                "vectors": {
                    "12d": result.packet.sensory_12d.tolist(),
                    "42d": result.packet.context_42d.tolist(),
                    "54d": result.packet.adaptive_54d.tolist(),
                },
            }
            self.after(0, self._show_result, payload)
        except Exception as exc:  # pragma: no cover - UI guard
            self.after(0, self._show_error, exc)

    def _show_result(self, payload: dict) -> None:
        self.last_payload = payload
        self.output.delete("1.0", "end")
        self.output.insert("1.0", payload["response"])
        self.telemetry.delete("1.0", "end")
        summary = {
            "coherence": payload["coherence"],
            "accepted_native": payload["accepted_native"],
            "memory_items": payload["status"].get("memory_items"),
            "hebbian_updates": payload["status"].get("hebbian_updates"),
            "entropy": payload["entropy"],
            "uncertainty": payload["uncertainty"],
            "shape_12d": len(payload["vectors"]["12d"]),
            "shape_42d": len(payload["vectors"]["42d"]),
            "shape_54d": len(payload["vectors"]["54d"]),
        }
        self.telemetry.insert("1.0", json.dumps(summary, indent=2))
        self.status_label.configure(text="Cycle complete")
        self.run_button.configure(state="normal")

    def _show_error(self, exc: Exception) -> None:
        self.run_button.configure(state="normal")
        self.status_label.configure(text="Error")
        messagebox.showerror(APP_TITLE, str(exc))

    def copy_json(self) -> None:
        if not self.last_payload:
            return
        self.clipboard_clear()
        self.clipboard_append(json.dumps(self.last_payload, indent=2))
        self.status_label.configure(text="JSON copied")


def main() -> int:
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument("--self-test", action="store_true", help="run a headless packaged-runtime smoke test")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    app = CNSBridgeDesktop()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
