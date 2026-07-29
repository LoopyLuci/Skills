---
name: wsl2-ide-integration
description: "Use when connecting IDEs to WSL2 toolchains."
category: software-development
tags: [wsl2, ide, vscode, jetbrains, development]
---
# WSL2 IDE Integration

Connecting IDEs to WSL2 toolchains.

## VS Code Remote-WSL

```bash
# Inside WSL2
cd ~/project
code .

# Or from Windows
wsl -d Ubuntu -- code /home/user/project

# Install extensions in WSL2
code --install-extension rust-lang.rust-analyzer
code --install-extension ms-vscode.cpptools
```

## JetBrains IDEs (Gateway)

```powershell
# Install JetBrains Gateway on Windows
# Open Gateway → Connect to WSL
# It auto-detects WSL2 distros and installs IDE backend

# Or via toolbox:
# 1. Open JetBrains Toolbox
# 2. Click on IDE → Settings → Install on WSL
```

## Visual Studio (C++ via WSL2)

```powershell
# VS 2022 can target WSL2 for C++ builds
# Install: "Linux development with C++" workload
# Then add WSL2 as a target:
# Tools → Options → Cross Platform → Connection Manager → Add → WSL
```

## Remote Development Checklist

```powershell
# Inside WSL2, ensure tools are installed:
sudo apt-get update
sudo apt-get install -y build-essential cmake gdb
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## File Access

```bash
# IDE runs on Windows, opens files via \\wsl.localhost\
# Slow for large projects -- better to run IDE inside WSL2

# VS Code does this automatically with Remote-WSL
# The VS Code server runs IN WSL2, only the UI is on Windows

# Performance tip for JetBrains:
# Install IDE inside WSL2 and use WSLg to display
sudo apt-get install -y intellij-idea-community  # if available
# Or use JetBrains Gateway which runs the backend in WSL2
```

## Terminal Integration

```powershell
# Windows Terminal has built-in WSL2 profiles
# They appear automatically after distro installation

# Set default terminal to WSL2
# Windows Terminal → Settings → Default profile → Ubuntu

# Or from VS Code terminal
# Ctrl+Shift+P → "Terminal: Select Default Profile" → "Ubuntu (WSL)"
```

## Pitfalls

- VS Code Remote-WSL requires code-server installation inside WSL2 (auto-handled)
- Git line endings: set `git config core.autocrlf false` inside WSL2
- Extensions must be installed separately for WSL2 context
- JetBrains Gateway mounts project files via \\wsl.localhost\ -- slower than native WSL2
- WSLg lets GUI apps run, but GPU-accelerated IDEs need extra config
