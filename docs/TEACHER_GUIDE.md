# Teacher Guide: Building a Software CNS

## Audience

This guide is for instructors teaching software architecture, AI systems, robotics, multimodal computing, adaptive systems, or introductory computational neuroscience analogies.

The project should be taught as an **engineering state machine inspired by nervous-system organization**, not as a biological CNS and not as proof of consciousness.

## Learning objectives

After completing the unit, students should be able to:

1. explain the difference between a model and a system architecture;
2. normalize heterogeneous sensor values into a common state vector;
3. explain the 12D → 42D → 54D state pipeline;
4. distinguish observation channels from recurrent/adaptive channels;
5. implement bounded Hebbian-style association learning;
6. explain self-attention over state channels;
7. integrate a custom backend without coupling it to sensor code;
8. design fail-soft behavior;
9. distinguish live data, replayed data, simulated data, and inferred data;
10. design an experiment that can falsify an engineering claim.

## Suggested 6-session unit

### Session 1 — Why a CNS layer?

Start with two architectures:

```text
A: prompt -> LLM -> answer
B: sensor -> state -> memory -> model -> action -> learning -> state
```

Ask students which one can maintain an independent shared state across multiple models and sensors.

**Lab:** run `cns-bridge status` and inspect the organ registry.

### Session 2 — 12D encoding

Discuss unit mismatch: Hertz, percentages, radians, and probabilities cannot be mixed naively.

**Lab:** modify `SensorySnapshot`, run `CNS12DEncoder`, graph each channel, and identify saturation.

**Discussion:** why is a “dimension” here a vector channel rather than another physical dimension?

### Session 3 — Context and recurrence

Show that a snapshot alone has no history. Compare two identical sensory snapshots with different previous states.

**Lab:** execute five harness cycles and inspect `state_delta`, memory count, and the final 12 adaptive channels.

### Session 4 — Hebbian plasticity

Teach the simplified rule:

```text
ΔW = η r x xᵀ
```

Then explain decay and clamping.

**Lab:** reward one repeated state and inspect the association matrix before/after.

### Session 5 — Attention and backend separation

Walk through `ReferenceStateTransformer`.

**Lab A:** disable attention mixing and compare state trajectories.

**Lab B:** connect `CallableBackend` to a simple rules engine. Demonstrate that the CNS works without an LLM.

### Session 6 — Scientific audit

Give students four labels:

- MEASURED
- DERIVED
- SIMULATED
- SPECULATIVE

Require every dashboard field or report claim to receive one label.

**Final project:** build one adapter (robot sensor, game telemetry, environmental data, MIDI, network metrics, etc.), create a measurable task, compare CNS-enabled versus baseline behavior, and write a limitations section.

## Classroom experiments

### Experiment A — Memory ablation

Hypothesis: memory improves repeated-context decision consistency.

Run identical sequences with memory enabled and disabled. Define consistency before collecting results.

### Experiment B — Plasticity ablation

Hypothesis: bounded Hebbian updates improve a repeated association task.

Compare fixed zero weights against online updates.

### Experiment C — Entropy-source invariance

Test system entropy, deterministic replay, and a constant 0.5 source. The task should reveal whether entropy is useful or merely decorative.

### Experiment D — Sensor dropout

Remove audio or vision inputs mid-run. The system should continue operating and flag the missing source rather than fabricate measurements.

## Assessment rubric (100 points)

- 20: correct state normalization
- 15: documented channel schema
- 15: correct recurrent pipeline
- 10: backend isolation
- 10: fail-soft handling
- 10: experiment design
- 10: reproducibility
- 10: scientific boundaries and limitations

## Common misconceptions

**“54D means 54 physical dimensions.”** No. It means 54 numerical state channels.

**“Quantum entropy makes the model quantum intelligent.”** No. It is an optional stochastic/control input.

**“Hebbian means biological brain.”** No. This package uses a mathematical association rule inspired by Hebbian learning.

**“A coherence score means the answer is true.”** No. The included gate is a software quality heuristic.

**“A recurrent state proves consciousness.”** No. Recurrence is an architecture property.

## Instructor safety/privacy notes

Do not require students to submit biometric data. Use synthetic or non-sensitive sensor summaries by default. If microphones/cameras are used, process locally where possible, obtain explicit consent, and store only the minimum data needed for the lab.

## Citation exercise

Students should cite the research lineage and the code separately. See `CITATION.cff` and `docs/LICENSING_AND_ATTRIBUTION.md`.
