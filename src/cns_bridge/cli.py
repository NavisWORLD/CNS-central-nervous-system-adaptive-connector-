from __future__ import annotations
import argparse
import json
from .encoder import SensorySnapshot
from .engine import CNSHarness


def _demo(args: argparse.Namespace) -> int:
    harness = CNSHarness(seed=args.seed)
    sample = SensorySnapshot(
        audio_rms=0.22,
        dominant_frequency_hz=220.0,
        spectral_flatness=0.18,
        geometric_phase_rad=0.4,
        phase_velocity=0.2,
        av_coherence=0.78,
        pleasure=0.2,
        arousal=0.55,
        dominance=0.6,
        motion_energy=0.12,
        luminance=0.65,
    )
    result = harness.run_step(args.prompt, sample, {"task_complexity": 0.4, "coherence": 0.8})
    if args.json:
        print(json.dumps({"response": result.response, "coherence": result.coherence, "status": result.status}, indent=2))
    else:
        print(result.response)
        print(f"coherence={result.coherence:.3f} state_norm={result.status['synaptic_field']['state_norm']:.3f}")
    return 0


def _status(_: argparse.Namespace) -> int:
    print(json.dumps(CNSHarness().warmup(), indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="cns-bridge", description="COSMOS/Davis CNS adaptive connector reference harness")
    sub = parser.add_subparsers(required=True)
    demo = sub.add_parser("demo", help="run one complete CNS cycle")
    demo.add_argument("--prompt", default="Explain the current state.")
    demo.add_argument("--seed", type=int, default=707)
    demo.add_argument("--json", action="store_true")
    demo.set_defaults(func=_demo)
    status = sub.add_parser("status", help="print organ and state status")
    status.set_defaults(func=_status)
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
