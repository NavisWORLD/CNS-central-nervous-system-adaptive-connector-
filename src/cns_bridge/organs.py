from __future__ import annotations
from dataclasses import dataclass, asdict
import numpy as np


@dataclass(slots=True)
class OrganStatus:
    name: str
    online: bool = True
    detail: str = "ready"


class SynapticField:
    def __init__(self):
        self.current = np.zeros(54, dtype=np.float64)
        self.previous = np.zeros(54, dtype=np.float64)
        self.iteration = 0

    def update(self, state: np.ndarray) -> None:
        x = np.asarray(state, dtype=np.float64).reshape(-1)
        if x.size != 54:
            raise ValueError("synaptic field expects 54 values")
        self.previous[:] = self.current
        self.current[:] = x
        self.iteration += 1

    def delta(self) -> float:
        return float(np.linalg.norm(self.current - self.previous))


class EmethHarmonizer:
    """Reference state coherence metric; the name preserves COSMOS architecture lineage."""
    def score(self, state: np.ndarray) -> float:
        x = np.asarray(state, dtype=np.float64)
        spread = float(np.std(x))
        return float(np.clip(1.0 - spread / 2.0, 0.0, 1.0))


class SwarmAwareness:
    def snapshot(self, field: SynapticField) -> dict:
        return {"iteration": field.iteration, "state_norm": float(np.linalg.norm(field.current)), "delta": field.delta()}


class BrainSurgeon:
    """Health/failover registry. It never rewrites code silently."""
    def __init__(self):
        self.statuses: dict[str, OrganStatus] = {}

    def set(self, name: str, online: bool, detail: str = "ready") -> None:
        self.statuses[name] = OrganStatus(name, bool(online), str(detail))

    def diagnose(self) -> dict:
        return {name: asdict(status) for name, status in self.statuses.items()}
