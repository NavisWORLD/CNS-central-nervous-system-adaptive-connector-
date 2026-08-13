from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import asyncio
import time
import numpy as np

from .backend import CNSBackend, StateSummaryBackend
from .coherence import CoherenceGate
from .context import ContextExpander
from .encoder import CNS12DEncoder, SensorySnapshot
from .entropy import CompositeEntropyBridge
from .memory import VectorMemory
from .models import CNSPacket
from .organs import BrainSurgeon, EmethHarmonizer, SwarmAwareness, SynapticField
from .plasticity import HebbianPlasticity
from .transformer import ReferenceStateTransformer


@dataclass(slots=True)
class CNSResult:
    response: str
    coherence: float
    accepted_native: bool
    packet: CNSPacket
    status: dict[str, Any]


class CNSHarness:
    """Complete public CNS reference harness.

    Pipeline:
      observation -> 12D -> 42D -> 54D adaptive state -> attention mixer ->
      synaptic field -> backend -> coherence gate -> fallback -> memory/plasticity
    """

    def __init__(
        self,
        backend: CNSBackend | None = None,
        fallback_backend: CNSBackend | None = None,
        *,
        seed: int = 707,
        memory_capacity: int = 512,
    ):
        self.encoder = CNS12DEncoder()
        self.context_expander = ContextExpander()
        self.transformer = ReferenceStateTransformer(seed=seed)
        self.memory = VectorMemory(memory_capacity)
        self.plasticity = HebbianPlasticity()
        self.entropy = CompositeEntropyBridge()
        self.field = SynapticField()
        self.harmonizer = EmethHarmonizer()
        self.awareness = SwarmAwareness()
        self.surgeon = BrainSurgeon()
        self.backend = backend or StateSummaryBackend()
        self.fallback_backend = fallback_backend or StateSummaryBackend()
        self.coherence_gate = CoherenceGate()
        self._initialized = False
        self._mark_organs()

    def _mark_organs(self) -> None:
        for name in (
            "synaptic_field", "quantum_bridge", "emeth_harmonizer",
            "swarm_plasticity", "swarm_awareness", "swarm_daemons", "brain_surgeon",
        ):
            self.surgeon.set(name, True, "ready")

    def warmup(self) -> dict[str, Any]:
        self._initialized = True
        return self.status()

    def _adaptive_state(self, x42: np.ndarray, entropy_value: float) -> np.ndarray:
        prior = self.field.current.copy()
        base = np.concatenate([x42, np.zeros(12, dtype=np.float64)])
        memory_hits = self.memory.recall(prior, k=3) if self.field.iteration else []
        memory_strength = sum(max(0.0, float(hit.get("score", 0.0))) for hit in memory_hits) / max(1, len(memory_hits))
        plastic = self.plasticity.modulation(prior) if self.field.iteration else np.zeros(54)
        tail = np.tanh(
            0.35 * prior[:12]
            + 0.35 * plastic[:12]
            + 0.15 * memory_strength
            + 0.15 * (2.0 * entropy_value - 1.0)
        )
        base[42:] = tail
        mixed = self.transformer.transform(base)
        return np.tanh(0.7 * base + 0.3 * mixed)

    async def step(
        self,
        prompt: str,
        sensory: SensorySnapshot | None = None,
        context: dict[str, float] | None = None,
        *,
        reward: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> CNSResult:
        if not self._initialized:
            self.warmup()
        started = time.perf_counter()
        sensory = sensory or SensorySnapshot()
        entropy_sample = self.entropy.sample()
        sensory.entropy = entropy_sample.value
        x12 = self.encoder.encode(sensory)
        ctx = dict(context or {})
        ctx.setdefault("quantum_mix", entropy_sample.value)
        ctx.setdefault("system_entropy", entropy_sample.value)
        ctx.setdefault("loop_iteration", float(self.field.iteration))
        x42 = self.context_expander.expand(x12, ctx)
        x54 = self._adaptive_state(x42, entropy_sample.value)
        recall = self.memory.recall(x54, k=3)
        uncertainty = {
            "state_dispersion": float(np.std(x54)),
            "state_delta": float(np.linalg.norm(x54 - self.field.current)),
        }
        packet = CNSPacket(
            sensory_12d=x12,
            context_42d=x42,
            adaptive_54d=x54,
            uncertainty=uncertainty,
            memory={"recall": recall, "size": len(self.memory)},
            entropy={"value": entropy_sample.value, "source": entropy_sample.source, "live": entropy_sample.live},
            control={"mode": "beast", "iteration": self.field.iteration + 1},
            metadata=dict(metadata or {}),
        )
        self.field.update(x54)
        native = await self.backend.generate(prompt, packet)
        score = self.coherence_gate.score(native)
        accepted = score >= self.coherence_gate.threshold
        response = native if accepted else await self.fallback_backend.generate(prompt, packet)
        if not accepted:
            score = self.coherence_gate.score(response)
        self.plasticity.update(x54, reward=reward)
        self.memory.add(x54, {"prompt": prompt, "response": response, "coherence": score})
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        status = self.status()
        status["last_latency_ms"] = elapsed_ms
        status["state_coherence"] = self.harmonizer.score(x54)
        return CNSResult(response=response, coherence=score, accepted_native=accepted, packet=packet, status=status)

    def run_step(self, *args, **kwargs) -> CNSResult:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.step(*args, **kwargs))
        raise RuntimeError("run_step() cannot be used inside an active event loop; await step() instead")

    def status(self) -> dict[str, Any]:
        return {
            "architecture": "COSMOS/Davis CNS public reference",
            "version": "0.1.0",
            "initialized": self._initialized,
            "state_shape": 54,
            "sensory_shape": 12,
            "context_shape": 42,
            "memory_items": len(self.memory),
            "hebbian_updates": self.plasticity.updates,
            "synaptic_field": self.awareness.snapshot(self.field),
            "organs": self.surgeon.diagnose(),
        }
