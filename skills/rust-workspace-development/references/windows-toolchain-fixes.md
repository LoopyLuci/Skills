# Windows Toolchain Fixes

## VS Build Tools

- Winget can return success without installing. If `ls "C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC"` is empty, download and run `vs_BuildTools.exe` directly.
- After install, MSVC lives under `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\<version>\bin\Hostx64\x64\`.
- Always run cargo via `vcvars64.bat`; otherwise git-bash `link.exe` is found first.

## LLVM/Clang

- Crates using `bindgen` (e.g. `llama-cpp-sys-2`, `ort`) require `libclang.dll`. Install via: `winget install --id LLVM.LLVM -e --accept-source-agreements --accept-package-agreements`
- After install: `ls "/c/Program Files/LLVM/bin/" | grep libclang` → shows `libclang.dll`
- Set `LIBCLANG_PATH="/c/Program Files/LLVM/bin"` during cargo runs.
- Note: setting `LIBCLANG_PATH` via `export` in bash may not propagate to cmake build scripts — use `.cargo/config.toml` `[env]` section for reliability.

## CMake

- The `cmake` Rust crate invokes `cmake` directly; it must be on PATH.
- Install: `winget install --id Kitware.CMake -e --accept-source-agreements --accept-package-agreements`
- Path: `C:\Program Files\CMake\bin`

## Ninja

- llama.cpp and other C++ dependencies use Ninja for parallel builds.
- Install: `winget install --id Ninja-build.Ninja -e --accept-source-agreements --accept-package-agreements`
- If not on PATH after install, download: `curl -L -o C:/Tools/ninja.exe https://github.com/ninja-build/ninja/releases/download/v1.12.1/ninja-win.zip`
- Path: `C:\Tools` (or wherever placed)

## Vulkan SDK

- Required for `llama-cpp-2/vulkan` feature.
- Download from `https://sdk.lunarg.com/sdk/download/latest/windows/vulkan-sdk.exe`
- Silent install: `./VulkanSDK-<version>-Installer.exe /S /D=C:\VulkanSDK\<version>`
- Verify: `ls "C:/VulkanSDK/<version>/Lib/cmake/"` contains `SPIRV-HeadersConfig.cmake`
- Set env vars: `VULKAN_SDK="C:/VulkanSDK/<version>"` and add `C:/VulkanSDK/<version>/Lib/cmake` to `CMAKE_PREFIX_PATH`

## Tauri Build Failures

- `Please install Vulkan SDK and ensure that VULKAN_SDK env variable is set` → install Vulkan SDK (see above)
- `Unable to find libclang` → install LLVM/Clang (see above)
- `Could not find a package configuration file provided by "SPIRV-Headers"` → add `C:/VulkanSDK/<version>/Lib/cmake` to `CMAKE_PREFIX_PATH`
- `ninja: error: loading 'build.ninja': The system cannot find the file specified` → stale build dir; delete `target` and `llama.cpp/build` dirs and rebuild
- `failed to execute command: program not found is cmake not installed?` → add CMake to PATH

## Cargo Errors Observed

- `error: failed to select a version for bson` → caused by duplicate `thiserror = "2"` in `[dependencies]`. Remove the duplicate.
- `the trait Copy cannot be implemented for this type` → `LocusId(String)` must not derive `Copy`.
- `cannot find type Store in this scope` → `wasmtime` does not always re-export `Store`, `Instance`, `Module`. Import explicitly.
- `unknown field tauri / package / allowlist` → `tauri-build` 2.6.3+ uses a different schema. Use only `productName`, `version`, `identifier`, `build`, `bundle`, `plugins`.
- `icons/icon.ico not found` → create a stub icon file or remove the icon array.
- `package.metadata does not exist` → remove `[package.metadata]`; Tauri 2 uses top-level keys only.
