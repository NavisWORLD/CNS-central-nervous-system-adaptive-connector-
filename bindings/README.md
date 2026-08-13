# Cross-language state bindings

This directory contains portable software implementations of the deterministic CNS state functions defined in `../spec/SYNAPTIC_CORE_V1.md`.

## Maintained first-class surfaces

- **Python** — `../src/cns_bridge/synaptic.py`
- **C** — `c/` is the stable ABI and numerical source of truth
- **C++** — `cpp/` is a convenience wrapper over the C ABI
- **JavaScript / TypeScript-compatible runtimes** — `javascript/core.mjs` is a dependency-free ES module
- **Go** — `go/` provides a native 12D encoder plus cgo wrappers over the shared C recurrent core
- **Rust** — `rust/` provides safe array-oriented wrappers over the shared C ABI
- **Dart / Flutter** — the existing mobile companion implementation lives in `../apps/mobile/lib/cns_engine.dart`

## Universal compatibility route

Any runtime with a C foreign-function interface can use the exact same numerical kernel through `c/include/cns_state_core.h`. This includes C#/.NET, Swift, Java/JVM through JNI or Foreign Function & Memory APIs, Kotlin/Native, Ruby, PHP, Lua, Julia, R, Zig, Nim and many other environments.

See `FFI_GUIDE.md` for shared-library build commands, vector layouts, and ABI calls.

## Why one C ABI matters

The recurrent update and modulation functions are intentionally centralized rather than independently rewritten in every language. This reduces numerical drift and makes the portable software claim auditable: different runtimes can call the same kernel while keeping ergonomic native wrappers at the edge.

## Scope

`Synaptic Core v1` covers deterministic normalization, 12-channel encoding, 12→42 expansion, bounded association-weight updates, recurrent-tail generation, 54D assembly, and the bounded 54D blend. The seeded Python Transformer remains a higher-level implementation because programming-language random-number generators do not share identical streams by default.
