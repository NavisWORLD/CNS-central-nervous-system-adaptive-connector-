from __future__ import annotations
from pathlib import Path
import numpy as np


class HebbianPlasticity:
    """Bounded, decayed Hebbian association matrix for 54D CNS state."""

    def __init__(self, size: int = 54, learning_rate: float = 0.002, decay: float = 0.001, clamp: float = 1.0):
        self.size = int(size)
        self.learning_rate = float(learning_rate)
        self.decay = float(decay)
        self.clamp = float(clamp)
        self.weights = np.zeros((self.size, self.size), dtype=np.float64)
        self.updates = 0

    def modulation(self, state: np.ndarray) -> np.ndarray:
        x = np.asarray(state, dtype=np.float64).reshape(-1)
        if x.size != self.size:
            raise ValueError(f"state must contain {self.size} values")
        return np.tanh(self.weights @ x)

    def update(self, state: np.ndarray, reward: float = 1.0) -> None:
        x = np.asarray(state, dtype=np.float64).reshape(-1)
        if x.size != self.size:
            raise ValueError(f"state must contain {self.size} values")
        r = float(np.clip(reward, -1.0, 1.0))
        self.weights *= (1.0 - self.decay)
        self.weights += self.learning_rate * r * np.outer(x, x)
        np.fill_diagonal(self.weights, 0.0)
        np.clip(self.weights, -self.clamp, self.clamp, out=self.weights)
        self.updates += 1

    def save(self, path: str | Path) -> None:
        np.savez_compressed(path, weights=self.weights, updates=np.asarray([self.updates]))

    def load(self, path: str | Path) -> None:
        data = np.load(path)
        w = np.asarray(data["weights"], dtype=np.float64)
        if w.shape != (self.size, self.size):
            raise ValueError("weight file has incompatible shape")
        self.weights[:] = w
        self.updates = int(np.asarray(data.get("updates", [0])).reshape(-1)[0])
