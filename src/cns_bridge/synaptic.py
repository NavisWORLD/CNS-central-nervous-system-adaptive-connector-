from __future__ import annotations
import numpy as np
from .encoder import CNS12DEncoder, SensorySnapshot
from .normalization import finite, unit

SENSORY_DIM = 12
CONTEXT_DIM = 42
STATE_DIM = 54

def encode_12d(snapshot: SensorySnapshot) -> np.ndarray:
    return CNS12DEncoder().encode(snapshot)

def expand_42d(sensory_12d, context_values=None) -> np.ndarray:
    x = np.asarray(sensory_12d, dtype=np.float64).reshape(-1)
    if x.size != SENSORY_DIM:
        raise ValueError("sensory_12d must contain 12 values")
    c = np.zeros(30, dtype=np.float64) if context_values is None else np.asarray(context_values, dtype=np.float64).reshape(-1)
    if c.size != 30:
        raise ValueError("context_values must contain 30 values")
    c = np.tanh(np.where(np.isfinite(c), c, 0.0))
    return np.concatenate([x, c])

def hebbian_modulation(weights, state) -> np.ndarray:
    w = np.asarray(weights, dtype=np.float64)
    x = np.asarray(state, dtype=np.float64).reshape(-1)
    if w.shape != (STATE_DIM, STATE_DIM) or x.size != STATE_DIM:
        raise ValueError("expected a 54x54 weight matrix and 54D state")
    return np.tanh(w @ x)

def hebbian_update(weights, state, reward=1.0, learning_rate=0.002, decay=0.001, clamp=1.0) -> np.ndarray:
    w = np.asarray(weights, dtype=np.float64).copy()
    x = np.asarray(state, dtype=np.float64).reshape(-1)
    if w.shape != (STATE_DIM, STATE_DIM) or x.size != STATE_DIM:
        raise ValueError("expected a 54x54 weight matrix and 54D state")
    if clamp <= 0 or learning_rate < 0 or not 0 <= decay < 1:
        raise ValueError("invalid Hebbian parameters")
    r = float(np.clip(float(reward), -1.0, 1.0))
    w *= 1.0 - float(decay)
    w += float(learning_rate) * r * np.outer(x, x)
    np.fill_diagonal(w, 0.0)
    np.clip(w, -float(clamp), float(clamp), out=w)
    return w

def adaptive_tail(prior_state, plastic_modulation, memory_strength, entropy) -> np.ndarray:
    p = np.asarray(prior_state, dtype=np.float64).reshape(-1)
    m = np.asarray(plastic_modulation, dtype=np.float64).reshape(-1)
    if p.size != STATE_DIM or m.size != STATE_DIM:
        raise ValueError("prior_state and plastic_modulation must contain 54 values")
    q = unit(entropy, 0.0, 1.0)
    s = max(0.0, finite(memory_strength))
    return np.tanh(0.35*p[:12] + 0.35*m[:12] + 0.15*s + 0.15*(2.0*q-1.0))

def assemble_54d(context_42d, tail_12d) -> np.ndarray:
    c = np.asarray(context_42d, dtype=np.float64).reshape(-1)
    t = np.asarray(tail_12d, dtype=np.float64).reshape(-1)
    if c.size != CONTEXT_DIM or t.size != 12:
        raise ValueError("expected 42D context and 12D tail")
    return np.concatenate([c, t])

def blend_54d(base_54d, mixed_54d) -> np.ndarray:
    b = np.asarray(base_54d, dtype=np.float64).reshape(-1)
    m = np.asarray(mixed_54d, dtype=np.float64).reshape(-1)
    if b.size != STATE_DIM or m.size != STATE_DIM:
        raise ValueError("base_54d and mixed_54d must contain 54 values")
    return np.tanh(0.7*b + 0.3*m)
