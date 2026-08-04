---
name: rust-ffi-cross-language
description: 'Generate C-compatible FFI bindings from Rust crates for Python, Node, Swift, and Kotlin consumers.'
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: ["rust", "ffi", "cbindgen", "bindgen", "interop"]
    related_skills: ["rust-package-build", "rust-ownership-borrowing"]
---

Use when a Rust crate needs to be called from Python, Node.js, Swift, or Kotlin
without a separate FFI codegen step.

# Rust FFI Binding Generation
## Overview
cbindgen reads Rust `extern "C"` blocks and emits idiomatic C headers.
Pair with language-specific binders: `cffi` (Python), `node-ffi-napi` (Node),
a `.swift` wrapper (Swift), or `JNA` (Kotlin/Java).

## Procedure
1. `cargo add --build cbindgen` and add a `build.rs` that calls
   `cbindgen::generate().write_to_file("mycrate.h")`.
2. Annotate every `#[no_mangle] extern "C"` function with `#[repr(C)]` and
   use only POD-compatible types (ints, pointers, slices as `*const`/`*mut`).
3. For strings, pass `*const c_char` (null-terminated) or
   `(*const u8, usize)` byte-slice pairs to avoid allocator coupling.
4. Build: `cargo build --release`. Distribute the `.so`/`.dylib`/`.dll`
   alongside the generated header.
5. Language binders:
   - Python: `ffi.cdef(open("mycrate.h").read()); lib = ffi.dlopen("libmycrate.so")`
   - Node: define via `ffi-napi` using the same C signatures.
   - Swift: `import Glibc` / `Darwin` and call through the `.so`.
6. Never cross an allocator boundary — Rust must allocate+deallocate (use a
   `free` function exported the same way), or copy into a caller-owned buffer.

## Pitfalls
- Panics across the FFI boundary are UB; wrap entry points in
  `std::panic::catch_unwinding`.
- `String`/`Vec` are NOT C-compatible — leak or segfault.
- Debug vs release ABIs differ; always ship release builds.

## Verification
- [ ] `cbindgen --config cbindgen.toml --crate mycrate --output mycrate.h` exits 0.
- [ ] `strings libmycrate.so | grep <exported_symbol>` shows the symbol.
- [ ] Python: `python3 -c "import mymod; print(mymod.add(2,3))"` prints 5.
