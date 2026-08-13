# CNS Adaptive Connector Engineering Manual

## 1. Purpose

This manual describes how to deploy the public CNS harness as a reusable subsystem inside another project.

The core engineering pattern is:

```text
Sense -> Normalize -> Encode -> Contextualize -> Adapt -> Transform -> Decide -> Gate -> Act -> Learn
```

## 2. Runtime requirements

- Python 3.10+
- NumPy 1.24+
- no cloud account required
- no GPU required for the reference implementation

Development tools are optional and include pytest, build, and ruff.

## 3. Installation modes

Editable development install:

```bash
pip install -e .[dev]
```

Local production install:

```bash
pip install .
```

Wheel build:

```bash
python -m build
pip install dist/*.whl
```

## 4. Harness lifecycle

```python
cns = CNSHarness()
cns.warmup()
result = cns.run_step(prompt, sensory, context)
status = cns.status()
```

`warmup()` initializes the public organ registry. `step()` is async; `run_step()` is a convenience wrapper for synchronous programs.

## 5. Feeding sensors

The library expects **summaries**, not raw streams. For example:

```python
SensorySnapshot(
    audio_rms=0.2,
    dominant_frequency_hz=210,
    spectral_flatness=0.3,
    motion_energy=0.1,
    luminance=0.7,
)
```

A camera adapter might calculate luminance and motion locally, then discard the frame. An audio adapter might calculate RMS/frequency features, then discard the PCM buffer.

## 6. Context channels

`ContextExpander` has 30 named context channels. Unknown/missing values default to zero. Values are bounded with `tanh`, so callers should generally use human-scale values around `[-3, 3]` rather than huge magnitudes.

## 7. Memory

Default memory is in-process and bounded. Persist it explicitly:

```python
cns.memory.save("memory.json")
```

Restore:

```python
from cns_bridge.memory import VectorMemory
cns.memory = VectorMemory.load("memory.json")
```

Do not save sensitive payloads unless your application has a retention policy.

## 8. Plasticity

Save Hebbian weights:

```python
cns.plasticity.save("hebbian.npz")
```

Restore:

```python
cns.plasticity.load("hebbian.npz")
```

The matrix is 54×54 and can be audited directly.

## 9. External entropy / quantum adapter

```python
def my_qrng():
    return 0.7342  # must be convertible to [0, 1]

cns.entropy.add_source("my-qrng", my_qrng)
```

If the source raises an exception or returns `None`, the harness tries the next source. If none succeeds, it falls back to OS cryptographic entropy.

For a remote service, keep network calls outside the real-time critical path or cache/refill a local buffer. Sensor/decision loops should not freeze because a remote entropy source is slow.

## 10. Custom backend

Use `CallableBackend` or implement `CNSBackend`:

```python
class RobotPolicy:
    async def generate(self, prompt, packet):
        x = packet.adaptive_54d
        return "TURN_LEFT" if x[0] > 0 else "TURN_RIGHT"
```

A string is used in the reference protocol because it works for language and command examples. Industrial applications may wrap structured JSON and validate it before actuation.

## 11. Coherence gate

The bundled gate rejects empty or highly degenerate text. Replace it for serious applications.

A robot should use physical/safety constraints. A financial system should validate schemas and risk limits. A medical system requires domain-specific validated software and regulatory controls; this reference library is not a medical device.

## 12. Failover

Recommended backend chain:

```text
native policy/model
   ↓ failure / gate reject
local fallback
   ↓ failure
safe deterministic state
```

Never make “try another model” the final safety layer for physical actuation.

## 13. Threading and async

Inside an async server:

```python
result = await cns.step(...)
```

Do not call `run_step()` from an active event loop.

## 14. Telemetry

At minimum log:

- UTC timestamp
- library version
- state schema version
- 12D/42D/54D shapes
- entropy source
- memory hit count
- Hebbian update count
- backend name
- coherence/gate result
- latency
- action/result category

Avoid logging raw sensitive sensor data by default.

## 15. Production hardening

Before production use:

1. replace demo coherence with domain validation;
2. version every state schema;
3. cap persistent storage;
4. add structured logs and metrics;
5. add deterministic replay tests;
6. checksum model/transformer weights;
7. define fail-safe output;
8. isolate external network adapters;
9. add authentication/authorization around control endpoints;
10. test sensor dropout and corrupted packets;
11. validate numerical bounds;
12. document every learned/persistent state file.

## 16. Reproducibility

A run should be reconstructable from:

```text
code commit
package version
configuration
transformer seed/checkpoint
initial Hebbian weights
memory snapshot or hash
input/replay sequence
entropy trace or deterministic seed
backend/version
```

## 17. Security principle

The CNS may influence downstream actions. Treat every adapter and backend as untrusted until validated. Do not deserialize arbitrary pickle files, execute generated code automatically, or let model output bypass an action policy.
