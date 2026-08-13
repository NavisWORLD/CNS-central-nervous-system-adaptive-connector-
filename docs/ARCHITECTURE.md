# Architecture Guide

## 1. System objective

The CNS Adaptive Connector is a **state integration and recurrence layer**. It accepts observations from arbitrary sources, converts them into a stable numerical representation, adds context and learned history, makes that state available to a downstream decision/generation backend, evaluates the output, and feeds the outcome into the next cycle.

It solves a systems problem: how do sensors, memory, stochastic control signals, agents, models, and actions share one coherent state without every component being tightly coupled to every other component?

## 2. Layer map

```text
INPUT SOURCES
text | audio summaries | vision summaries | bio | tools | environment | memory
                                  │
                                  ▼
                          Normalization layer
                                  │
                                  ▼
                         12-channel encoder
                                  │
                                  ▼
                       42-channel context state
                                  │
                    memory / entropy / controls
                                  │
                                  ▼
                       54-channel adaptive state
                                  │
                                  ▼
                 Transformer-style attention mixer
                                  │
                                  ▼
                           Synaptic Field
                                  │
                                  ▼
                   model / agent / control backend
                                  │
                           coherence gate
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
                  accept                     fallback
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                               action
                                  │
                                  ▼
                    memory + Hebbian plasticity
                                  │
                                  └──────────→ next cycle
```

## 3. 12D state

“12D” is an engineering label for a 12-component vector, not a physical-space claim.

The reference encoder publishes these channels:

1. frequency mass
2. geometric phase
3. spectral flatness
4. phase velocity
5. A/V entanglement/coherence
6. pleasure
7. arousal
8. dominance
9. audio Ψ proxy
10. φ-harmonic proxy
11. motion/luminance coherence
12. entropy

The exact sensor formulas are replaceable. The public contract that matters is: **12 finite, normalized values with documented semantics**.

## 4. 42D context

The 42D vector is:

```text
12 sensory channels + 30 contextual/control channels
```

The reference context channels include system load, memory pressure, tool activity, novelty, uncertainty, coherence, reward, error rate, latency, environment summaries, retrieval strength, worker disagreement, entropy mix, safety/fallback pressure, and exploration/precision/creativity biases.

Applications may rename or remap those 30 channels as long as their schema is versioned.

## 5. 54D adaptive state

The 54D vector is:

```text
42 contextual channels + 12 adaptive/recurrent channels
```

The reference adaptive tail is a bounded function of:

- previous CNS state
- Hebbian modulation
- retrieved-memory strength
- entropy/control value

Then the entire 54-channel vector is passed through the public attention mixer and residual blending.

A compact abstraction is:

```text
x12(t) = Encode(observation(t))
x42(t) = Expand(x12(t), context(t))
a12(t) = tanh(previous + plasticity + memory + entropy)
x54_raw(t) = concat(x42(t), a12(t))
x54(t) = tanh(0.7*x54_raw + 0.3*Transformer(x54_raw))
```

The coefficients in the reference code are implementation defaults, not universal constants.

## 6. Synaptic Field

The Synaptic Field stores current and previous 54D state. It exposes transition magnitude and iteration count. It is intentionally simple because the field is the shared bus, not a hidden black box.

A production system may add:

- timestamped state history
- uncertainty covariance
- per-organ state partitions
- event streaming
- distributed replication
- real-time dashboards

## 7. Entropy/quantum bridge

The entropy bridge accepts user-supplied callables returning a scalar in `[0, 1]`.

Possible sources:

- hardware QRNG
- quantum measurement service
- operating-system cryptographic entropy
- simulation RNG
- deterministic replay trace

The bridge is **control context**, not the language generator. It fails soft to system entropy.

## 8. Memory

The default memory is deliberately transparent: a bounded deque of vectors plus payloads and cosine-similarity retrieval.

Replace it with any persistent system by implementing equivalent `add` and `recall` behavior. The state packet should contain retrieval summaries, not private raw stores.

## 9. Hebbian plasticity

The reference rule is:

```text
W <- (1 - decay) W + learning_rate * reward * outer(x, x)
```

Then:

- diagonal is zeroed
- values are clamped
- state modulation is `tanh(W @ x)`

This is a software association rule inspired by Hebbian learning. It is not a claim that the implementation is a biological nervous system.

## 10. Backends

A backend only needs one asynchronous method:

```python
async def generate(prompt: str, packet: CNSPacket) -> str:
    ...
```

This can wrap:

- local LLM
- cloud LLM
- planning model
- robot policy
- rules engine
- simulation controller
- multimodel swarm
- database decision service

The backend receives CNS state. It does not own CNS state.

## 11. Coherence and failover

The public coherence gate is intentionally simple and deterministic. It catches empty/degenerate outputs, not truth.

Production gates should be domain-specific and may include:

- schema validation
- safety constraints
- temporal consistency
- task success metrics
- physical feasibility
- confidence calibration
- human approval

## 12. Seven-organ compatibility map

| Organ | Public implementation | Role |
|---|---|---|
| Synaptic Field | `SynapticField` | shared recurrent state |
| Quantum Bridge | `CompositeEntropyBridge` | optional entropy/control |
| Emeth Harmonizer | `EmethHarmonizer` | state coherence proxy |
| Swarm Plasticity | `HebbianPlasticity` | bounded association learning |
| Swarm Awareness | `SwarmAwareness` | inspect state motion |
| Swarm Daemons | backend/worker extension | specialized workers |
| Brain Surgeon | `BrainSurgeon` | health/failover registry |

## 13. Failure model

A production CNS should prefer degradation over total collapse:

```text
camera unavailable     -> run without vision summary
microphone unavailable -> run without audio summary
external entropy fails -> use system entropy
memory unavailable     -> run stateless for the turn
native backend fails   -> use fallback backend
worker fails           -> remove worker from routing
invalid state          -> reject before backend execution
```

## 14. Versioning

Downstream systems should record:

- package version
- state schema version
- encoder version
- transformer weight hash
- memory implementation
- entropy source and whether it was live/replayed
- backend name/version

That makes experiments reproducible.
