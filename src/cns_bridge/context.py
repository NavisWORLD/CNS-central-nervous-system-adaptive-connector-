from __future__ import annotations
from collections.abc import Mapping
import numpy as np
from .normalization import signed


class ContextExpander:
    """Expand 12 sensory channels to a stable 42-channel context vector."""

    CONTEXT_CHANNELS = (
        "system_load", "memory_pressure", "network_activity", "tool_activity",
        "task_complexity", "novelty", "uncertainty", "coherence", "goal_pressure",
        "recent_reward", "error_rate", "latency", "environment_motion", "environment_light",
        "environment_noise", "user_turn_rate", "history_depth", "retrieval_strength",
        "worker_count", "worker_disagreement", "quantum_mix", "system_entropy",
        "session_age", "loop_iteration", "safety_pressure", "fallback_pressure",
        "creativity_bias", "precision_bias", "exploration_bias", "reserved",
    )

    def expand(self, sensory_12d: np.ndarray, context: Mapping[str, float] | None = None) -> np.ndarray:
        x = np.asarray(sensory_12d, dtype=np.float64).reshape(-1)
        if x.size != 12:
            raise ValueError("sensory_12d must contain 12 values")
        context = context or {}
        extra = np.asarray([signed(context.get(name, 0.0), 1.0) for name in self.CONTEXT_CHANNELS])
        return np.concatenate([x, extra])
