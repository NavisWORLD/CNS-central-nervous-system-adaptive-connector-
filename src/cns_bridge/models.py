from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import time
import numpy as np


def _vector(values: Any, size: int, name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64).reshape(-1)
    if arr.size != size:
        raise ValueError(f"{name} must contain exactly {size} values; got {arr.size}")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains non-finite values")
    return arr


@dataclass(slots=True)
class CNSPacket:
    """Portable state packet passed between CNS organs and backends."""

    sensory_12d: np.ndarray
    context_42d: np.ndarray
    adaptive_54d: np.ndarray
    uncertainty: dict[str, float] = field(default_factory=dict)
    memory: dict[str, Any] = field(default_factory=dict)
    entropy: dict[str, Any] = field(default_factory=dict)
    control: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        self.sensory_12d = _vector(self.sensory_12d, 12, "sensory_12d")
        self.context_42d = _vector(self.context_42d, 42, "context_42d")
        self.adaptive_54d = _vector(self.adaptive_54d, 54, "adaptive_54d")

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "sensory_12d": self.sensory_12d.tolist(),
            "context_42d": self.context_42d.tolist(),
            "adaptive_54d": self.adaptive_54d.tolist(),
            "uncertainty": self.uncertainty,
            "memory": self.memory,
            "entropy": self.entropy,
            "control": self.control,
            "metadata": self.metadata,
        }
