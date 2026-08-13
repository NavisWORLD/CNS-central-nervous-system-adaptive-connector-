# Language compatibility matrix

| Language / runtime | Synaptic Core v1 route | Status |
|---|---|---|
| Python | `cns_bridge.synaptic` | Maintained direct API |
| C | `c/include/cns_state_core.h` + `c/src/cns_state_core.c` | Maintained ABI/core |
| C++ | `cpp/include/cns_state_core.hpp` | Maintained wrapper |
| JavaScript / Node / browser | `javascript/core.mjs` | Maintained direct module |
| TypeScript | import the JavaScript ES module | Compatible; typed declaration package not yet published |
| Go | `go/` native encoder + cgo recurrent core | Maintained wrapper |
| Rust | `rust/` safe wrappers linked to C core | Maintained wrapper |
| Dart / Flutter | `../apps/mobile/lib/cns_engine.dart` | Existing mobile implementation |
| C# / .NET | P/Invoke to C ABI | Supported FFI route |
| Swift | C interoperability to C ABI | Supported FFI route |
| Java / JVM | JNI / Foreign Function & Memory API | Supported FFI route |
| Kotlin/Native | C interop | Supported FFI route |
| Ruby | Fiddle / FFI to C ABI | Supported FFI route |
| PHP | FFI extension to C ABI | Supported FFI route |
| Lua | LuaJIT FFI or native module | Supported FFI route |
| Julia | `ccall` to C ABI | Supported FFI route |
| R | `.C` / `.Call` native bridge | Supported FFI route |
| Zig | direct C import | Supported FFI route |
| Nim | C import / dynlib binding | Supported FFI route |
| Other native runtimes | standard C foreign-function interface | Portable route |

The universal route uses caller-owned arrays of IEEE-754 doubles, so the ABI does not transfer allocator ownership across language boundaries.

See `FFI_GUIDE.md` and `../spec/SYNAPTIC_CORE_V1.md`.
