---
name: c-plus-plus-structural-verification
description: "Verify C++ correctness without a build toolchain."
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cpp, verification, structural-check, build-independent, no-compiler]
    related_skills: [requesting-code-review, systematic-debugging]
---

# C++ Structural Verification (No Build Toolchain)

## Overview

When a C++ compiler is unavailable in the environment (no MSVC, no GCC, no Clang), structural verification catches the most common correctness issues that a compiler would normally find. Run these checks before committing any C++ changes when `cmake --build` or `ninja` cannot execute.

## When to Use

- After adding new C++ methods to a header file
- After expanding a Vulkan implicit layer hook surface
- When the sandbox lacks a C++ build toolchain
- Before `git commit` on C++ changes when compilation is deferred

## Three Structural Checks

### 1. Header ↔ Implementation Consistency

Every method declared in the header must have a definition in the .cpp file. Orphan declarations cause linker errors, not compiler errors — they pass compilation and only surface at link time.

```bash
# Declared in header
grep -oP 'ClassName::\w+(?=\s*\()' myclass.h | sort -u
# Defined in implementation
grep -oP 'ClassName::\w+(?=\s*\()' myclass.cpp | sort -u
```

The .cpp set must be a superset of the .h set (except for the constructor/destructor names).

### 2. Dispatch Table Completeness

When adding hooks to a Vulkan layer, every new function must appear in:
1. The **GIPA dispatch table** (`vkGetInstanceProcAddr`)
2. The **device dispatch table** (`vkGetDeviceProcAddr`)
3. The **per-device function pointer array** (`DeviceCtx` or equivalent struct)

```bash
# Verify each new hook appears at least twice (GIPA + device-level)
grep -c "vkCmdDraw\|vkCmdDispatch\|vkCmdPushConstants" layer_entry.cpp
```

### 3. Function Pointer Initialization

All function pointer fields in dispatch structs must be explicitly initialized to `nullptr`. An uninitialized function pointer causes a segfault at runtime with no compile error.

## MSVC-Specific Compilation Pitfalls

These issues do not appear on Clang/GCC and cause cascading failures on MSVC:

- **Missing transitive includes** — `std::vector` used without `#include <vector>`. GCC/Clang pull it in transitively; MSVC does not. Always verify every type in a header has its own include.
- **`__builtin_popcount` unavailable** — Use `#ifdef _MSC_VER` / `__popcnt` / `#else` / `__builtin_popcount` / `#endif` guards.
- **`mutable` for mutexes in const methods** — `std::lock_guard<std::mutex>` requires non-const. If a `const` method needs locking, the mutex must be `mutable`.
- **Access specifier ordering** — Members used in `public:` methods but declared in `private:` cause "cannot access private member" errors. Move struct definitions (like `ResourceMeta`, `JITStutterStats`) to `public:` if returned from public methods.
- **Header parse cascade** — If a header has a fatal error, the entire class declaration becomes invisible. Symptom: `'ClassName': is not a class or namespace name` in `.cpp`. Fix by compiling headers individually.
- **`_CRT_SECURE_NO_WARNINGS`** — `std::getenv()` triggers C4996. Add as compile definition in CMakeLists.txt.
- **`std::atomic<NonTrivialType>` → `std::construct_at` failure** — `std::atomic` with non-trivially-constructible types (structs with default member initializers, or non-copyable types containing `std::atomic`) causes MSVC's `std::construct_at` to fail with C2672. The error is cryptic: `'std::construct_at': no matching overloaded function found`. Root cause: `MipResidencyState` contains `std::atomic<bool>` → non-copyable → `std::vector<MipResidencyState>` fails on resize. **Fix**: Replace `std::vector<NonCopyableType>` with `std::unique_ptr<NonCopyableType[]>` + `std::make_unique`. Add explicit move constructor and delete copy constructor on the element type.
- **`asm volatile` unavailable on MSVC** — GCC/Clang inline assembly syntax doesn't compile on MSVC. Use `#ifdef _MSC_VER` / `#include <intrin.h>` / `_ReadWriteBarrier()` / `#else` / `asm volatile(...)` / `#endif`.
- **DLL export for Vulkan implicit layers** — `VKAPI_ATTR` expands to nothing on Windows. To export symbols from a DLL, add `__declspec(dllexport)` explicitly: `SYNAPSE_EXPORT VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL functionName(...)`. Define `SYNAPSE_EXPORT` as `__declspec(dllexport)` on Windows, empty elsewhere.
- **`CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS` must be a CMake variable** — Setting it as a target property (`set_target_properties(... PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON)`) does NOT work with the VS generator. Must use `set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)` at the top level, before `add_library`.
- **Vulkan function pointer signature mismatches** — `PFN_vkCmdPushConstants` has 6 parameters (includes `VkShaderStageFlags stageFlags`), not 5. Always verify against the Vulkan spec header. Mismatched argument count causes C2198 "too few arguments for call".
- **Line continuation in comments** — `\\` at end of comment lines triggers C4010 "single-line comment contains line-continuation character". This warning becomes an error with `/WX`. Remove trailing `\\` from comment banner lines.

## Vulkan SDK Header Management

When Vulkan SDK is not installed, download from Khronos GitHub:
- Core: `vulkan.h`, `vulkan_core.h`, `vk_platform.h`, `vk_layer.h`
- Video codecs: `vk_video/vulkan_video_codec_*.h` (11 files)
- Library: `vulkan-1.lib` from System32 or any Vulkan loader
- Set `VULKAN_SDK` env var for `find_package(Vulkan)`

## Docker-Based Build Verification

When Docker is available, use it for reproducible builds instead of relying on host-installed toolchains:

```bash
# Build the Docker image (one-time)
docker build -t synapse-igpu-shim:latest -f docker/Dockerfile .

# Compile inside container
docker compose run build

# Run tests
docker compose run test

# Full CI pipeline
docker compose run ci
```

**Dockerfile essentials**: Ubuntu 24.04 + Clang 17 + CMake + Ninja + Vulkan SDK + ccache. Copy MCP server for AI agent integration.

**docker-compose.yml pattern**: Use `extends: base` for shared config, separate `profiles` for build/test/lint/ci/mcp services.

## Pitfalls

- **No compiler in sandbox** — document explicitly that a real toolchain (MSVC 19.x / Clang 17) is required for full compilation. Structural checks do NOT prove the code compiles.
- **Orphan declarations** — the most common mistake when expanding a class. A declaration without a definition compiles fine and only errors at link time.
- **Uninitialized function pointers** — `nullptr` call segfaults at runtime with no diagnostic. Always initialize in the struct definition.
- **Docker daemon not running** — On Windows, Docker Desktop WSL2 backend may fail to start. Fall back to MSVC local build or diagnose WSL2 before assuming Docker is available.
- **VS generator vs NMake** — `cmake -G "NMake Makefiles"` requires LIB/INCLUDE/PATH set manually; VS generator handles this. Prefer VS generator on Windows when NMake fails with "cannot open kernel32.lib".
- **MSVC header order sensitivity** — Nested structs must be defined before use in the same class body. Unlike .cpp files, class body declarations are order-dependent.
- **`_CRT_SECURE_NO_WARNINGS` in CMakeLists.txt** — must use `add_compile_definitions()`, not `#define` in individual source files.