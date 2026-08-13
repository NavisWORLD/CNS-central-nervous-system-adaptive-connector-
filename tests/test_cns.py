import numpy as np
from cns_bridge import CNSHarness, CNS12DEncoder, SensorySnapshot, ReferenceStateTransformer


def test_encoder_shape_and_bounds():
    x = CNS12DEncoder().encode(SensorySnapshot(audio_rms=0.5, dominant_frequency_hz=440, entropy=0.7))
    assert x.shape == (12,)
    assert np.all(np.isfinite(x))
    assert np.max(np.abs(x)) <= 1.0 + 1e-9


def test_reference_transformer_shape():
    t = ReferenceStateTransformer(seed=1)
    y = t.transform(np.linspace(-1, 1, 54))
    assert y.shape == (54,)
    assert np.all(np.isfinite(y))


def test_full_harness_cycle_updates_memory_and_plasticity():
    h = CNSHarness(seed=1)
    r = h.run_step("hello", SensorySnapshot(arousal=0.4), {"coherence": 0.7})
    assert r.packet.sensory_12d.shape == (12,)
    assert r.packet.context_42d.shape == (42,)
    assert r.packet.adaptive_54d.shape == (54,)
    assert h.plasticity.updates == 1
    assert len(h.memory) == 1
    assert r.response


def test_fail_soft_entropy_source():
    h = CNSHarness()
    h.entropy.add_source("broken", lambda: (_ for _ in ()).throw(RuntimeError("nope")))
    r = h.run_step("test")
    assert 0 <= r.packet.entropy["value"] <= 1
    assert r.packet.entropy["source"] == "system_entropy"
