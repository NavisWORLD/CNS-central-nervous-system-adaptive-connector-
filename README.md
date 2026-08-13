# CNS Central Nervous System Adaptive Connector

An open, installable reference implementation of the **COSMOS / Davis CNS adaptive connector architecture**.

The library turns heterogeneous observations into a bounded recurrent control state, expands that state through a **12D → 42D → 54D** pipeline, mixes the resulting state with a transparent Transformer-style attention block, passes the state to any model/agent/robot backend, gates the output for basic coherence, and feeds the outcome back into memory and bounded Hebbian plasticity.

> **Scientific boundary:** in this project, “12D/42D/54D” means numerical state channels. It is not a claim that software is operating in literal extra spatial dimensions. Quantum/QRNG sources are optional entropy/control inputs; they do not replace the model or perform language inference.

## Distribution

The public project now includes reproducible desktop, mobile, and binary release packaging:

- ✅ **One-click Windows `.exe` installer** — generated with PyInstaller + Inno Setup and smoke-tested after installation on a clean Windows runner.
- ✅ **macOS `.dmg` / `.app` installer** — the app is built, placed in a DMG, the DMG is mounted in CI, and the packaged CNS self-test is executed from the mounted image.
- ✅ **Polished iPhone / Android companion application** — Flutter mobile UI with a local 12D → 42D → 54D recurrent state engine, mobile contract tests, Android emulator launch verification, and iPhone simulator launch verification.
- ✅ **Packaged GitHub Release with binaries** — the release workflow publishes Windows, macOS, Android, iOS, the certified Python wheel, release notes, and SHA-256 checksums after all platform jobs pass on `main`.

See [`docs/APPS_AND_INSTALLERS.md`](docs/APPS_AND_INSTALLERS.md) for artifact names and verification details.

> **Apple distribution note:** an iPhone simulator app and unsigned physical-device app bundle can be built and published automatically. Installation on a physical iPhone, TestFlight distribution, App Store distribution, and Apple notarization require an Apple Developer signing identity supplied by the distributor. The project does not embed private signing credentials.

## Why this exists

Most AI applications are organized as `prompt -> model -> answer`. The CNS harness is organized as a recurrent system:

```text
observation
   ↓
12D sensory state
   ↓
42D contextual state
   ↓
54D adaptive state
   ↓
state transformer / synaptic field
   ↓
backend / agent / policy
   ↓
coherence + failover
   ↓
action / response
   ↓
memory + Hebbian update
   └──────────────→ next cycle
```

The **model is one organ of the system, not the whole system**.

## Install

### Python

```bash
python -m pip install .
```

For development:

```bash
python -m pip install -e .[dev]
pytest -q
```

Build a downloadable wheel and source package:

```bash
python -m build
```

Artifacts will appear in `dist/`.

### Desktop and mobile

Use the packaged artifacts attached to the GitHub Release for normal end-user installation. The repository also contains the complete reproducible build definitions for Windows, macOS, Android, and iOS.

## 30-second demo

```bash
cns-bridge demo --prompt "Choose the next action." --json
```

Or in Python:

```python
from cns_bridge import CNSHarness, SensorySnapshot

cns = CNSHarness()

result = cns.run_step(
    "Choose the next control action.",
    SensorySnapshot(
        audio_rms=0.18,
        dominant_frequency_hz=220.0,
        spectral_flatness=0.2,
        av_coherence=0.75,
        arousal=0.45,
        luminance=0.6,
    ),
    context={
        "task_complexity": 0.6,
        "precision_bias": 0.8,
    },
)

print(result.response)
print(result.packet.sensory_12d.shape)   # (12,)
print(result.packet.context_42d.shape)   # (42,)
print(result.packet.adaptive_54d.shape)  # (54,)
```

## Connect any model or agent

```python
from cns_bridge import CNSHarness
from cns_bridge.backend import CallableBackend

async def my_backend(prompt, packet):
    # packet.adaptive_54d is the current CNS state.
    # Call your local model, cloud model, robot policy, planner, or tool router here.
    return f"received {prompt!r}; state_norm={float((packet.adaptive_54d**2).sum()**0.5):.3f}"

cns = CNSHarness(backend=CallableBackend(my_backend, name="my-backend"))
```

No vendor is required. A backend can be an LLM, a deterministic controller, a simulation, an industrial decision system, a robot policy, or a multi-agent orchestrator.

## Public state contract

Each completed cycle produces a `CNSPacket` containing:

- `sensory_12d`: normalized 12-channel observation
- `context_42d`: observation plus 30 context/control channels
- `adaptive_54d`: context plus 12 recurrent/adaptive channels, then attention-mixed
- `uncertainty`: simple state dispersion and transition diagnostics
- `memory`: retrieval metadata
- `entropy`: active entropy/control source
- `control`: loop mode and iteration
- `metadata`: application-defined annotations

## The seven CNS organs

The public harness preserves the modular organ map used by the COSMOS architecture:

1. **Synaptic Field** — current and previous 54D shared state
2. **Quantum Bridge** — optional entropy/control source with fail-soft system entropy fallback
3. **Emeth Harmonizer** — reference state-coherence metric
4. **Swarm Plasticity** — bounded Hebbian association matrix
5. **Swarm Awareness** — state norm/delta/iteration observer
6. **Swarm Daemons** — extension point for workers/agents
7. **Brain Surgeon** — health/failover registry; never silently rewrites code

## What is included

```text
src/cns_bridge/
  backend.py          pluggable model/agent interface
  cli.py              command line harness
  coherence.py        deterministic response acceptance gate
  context.py          12D -> 42D expansion
  encoder.py          compact 12D multimodal encoder
  engine.py           complete recurrent CNS cycle
  entropy.py          external entropy + system fallback
  memory.py           local cosine-similarity memory
  models.py           stable CNSPacket contract
  normalization.py    bounded numerical transforms
  organs.py           reference organ implementations
  plasticity.py       bounded Hebbian learning
  transformer.py      inspectable 54-channel self-attention mixer

apps/desktop/
  cns_bridge_desktop.py   Windows/macOS desktop shell + packaged self-test

apps/mobile/
  lib/                    Flutter mobile UI + local CNS companion engine
  test/                   12D/42D/54D and recurrence contract tests
  pubspec.yaml

installer/windows/
  CNSBridge.iss            one-click Windows installer definition

.github/workflows/
  ci.yml
  release-verification.yml
  packaged-release.yml     desktop/mobile builders + GitHub binary release

docs/
  ARCHITECTURE.md
  TRANSFORMER_GUIDE.md
  TEACHER_GUIDE.md
  ENGINEERING_MANUAL.md
  INTEGRATION_GUIDE.md
  APPS_AND_INSTALLERS.md
  RELEASE_VERIFICATION.md
  SCIENTIFIC_BOUNDARIES.md
examples/
tests/
```

## Design principles

**Model-independent.** The CNS state is separate from the generator.

**Fail-soft.** Optional sensors, QRNG/quantum sources, memory, or specialized backends should fail without collapsing the full runtime.

**Local-first capable.** The reference library itself requires no cloud API.

**Auditable.** State vectors and learning weights are inspectable NumPy arrays.

**Bounded adaptation.** Hebbian weights decay and clamp instead of growing without limit.

**Simulation is labeled.** Demo values are not represented as measurements.

**No consciousness claim.** This repository implements a cognitive/control architecture; it does not prove biological life, sentience, consciousness, or a soul.

## Research lineage and citation

Foundational deposited research:

**Cory Shane Davis. _12-Dimensional Cosmic Synapse Theory_. Zenodo. DOI: 10.5281/zenodo.17574447.**

Preferred citation metadata is in [`CITATION.cff`](CITATION.cff).

Citation is strongly requested for academic/research use. The Apache-2.0 software license itself remains permissive; see `LICENSE`, `NOTICE`, and `docs/LICENSING_AND_ATTRIBUTION.md`.

## Licensing

- **Software:** Apache License 2.0
- **Original manuals and documentation in `docs/`:** Creative Commons Attribution 4.0 International (CC BY 4.0), except quoted third-party material where separately noted
- **Research record:** governed by its Zenodo record and associated terms

This dual-license structure keeps the code broadly reusable while preserving clear attribution for the explanatory/publication material.

## Status

`v0.1.0` is a working public reference implementation with automated source, wheel, desktop installer, and mobile application build verification. It does **not** contain private COSMOS model weights, secret keys, vendor credentials, Apple signing identities, or a claim that this NumPy/mobile reference implementation reproduces every private/heavy COSMOS component.

## Start here

- Apps/installers/downloads: [`docs/APPS_AND_INSTALLERS.md`](docs/APPS_AND_INSTALLERS.md)
- Engineers: [`docs/ENGINEERING_MANUAL.md`](docs/ENGINEERING_MANUAL.md)
- Architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Transformer/state layer: [`docs/TRANSFORMER_GUIDE.md`](docs/TRANSFORMER_GUIDE.md)
- Teachers/students: [`docs/TEACHER_GUIDE.md`](docs/TEACHER_GUIDE.md)
- Integration teams: [`docs/INTEGRATION_GUIDE.md`](docs/INTEGRATION_GUIDE.md)
- Scientific claims/boundaries: [`docs/SCIENTIFIC_BOUNDARIES.md`](docs/SCIENTIFIC_BOUNDARIES.md)
