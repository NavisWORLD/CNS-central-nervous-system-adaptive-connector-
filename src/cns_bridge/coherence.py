from __future__ import annotations
from collections import Counter
import re
import numpy as np


class CoherenceGate:
    """Small deterministic acceptance gate for backend text."""

    def __init__(self, threshold: float = 0.35):
        self.threshold = float(threshold)

    def score(self, text: str) -> float:
        text = (text or "").strip()
        if not text:
            return 0.0
        words = re.findall(r"[A-Za-z0-9_'-]+", text.lower())
        if not words:
            return 0.05
        unique_ratio = len(set(words)) / len(words)
        counts = Counter(words)
        repeat_penalty = max(counts.values()) / len(words)
        length_score = min(1.0, len(words) / 24.0)
        return float(np.clip(0.50*unique_ratio + 0.35*length_score + 0.15*(1-repeat_penalty), 0.0, 1.0))

    def accepts(self, text: str) -> bool:
        return self.score(text) >= self.threshold
