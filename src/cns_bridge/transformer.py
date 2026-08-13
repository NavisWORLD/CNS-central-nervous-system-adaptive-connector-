from __future__ import annotations
from pathlib import Path
import math
import numpy as np


def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    z = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(z)
    return e / (np.sum(e, axis=axis, keepdims=True) + 1e-12)


def _layer_norm(x: np.ndarray) -> np.ndarray:
    mean = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + 1e-6)


class ReferenceStateTransformer:
    """Deterministic single-block attention mixer over 54 scalar CNS channels.

    This is a public, inspectable reference implementation. It is not presented
    as the private/heavy COSMOS language-model weights. It demonstrates how a
    54-channel CNS state can be mixed with Transformer-style self-attention.
    """

    def __init__(self, state_dim: int = 54, d_model: int = 16, seed: int = 707):
        self.state_dim = int(state_dim)
        self.d_model = int(d_model)
        rng = np.random.default_rng(seed)
        scale = 1.0 / math.sqrt(self.d_model)
        self.input_scale = rng.normal(0, scale, (self.d_model,))
        self.position = rng.normal(0, scale, (self.state_dim, self.d_model))
        self.wq = rng.normal(0, scale, (self.d_model, self.d_model))
        self.wk = rng.normal(0, scale, (self.d_model, self.d_model))
        self.wv = rng.normal(0, scale, (self.d_model, self.d_model))
        self.wo = rng.normal(0, scale, (self.d_model, self.d_model))
        self.readout = rng.normal(0, scale, (self.d_model,))

    def transform(self, state_54d: np.ndarray) -> np.ndarray:
        x = np.asarray(state_54d, dtype=np.float64).reshape(-1)
        if x.size != self.state_dim:
            raise ValueError(f"state_54d must contain {self.state_dim} values")
        tokens = x[:, None] * self.input_scale[None, :] + self.position
        q, k, v = tokens @ self.wq, tokens @ self.wk, tokens @ self.wv
        attention = _softmax((q @ k.T) / math.sqrt(self.d_model), axis=-1)
        mixed = attention @ v
        hidden = _layer_norm(tokens + mixed @ self.wo)
        out = np.tanh(hidden @ self.readout)
        return out.astype(np.float64)

    def save(self, path: str | Path) -> None:
        np.savez_compressed(
            path, input_scale=self.input_scale, position=self.position,
            wq=self.wq, wk=self.wk, wv=self.wv, wo=self.wo, readout=self.readout,
        )

    def load(self, path: str | Path) -> None:
        d = np.load(path)
        for name in ("input_scale", "position", "wq", "wk", "wv", "wo", "readout"):
            setattr(self, name, np.asarray(d[name], dtype=np.float64))
