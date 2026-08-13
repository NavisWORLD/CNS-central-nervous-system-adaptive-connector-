# CNS Transformer and 54D State Guide

## What “transformer” means in this repository

The public package contains `ReferenceStateTransformer`, a **single-block Transformer-style self-attention mixer over 54 scalar CNS channels**.

It is intentionally inspectable NumPy code. It is not represented as a dump of private/heavy COSMOS model weights and it is not evidence of a newly proven replacement for conventional Transformer attention.

The purpose is to give any engineer a concrete, runnable reference for mixing the 54D state before it enters a model, policy, or agent.

## Input

```text
x ∈ R^54
```

Each scalar state channel becomes one token. For token `i`:

```text
h_i = x_i * input_scale + positional_embedding_i
```

So the 54 scalar channels become a matrix:

```text
H ∈ R^(54 × d_model)
```

The default `d_model` is 16.

## Self-attention

The reference block computes:

```text
Q = H Wq
K = H Wk
V = H Wv
A = softmax(Q Kᵀ / sqrt(d_model))
M = A V
```

Then:

```text
H' = LayerNorm(H + M Wo)
```

A learned readout vector converts each token back to one scalar:

```text
y_i = tanh(H'_i · r)
```

Result:

```text
y ∈ R^54
```

## Residual state blend

The harness does not replace raw state with attention output. It blends them:

```text
state_54 = tanh(0.7 * raw_state_54 + 0.3 * attention_state_54)
```

This makes the reference system stable enough for demonstration while preserving cross-channel mixing.

## Determinism

`ReferenceStateTransformer(seed=707)` initializes deterministic weights from the supplied seed. The weights can be saved with:

```python
transformer.save("state_transformer.npz")
```

and loaded with:

```python
transformer.load("state_transformer.npz")
```

For research runs, record the seed or hash the saved weight file.

## Training

The reference attention block is an inference-only demonstrator. To make it trainable, port the equations to PyTorch/JAX/TensorFlow and optimize against an explicit task objective.

Recommended targets include:

- next-state prediction
- action success
- sensor reconstruction
- anomaly detection
- calibrated task reward
- multimodal alignment

Do not use “the state looks interesting” as a training target. Define a measurable loss.

## Relationship to language models

The state transformer and the language model are different objects.

```text
54D state transformer -> state/context representation
LLM/backend           -> language or action generation
```

A backend can consume `packet.adaptive_54d` by:

- serializing selected state to a prompt
- projecting state into model embeddings
- conditioning a policy network
- using state to choose tools/models
- adjusting decoding controls

## Safe integration rule

Do not let an arbitrary model directly rewrite the transformer's weights in production. Prefer:

1. collect outcomes
2. train/evaluate offline
3. compare against baseline
4. save a candidate checkpoint
5. approve promotion explicitly
6. retain rollback checkpoint

The small Hebbian matrix in this library is allowed to update online because it is bounded, decayed, separately inspectable, and not arbitrary executable code.

## Extending to multiple attention blocks

A production implementation can stack blocks:

```text
54 scalar channels
    ↓
embedding
    ↓
attention block × N
    ↓
feed-forward layers
    ↓
readout / policy / conditioning vector
```

Keep the public state schema separate from the model's internal hidden dimension. `54D` describes the CNS interface, not the internal width of every neural network.

## Validation checklist

For any replacement transformer, report:

- seed/checkpoint hash
- number of parameters
- task dataset
- train/validation/test split
- loss function
- baseline comparison
- latency
- state-transition stability
- ablation with transformer disabled
- ablation with memory disabled
- ablation with plasticity disabled
- ablation with entropy fixed

That is how claims about improvement become measurable.
