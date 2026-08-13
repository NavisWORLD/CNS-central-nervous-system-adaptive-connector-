from cns_bridge import CNSHarness, SensorySnapshot

harness = CNSHarness()

snapshot = SensorySnapshot(
    audio_rms=0.18,
    dominant_frequency_hz=196.0,
    spectral_flatness=0.24,
    av_coherence=0.72,
    pleasure=0.1,
    arousal=0.42,
    dominance=0.55,
    luminance=0.6,
)

result = harness.run_step(
    "Choose the next control action.",
    snapshot,
    context={"task_complexity": 0.6, "precision_bias": 0.8},
)

print(result.response)
print(result.packet.adaptive_54d.shape)
print(result.status)
