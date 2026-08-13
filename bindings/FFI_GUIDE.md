# Universal language binding guide

The C interface in `c/include/cns_state_core.h` is the stable native boundary for the portable CNS state functions.

Any runtime that can call a C shared library can use the same implementation without translating the numerical rules. This includes Rust, Go, C#, Swift, Kotlin/Native, Ruby, PHP, Lua, Julia, R, Zig, Nim and many other environments.

## Native library

Compile the implementation as a shared library.

Linux:

```bash
gcc -O2 -fPIC -shared -Ibindings/c/include bindings/c/src/cns_state_core.c -lm -o libcns_state_core.so
```

macOS:

```bash
clang -O2 -fPIC -dynamiclib -Ibindings/c/include bindings/c/src/cns_state_core.c -lm -o libcns_state_core.dylib
```

Windows with MinGW:

```bash
gcc -O2 -shared -Ibindings/c/include bindings/c/src/cns_state_core.c -o cns_state_core.dll
```

## Stable shapes

- input vector: 12 doubles
- context vector: 30 doubles
- expanded vector: 42 doubles
- full state vector: 54 doubles
- association matrix: 2916 doubles stored row-major

## Stable calls

- `cns_encode_12d`
- `cns_expand_42d`
- `cns_weight_update`
- `cns_weight_modulation`
- `cns_recurrent_tail`
- `cns_assemble_54d`
- `cns_blend_54d`

All functions return `0` on success and a nonzero value on invalid input. Caller-owned arrays are used so there is no cross-language allocator ownership problem.

The formulas and channel ordering are defined by `../spec/SYNAPTIC_CORE_V1.md`.
