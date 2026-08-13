from __future__ import annotations
import math
import numpy as np


def finite(value: float, default: float = 0.0) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return default
    return x if math.isfinite(x) else default


def unit(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clamp a scalar to [0, 1] after min/max normalization."""
    x = finite(value)
    if high <= low:
        raise ValueError("high must be greater than low")
    return float(np.clip((x - low) / (high - low), 0.0, 1.0))


def signed(value: float, scale: float = 1.0) -> float:
    """Map an unbounded scalar to (-1, 1) with tanh."""
    if scale <= 0:
        raise ValueError("scale must be positive")
    return float(np.tanh(finite(value) / scale))


def normalize_vector(values: np.ndarray, clip: float = 4.0) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        return arr.copy()
    mean = float(np.mean(arr))
    std = float(np.std(arr))
    if std < 1e-9:
        return np.zeros_like(arr)
    return np.clip((arr - mean) / std, -clip, clip) / clip
