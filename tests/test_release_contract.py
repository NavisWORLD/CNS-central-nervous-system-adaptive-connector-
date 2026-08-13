import numpy as np

from cns_bridge import CNSHarness, SensorySnapshot
from cns_bridge.backend import CallableBackend
from cns_bridge.memory import VectorMemory
from cns_bridge.plasticity import HebbianPlasticity


def test_custom_backend_receives_54d_packet():
    seen = {}

    def backend(prompt, packet):
        seen["shape"] = packet.adaptive_54d.shape
        seen["prompt"] = prompt
        return "Custom backend produced a complete deterministic response with sufficient lexical variety for certification."

    h = CNSHarness(backend=CallableBackend(backend, name="cert-backend"))
    result = h.run_step("backend contract", SensorySnapshot(arousal=0.3))
    assert seen == {"shape": (54,), "prompt": "backend contract"}
    assert result.response.startswith("Custom backend")
    assert result.accepted_native is True


def test_external_entropy_source_and_recurrence():
    h = CNSHarness(seed=5)
    h.entropy.add_source("fixed-cert-source", lambda: 0.25)
    r1 = h.run_step("first", SensorySnapshot(audio_rms=0.1))
    r2 = h.run_step("second", SensorySnapshot(audio_rms=0.2))
    assert r1.packet.entropy["source"] == "fixed-cert-source"
    assert r1.packet.entropy["value"] == 0.25
    assert h.field.iteration == 2
    assert len(h.memory) == 2
    assert h.plasticity.updates == 2
    assert not np.allclose(r1.packet.adaptive_54d, r2.packet.adaptive_54d)


def test_memory_round_trip(tmp_path):
    h = CNSHarness(seed=9)
    h.run_step("persist memory", SensorySnapshot(arousal=0.5))
    path = tmp_path / "memory.json"
    h.memory.save(path)
    restored = VectorMemory.load(path)
    assert len(restored) == 1
    hits = restored.recall(h.field.current, k=1)
    assert hits
    assert hits[0]["prompt"] == "persist memory"


def test_plasticity_round_trip(tmp_path):
    p = HebbianPlasticity()
    state = np.linspace(-1.0, 1.0, 54)
    p.update(state, reward=0.75)
    path = tmp_path / "hebbian.npz"
    p.save(path)

    restored = HebbianPlasticity()
    restored.load(path)
    assert restored.updates == 1
    assert np.allclose(restored.weights, p.weights)
