---
name: windows-symbol-server
description: "Use when setting up debug symbol servers on Windows."
category: software-development
tags: [windows, symbols, debugging, pdb, windbg]
---
# Windows Symbol Server

Setting up debug symbol servers and configuring debuggers.

## Microsoft Public Symbol Server

```powershell
# For debugging Windows system code
$env:_NT_SYMBOL_PATH = "srv*C:\Symbols*https://msdl.microsoft.com/download/symbols"

# Make permanent (User)
[Environment]::SetEnvironmentVariable('_NT_SYMBOL_PATH',
    'srv*C:\Symbols*https://msdl.microsoft.com/download/symbols', 'User')
```

## Local Symbol Cache

```powershell
# Create local cache
New-Item -ItemType Directory -Path "C:\Symbols" -Force

# Pre-cache common symbols
# Run windbg or use symchk:
symchk /r c:\windows\system32\*.exe /s srv*C:\Symbols*https://msdl.microsoft.com/download/symbols
```

## Custom Symbol Server for Your App

```powershell
# During build, publish PDBs alongside binaries
# In CMake:
# set(CMAKE_CXX_FLAGS_DEBUG "/Zi /Fd${CMAKE_BINARY_DIR}/symbols/")
# set(CMAKE_CXX_FLAGS_RELEASE "/Zi /Fd${CMAKE_BINARY_DIR}/symbols/")

# After build, copy PDBs to symbol share
$symbolShare = "\\server\symbols"
Copy-Item "build\*.pdb" $symbolShare -Recurse

# Or use symstore (from Debugging Tools for Windows)
symstore add /r /f "build\*.pdb" /s "\\server\symbols" /t "MyApp" /v "1.0.0"
```

## Configure Debugger

```powershell
# WinDbg
# .sympath srv*C:\Symbols*https://msdl.microsoft.com/download/symbols;\\server\symbols
# .reload /f

# VS Code (launch.json)
# {
#   "symbolOptions": {
#     "searchPaths": ["C:\\Symbols", "\\\\server\\symbols"],
#     "searchMicrosoftSymbolServer": true
#   }
# }

# Visual Studio
# Tools → Options → Debugging → Symbols
# Add: \\server\symbols
# Check: Microsoft Symbol Servers
# Cache: C:\Symbols
```

## Debugging with Symbols

```powershell
# Check if symbols are loaded
# WinDbg: lm
# VS: Modules window

# Force symbol load
# WinDbg: .reload /f myapp.exe
# VS: Ctrl+Alt+U → Right-click module → Load Symbols

# Verify symbol matches binary
# chkmatc h:
chkmatch myapp.exe myapp.pdb
```

## Pitfalls

- PDB path embedded in binary during build -- if moved, symbols won't load
- Release builds with /Zi generate PDBs but no tracking -- use /DEBUG:FULL
- Symbol server needs write access for symstore
- Microsoft symbols are free but large (multi-GB cache over time)
- Public symbols don't have private information (line numbers, locals)
