---
name: cmake-windows-workflow
description: "Use when building C++ projects with CMake on Windows."
category: software-development
tags: [cmake, windows, cpp, build, msvc, clang]
---
# CMake on Windows Workflow

Building C++ projects with CMake on Windows (MSVC, Clang-CL, Ninja).

## Generators

```powershell
# List available generators
cmake --help

# Common Windows generators:
# - "Visual Studio 17 2022"    (MSBuild .sln/.vcxproj)
# - "Visual Studio 17 2022" -A Win64
# - "Visual Studio 17 2022" -A ARM64
# - "Ninja"                    (fast, no IDE)
# - "Ninja Multi-Config"       (Ninja with Debug/Release)
# - "MSYS Makefiles"           (git-bash/MinGW)
```

## Configure & Build

```powershell
# Ninja (recommended for speed)
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build

# Visual Studio
cmake -B build_msvc -G "Visual Studio 17 2022" -A x64
cmake --build build_msvc --config Release

# With Clang-CL (LLVM's MSVC-compatible frontend)
cmake -B build -G Ninja -DCMAKE_C_COMPILER=clang-cl -DCMAKE_CXX_COMPILER=clang-cl
cmake --build build
```

## CMakePresets.json

```json
{
  "version": 6,
  "configurePresets": [
    {
      "name": "default",
      "displayName": "Ninja Release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_CXX_COMPILER": "clang-cl",
        "CMAKE_C_COMPILER": "clang"
      }
    },
    {
      "name": "debug",
      "displayName": "Ninja Debug",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build_debug",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug" }
    },
    {
      "name": "msvc-release",
      "displayName": "MSVC Release",
      "generator": "Visual Studio 17 2022",
      "architecture": "x64",
      "binaryDir": "${sourceDir}/build_msvc",
      "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" }
    }
  ],
  "buildPresets": [
    { "name": "default", "configurePreset": "default" },
    { "name": "debug", "configurePreset": "debug" },
    { "name": "msvc-release", "configurePreset": "msvc-release" }
  ]
}
```

## Essential CMake Flags

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.20)
project(MyProject LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreadedDLL")

# Vulkan support
find_package(Vulkan REQUIRED)
target_link_libraries(myapp PRIVATE Vulkan::Vulkan)
```

## Common Flags by Compiler

```powershell
# MSVC
cmake -B build -DCMAKE_CXX_FLAGS="/O2 /arch:AVX2 /MD /utf-8"

# Clang-CL (MSVC compatible)
cmake -B build -DCMAKE_CXX_FLAGS="-O2 -mavx2 -D_CRT_SECURE_NO_WARNINGS"

# MinGW/GCC
cmake -B build -G "MinGW Makefiles" -DCMAKE_CXX_FLAGS="-O2 -mavx2"
```

## Debugging

```powershell
# Verbose make
cmake --build build --verbose

# Export compile commands (for clangd, IDEs)
cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

# See all detected settings
cmake -B build --trace-source=CMakeLists.txt
```

## Pitfalls

- **MSVC and Ninja** need `-DCMAKE_BUILD_TYPE=` explicitly; VS generator ignores it
- **Clang-CL** needs both `CMAKE_C_COMPILER=clang-cl` and `CMAKE_CXX_COMPILER=clang-cl`
- **Spaces in PATH** -- CMake handles quoted paths, but backslashes must be escaped
- **Windows SDK** required for MSVC -- install via "Visual Studio Build Tools" workload
- **`/MD` vs `/MT`** -- /MD uses dynamic CRT (smaller, needs redistributable); /MT is static
