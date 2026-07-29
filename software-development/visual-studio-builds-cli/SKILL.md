---
name: visual-studio-builds-cli
description: "Use when building VS solutions from command line."
category: software-development
tags: [visual-studio, msbuild, cli, build, automation]
---
# Visual Studio Builds CLI

Building Visual Studio solutions and projects from command line.

## MSBuild

```powershell
# Find MSBuild path
$vsPath = & "${env:ProgramFiles}\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.Component.MSBuild -property installationPath
$msbuild = Join-Path $vsPath "MSBuild\Current\Bin\MSBuild.exe"

# Build solution
& $msbuild MyApp.sln /p:Configuration=Release /p:Platform=x64

# Build specific project
& $msbuild src\MyApp.vcxproj /p:Configuration=Debug /p:Platform=x64

# With verbosity
& $msbuild MyApp.sln /v:minimal           # errors only
& $msbuild MyApp.sln /v:normal            # default
& $msbuild MyApp.sln /v:detailed          # verbose
& $msbuild MyApp.sln /v:diag              # everything

# Clean
& $msbuild MyApp.sln /t:Clean
& $msbuild MyApp.sln /t:Rebuild

# Parallel build
& $msbuild MyApp.sln /m                   # use all cores
& $msbuild MyApp.sln /m:4                 # use 4 cores
```

## devenv.exe

```powershell
# Find devenv
$devenv = Join-Path $vsPath "Common7\IDE\devenv.exe"

# Build
& $devenv MyApp.sln /Build Release /Project MyApp

# Build and deploy
& $devenv MyApp.sln /Build Release /Deploy

# Upgrade solution format
& $devenv MyApp.sln /Upgrade

# Open in VS (for CI purposes)
& $devenv MyApp.sln /Edit
```

## cmake --build

```powershell
# When using CMake with VS generator
cmake -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
cmake --build build --config Release --target MyApp
cmake --build build --config Release --clean-first
cmake --build build --config Release --verbose
```

## Common Properties

```powershell
/p:Configuration=Release        # Debug / Release / RelWithDebInfo
/p:Platform=x64                 # x86 / x64 / ARM64 / Any CPU
/p:PlatformToolset=v143         # v143=VS2022, v142=VS2019
/p:WindowsTargetPlatformVersion=10.0
/p:OutDir=C:\BuildOutput\
/p:IntermediateOutputPath=C:\Build\obj\
/p:UseEnv=true                  # use environment PATH
```

## CI Integration

```powershell
# Check build result
& $msbuild MyApp.sln /p:Configuration=Release
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

# Test
& vstest.console.exe build\Release\MyApp.Tests.dll
```

## Pitfalls

- MSBuild needs Developer Command Prompt environment -- use vcvars64.bat
- vswhere finds the latest VS installation
- Parallel builds (/m) may fail with certain project dependencies
- OutDir must end with backslash on MSBuild command line
- C++ projects need /p:PlatformToolset matching installed VS
