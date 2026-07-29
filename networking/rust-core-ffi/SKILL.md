---
name: rust-core-ffi
title: Rust Core FFI
description: Use when generating cross-language FFI bindings for Rust.
category: networking
tags: [ffi, rust, bindings, uniffi, cross-language, cbindgen]
---

# Rust Core FFI

**Trigger**: Use when generating cross-language FFI bindings for the Rust core engine.

**Libraries**: `uniffi` (Mozilla's cross-language bindings), `cbindgen` (C headers), `jni` (Java/Kotlin)

**Implementation**: UniFFI for Python/Swift/Kotlin bindings from Rust. Define UDL (UniFFI Definition Language) file for exported interface. Generate Python `.so`/`.dylib`, Swift `.a`, Kotlin `.so`. `cbindgen` for C-compatible headers. Thread-safe exports via `Arc<RwLock<>>` pattern. Async Rust exports via UniFFI proc-macro. Memory management: Rust owns, borrows to caller.

**Connected**: `python-orchestrator`, `ios-vpn-adblocker`, `android-vpn-adblocker`, `svelte-web-dashboard`, `clojure-rule-engine`, `service-orchestrator`
