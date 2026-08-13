# Synaptic Core v1

`Synaptic Core v1` is the language-neutral deterministic numerical subset of the COSMOS/Davis CNS public reference implementation.

It lets Python, C, C++, Rust, JavaScript, Go and foreign-function-interface consumers share the same state math without copying slightly different algorithms.

## Dimensions

- sensory state: 12 scalar channels
- context state: 42 scalar channels = 12 sensory + 30 context/control
- adaptive state: 54 scalar channels = 42 context + 12 recurrent/adaptive

These are numerical state channels, not literal spatial dimensions.

## Normalization

`finite(x, fallback)` returns `x` when finite, otherwise `fallback`.

`unit(x, low, high) = clamp((finite(x)-low)/(high-low), 0, 1)`.

`signed(x, scale) = tanh(finite(x)/scale)`.

## Raw 12-value input ordering

The C/JavaScript/Go portable encoder accepts this stable raw field order:

1. `audio_rms`
2. `dominant_frequency_hz`
3. `spectral_flatness`
4. `geometric_phase_rad`
5. `phase_velocity`
6. `av_coherence`
7. `pleasure`
8. `arousal`
9. `dominance`
10. `motion_energy`
11. `luminance`
12. `entropy`

The Python facade accepts `SensorySnapshot` and maps the same fields.

## 12-channel sensory encoder

The output channel formulas are:

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

Dominant frequency is normalized over `0..4000 Hz` and `phi=(1+sqrt(5))/2`.

## 12 -> 42 expansion

The first 12 values are copied unchanged. Thirty context values are appended, each mapped through `tanh(value)`.

## Bounded association update

For a 54D state `x`, reward/control gain `r` clamped to `[-1,1]`, learning rate `eta`, decay `lambda`, and matrix clamp `C`:

`W = clamp((1-lambda) * W + eta * r * outer(x,x), -C, C)`

The diagonal is always reset to zero.

Modulation:

`m = tanh(W @ x)`

The Python public class names this Hebbian plasticity; the language-neutral ABI uses neutral matrix/update naming while implementing the same public numerical rule.

## Adaptive 12-channel recurrent tail

For prior 54D state `p`, plastic modulation `m`, memory strength `s`, and entropy `q` in `[0,1]`:

`tail[i] = tanh(0.35*p[i] + 0.35*m[i] + 0.15*s + 0.15*(2*q-1))`

for `i=0..11`.

## 54D assembly and blend

The 54D base state is `context42 || tail12`.

A deterministic mixer may provide a same-size vector `mixed`. The public blend rule is:

`out = tanh(0.7*base + 0.3*mixed)`

The seeded Transformer mixer remains a higher-level implementation detail. Synaptic Core v1 intentionally excludes PRNG-specific parameter generation because programming-language random generators do not guarantee identical streams.

## Numeric conformance

Portable implementations use IEEE-754 double precision and the platform standard math library. Cross-language checks compare shapes, finiteness, channel ordering and representative values with small floating-point tolerances.

## Universal interoperability

The C implementation exposes a stable C ABI. Any environment capable of native FFI can bind it directly, including C#/.NET, Swift, Java/JVM, Kotlin/Native, Ruby, PHP, Lua, Julia, R, Zig, Nim and other native runtimes.

The maintained direct wrappers and universal FFI instructions are documented under `bindings/`.
