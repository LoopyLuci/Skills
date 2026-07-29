---
name: msvc-toolchain
description: "Use when compiling with MSVC on Windows."
category: software-development
tags: [msvc, cpp, compiler, windows, visual-cpp]
---
# MSVC Toolchain

Using the MSVC compiler (cl.exe) and linker (link.exe) on Windows.

## Setup

```powershell
# From "x64 Native Tools Command Prompt for VS 2022":
# Or find the toolchain path:
$vcDir = & "${env:ProgramFiles}\Microsoft Visual Studio\Installer\vswhere.exe" -latest -property installationPath
$vcToolsDir = Join-Path $vcDir "VC\Tools\MSVC"
$latest = Get-ChildItem $vcToolsDir | Sort-Object Name -Descending | Select-Object -First 1
$env:Path = "$($latest.FullName)\bin\Hostx64\x64;$env:Path"
$env:INCLUDE = "$($latest.FullName)\include;$env:INCLUDE"
$env:LIB = "$($latest.FullName)\lib\x64;$env:LIB"
```

## Key Flags

```batch
cl.exe /c /O2 /arch:AVX2 /MD /std:c++20 /utf-8 /EHsc /Zi source.cpp

/O1      Optimize for size
/O2      Optimize for speed
/Od      No optimization (debug)
/arch:AVX2  Enable AVX2 instructions
/MD      Dynamic CRT (msvcr*.dll)
/MT      Static CRT (no redist needed)
/std:c++20  C++ standard version
/utf-8   Treat source as UTF-8
/EHsc    Enable C++ exceptions
/Zi      Generate PDB debug info
/Z7      Embed debug info in .obj
/GL      Whole program optimization
/LTCG    Link-time code generation
/W4      Warning level 4
/WX      Treat warnings as errors
/MP      Multi-process compilation
```

## Linking

```batch
REM Static lib
lib.exe /OUT:myapp.lib a.obj b.obj

REM DLL
link.exe /DLL /OUT:myapp.dll a.obj b.obj myapp.def

REM Executable
link.exe /OUT:myapp.exe a.obj b.obj /LIBPATH:C:\libs mylib.lib
```

## From CMake

```powershell
# MSVC with Ninja
cmake -B build -G Ninja `
    -DCMAKE_C_COMPILER=cl.exe -DCMAKE_CXX_COMPILER=cl.exe `
    -DCMAKE_BUILD_TYPE=Release

# Additional MSVC flags from CMake
cmake -B build -DCMAKE_CXX_FLAGS="/O2 /arch:AVX2 /utf-8 /EHsc"
```

## Common Errors

```powershell
# LNK2019: unresolved external -- missing library
# Fix: add library to linker input

# LNK2001: unresolved external symbol -- missing definition
# Fix: implement the declared function

# C1001: internal compiler error -- compiler bug
# Fix: simplify code, update VS, or use different optimization flag

# C4996: 'function' was declared deprecated
# Fix: define _CRT_SECURE_NO_WARNINGS
```

## Pitfalls

- **/MD** vs **/MT** -- all linked objects must use same CRT model
- **/clr** (C++/CLI) incompatible with some optimization flags
- **Precompiled headers** (/Yc /Yu) -- must match exactly between creation and use
- **PDB files** -- debug builds generate large PDBs; use /PDBALTPATH for reproducible builds
- **VS versions** -- major MSVC versions are not ABI-compatible
