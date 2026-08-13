from __future__ import annotations
from collections import deque
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any
import numpy as np


@dataclass(slots=True)
class MemoryItem:
    vector: np.ndarray
    payload: dict[str, Any]


class VectorMemory:
    """Small local cosine-similarity memory used by the reference harness."""

    def __init__(self, capacity: int = 512):
        self.capacity = int(capacity)
        self._items: deque[MemoryItem] = deque(maxlen=self.capacity)

    def __len__(self) -> int:
        return len(self._items)

    def add(self, vector: np.ndarray, payload: dict[str, Any] | None = None) -> None:
        v = np.asarray(vector, dtype=np.float64).reshape(-1)
        self._items.append(MemoryItem(v.copy(), dict(payload or {})))

    def recall(self, query: np.ndarray, k: int = 3) -> list[dict[str, Any]]:
        if not self._items:
            return []
        q = np.asarray(query, dtype=np.float64).reshape(-1)
        qn = np.linalg.norm(q) + 1e-12
        scored = []
        for item in self._items:
            if item.vector.size != q.size:
                continue
            score = float(np.dot(q, item.vector) / (qn * (np.linalg.norm(item.vector) + 1e-12)))
            scored.append((score, item))
        scored.sort(key=lambda t: t[0], reverse=True)
        return [{"score": s, **item.payload} for s, item in scored[: max(0, int(k))]]

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [{"vector": i.vector.tolist(), "payload": i.payload} for i in self._items]
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path, capacity: int = 512) -> "VectorMemory":
        mem = cls(capacity)
        p = Path(path)
        if not p.exists():
            return mem
        for raw in json.loads(p.read_text(encoding="utf-8")):
            mem.add(np.asarray(raw["vector"], dtype=np.float64), raw.get("payload") or {})
        return mem
