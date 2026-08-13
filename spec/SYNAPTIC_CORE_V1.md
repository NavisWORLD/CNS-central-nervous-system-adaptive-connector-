# Synaptic Core v1

`Synaptic Core v1` is the language-neutral deterministic numerical subset of the
COSMOS/Davis CNS public reference implementation.

It exists so Python, C, C++, Rust, JavaScript/TypeScript, Go, Java/Kotlin,
C#/.NET, Swift and FFI consumers can share the same state math without copying
slightly different algorithms.

## Dimensions

- sensory state: 12 scalar channels
- context state: 42 scalar channels = 12 sensory + 30 context/control
- adaptive state: 54 scalar channels = 42 context + 12 recurrent/adaptive

These are numerical state channels, not literal spatial dimensions.

## Normalization

`finite(x, fallback)` returns `x` when finite, otherwise `fallback`.

`unit(x, low, high) = clamp((finite(x)-low)/(high-low), 0, 1)`.

`signed(x, scale) = tanh(finite(x)/scale)`.

## 12-channel sensory encoder

Given the public sensory fields:

1. frequency mass = `sqrt(rms) * (2*freq_norm - 1)`
2. geometric phase = `sin(phase_rad)`
3. spectral flatness = `2*flatness - 1`
4. phase velocity = `tanh(phase_velocity / 10)`
5. A/V entanglement = `2*av_coherence - 1`
6. pleasure = clamp to `[-1,1]`
7. arousal = `2*arousal - 1`
8. dominance = `2*dominance - 1`
9. audio psi = `sin(2*pi*freq_norm) * rms`
10. phi harmonics = `cos(2*pi*((freq_norm*phi) mod 1)) * (0.25 + 0.75*rms)`
11. motion/luminance coherence = `2*(1-min(1, abs(motion-luminance))) - 1`
12. entropy = `2*entropy - 1`

where dominant frequency is normalized over `0..4000 Hz` and
`phi=(1+sqrt(5))/2`.

## 12 -> 42 expansion

The first 12 values are copied unchanged. Thirty context values are appended,
each mapped through `tanh(value)`.

## Bounded Hebbian update

For a 54D state `x`, reward `r` clamped to `[-1,1]`, learning rate `eta`,
decay `lambda`, and weight clamp `C`:

`W = clamp((1-lambda) * W + eta * r * outer(x,x), -C, C)`

The diagonal is always reset to zero.

Modulation:

`m = tanh(W @ x)`

## Adaptive 12-channel recurrent tail

For prior 54D state `p`, plastic modulation `m`, memory strength `s`,
and entropy `q` in `[0,1]`:

`tail[i] = tanh(0.35*p[i] + 0.35*m[i] + 0.15*s + 0.15*(2*q-1))`

for `i=0..11`.

## 54D blend

A deterministic mixer may provide a same-size vector `mixed`.
The public blend rule is:

`out = tanh(0.7*base + 0.3*mixed)`

The seeded Transformer mixer remains a higher-level implementation detail; this
core contract intentionally excludes PRNG-specific weight generation so all
languages can be bit-close without requiring identical random generators.

## Numeric conformance

Implementations must match `golden_vectors.json` within `1e-9` for scalar
functions and within `1e-8` for vector tests unless a platform's standard
library documents lower floating-point precision.

## Universal interoperability

The C implementation exposes a stable C ABI. Any environment capable of FFI can
bind it directly, including Ruby, PHP, Lua, Julia, R, Swift, Zig, Nim and other
native runtimes. Network/process integrations may instead use the documented
JSON vector shapes.
