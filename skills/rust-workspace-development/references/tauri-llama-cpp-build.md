# Tauri + llama.cpp Build on Windows

## Overview

Building a Tauri desktop app that depends on `llama-cpp-2`/`llama-cpp-sys-2` with Vulkan support on Windows requires a specific toolchain chain. This is the setup that worked for the Aion project.

## Required Toolchain (install order)

1. **MSVC Build Tools** — `winget install --id Microsoft.VisualStudio.2022.BuildTools`
2. **LLVM/Clang** — `winget install --id LLVM.LLVM -e --accept-source-agreements --accept-package-agreements`
3. **CMake** — `winget install --id Kitware.CMake -e --accept-source-agreements --accept-package-agreements`
4. **Ninja** — `winget install --id Ninja-build.Ninja -e --accept-source-agreements --accept-package-agreements`
5. **Vulkan SDK** — download from `https://sdk.lunarg.com/sdk/download/latest/windows/vulkan-sdk.exe`, install to `C:\VulkanSDK\<version>`

## Environment Setup

Create `.cargo/config.toml` at workspace root:

```toml
[env]
CMAKE = "C:/Program Files/CMake/bin/cmake.exe"
PATH = "C:/Program Files/CMake/bin;C:/Program Files/LLVM/bin;C:/Tools;{PATH}"
```

## Build Commands

```bash
# Clean previous build artifacts (important when switching configs)
rm -rf packages/desktop/src-tauri/target
rm -rf crates/vendor/llama-cpp-sys-2/llama.cpp/build

# Build Tauri desktop app
cd packages/desktop
npx tauri build --debug
```

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Unable to find libclang` | LLVM not installed or not on PATH | Install LLVM, add to PATH via `.cargo/config.toml` |
| `Could not find a package configuration file provided by "SPIRV-Headers"` | Vulkan SDK cmake dir not in `CMAKE_PREFIX_PATH` | Add `C:/VulkanSDK/<version>/Lib/cmake` to `CMAKE_PREFIX_PATH` |
| `Please install Vulkan SDK and ensure that VULKAN_SDK env variable is set` | Vulkan SDK not installed | Install Vulkan SDK |
| `ninja: error: loading 'build.ninja': The system cannot find the file specified` | Stale build directory from previous failed build | Delete `target` and `llama.cpp/build` dirs |
| `failed to execute command: program not found is cmake not installed?` | CMake not on PATH | Add CMake to PATH via `.cargo/config.toml` |
| `OpenSSL not found, HTTPS support disabled` | OpenSSL not installed (non-fatal) | Can ignore, or install via `winget install --id ShiningLight.OpenSSL` |

## Build Time

Expect 8-10 minutes for a clean debug build on a modern machine. The `llama-cpp-sys-2` crate compiles llama.cpp from source, which is the bulk of the time.

## Output Artifacts

- Debug executable: `packages/desktop/src-tauri/target/debug/aion-desktop.exe`
- MSI installer: `packages/desktop/src-tauri/target/debug/bundle/msi/Aion_0.1.0_x64_en-US.msi`
- NSIS installer: `packages/desktop/src-tauri/target/debug/bundle/nsis/Aion_0.1.0_x64-setup.exe`
