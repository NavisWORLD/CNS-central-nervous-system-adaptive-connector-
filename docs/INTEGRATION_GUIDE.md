# Integration Guide

## Integration pattern A: existing LLM application

Keep your current model call. Add CNS state beside it:

```text
user input -> CNS step -> packet.adaptive_54d -> model context -> response
```

Use a custom backend adapter so the CNS owns recurrence and the LLM remains replaceable.

## Integration pattern B: robotics

```text
sensors -> local feature extraction -> CNS -> policy -> safety controller -> actuators
```

The safety controller must be outside the generative model and may veto actions.

## Integration pattern C: game/simulation

Map game telemetry into `SensorySnapshot` and `context`. The backend can emit NPC decisions, simulation control, or narrative output. Save CNS memory with the world save if continuity is desired.

## Integration pattern D: multi-agent swarm

Use the 54D state as shared context. Each specialist can receive the same packet while the orchestrator selects or reconciles outputs.

Do not force all agents to share private scratch state. Share the explicit CNS packet and controlled memory summaries.

## Integration pattern E: industrial telemetry

Replace human-sensory semantics with machine channels, but preserve the interface sizes or create a schema version.

Example mapping:

```text
12D: vibration, temperature, current, pressure, flow, error rates...
42D: 12D + machine/environment/control context
54D: 42D + adaptive/history channels
```

## Creating an adapter

An adapter should:

1. acquire data;
2. validate freshness;
3. summarize locally;
4. normalize units;
5. mark unavailable values;
6. return only the fields needed by the CNS.

Avoid hidden side effects inside adapters.

## Structured actions

For structured systems, ask the backend for JSON and validate it:

```json
{"action":"MOVE","speed":0.2,"direction":"LEFT"}
```

Then enforce schema and policy limits before execution.

## Entropy adapters

An entropy adapter returns a scalar in `[0,1]`. Keep provenance in the source name. Replayed quantum measurements should be labeled replay, not live.

## Memory adapters

Production memory may use a vector DB or relational store. Preserve these semantics:

- bounded retrieval count
- explicit payload fields
- retention controls
- deletion support
- similarity score exposed

## Compatibility test

Every integration should pass a test where all optional external services are disabled. The CNS should still complete a cycle using local defaults.
