# Scientific Boundaries and Claim Discipline

This file is part of the project specification.

## What the repository demonstrates

The repository demonstrates a working software architecture with:

- normalized multimodal/state channels;
- 12→42→54 state expansion;
- recurrent state;
- bounded Hebbian-style association learning;
- local vector memory;
- Transformer-style self-attention over state channels;
- pluggable model/control backends;
- fail-soft entropy sources;
- basic output gating;
- reproducible tests.

## What it does not establish

The repository does not by itself establish that:

- 12D/42D/54D are physical dimensions;
- the system is conscious, sentient, alive, biological, or self-aware in the human sense;
- a quantum entropy source provides a computational advantage;
- the included reference attention block outperforms conventional architectures;
- the coherence heuristic measures truth;
- a bio/sensory summary diagnoses emotion, intent, deception, disease, or mental state;
- an association rule reproduces biological synapses;
- simulation output is a real-world measurement.

## Required evidence labels

Public demonstrations should label data as one of:

- **MEASURED** — directly recorded from a named instrument/source
- **DERIVED** — calculated from measured inputs
- **REPLAYED** — previously recorded measurement used again
- **SIMULATED** — generated for demonstration/testing
- **INFERRED** — model estimate
- **SPECULATIVE** — hypothesis or interpretation not established by the data

## Quantum terminology

The quantum bridge is an entropy/control interface. If connected to a real provider, document:

- provider/backend
- timestamp
- shots/samples
- live versus replay
- preprocessing/normalization
- fallback behavior

Do not describe a PRNG fallback as quantum data.

## Improvement claims

Any performance claim should include:

- baseline
- metric
- dataset or test harness
- number of runs
- uncertainty/error bars when appropriate
- ablation
- code/checkpoint version

## Privacy

Audio/video/biometric sources are sensitive. The reference library is designed for summary-level inputs and does not require raw recordings. Integrators are responsible for consent, retention, access control, and applicable law.
