---
name: windows-dev-environment-setup
description: "Use when provisioning a Windows dev machine via script."
category: software-development
tags: [windows, dev-environment, provisioning, setup, automation]
---
# Windows Dev Environment Setup

One-script provisioning of a Windows development machine.

## One-Click Setup Script

```powershell
# save as setup-dev.ps1 and run as admin
$ErrorActionPreference = 'Stop'

function Install-WithWinget {
    param([string]$Id, [string]$Name)
    Write-Host "Installing $Name..."
    winget install -e --id $Id --accept-source-agreements --accept-package-agreements 2>$null
}

# Essentials
Install-WithWinget "Git.Git" "Git"
Install-WithWinget "Microsoft.VisualStudioCode" "VS Code"
Install-WithWinget "Microsoft.PowerShell" "PowerShell 7"

# Browsers
Install-WithWinget "Google.Chrome" "Chrome"
Install-WithWinget "Mozilla.Firefox" "Firefox"

# Dev Tools
Install-WithWinget "Docker.DockerDesktop" "Docker Desktop"
Install-WithWinget "Microsoft.VisualStudio.2022.BuildTools" "VS Build Tools"
Install-WithWinget "Kitware.CMake" "CMake"
Install-WithWinget "LLVM.LLVM" "LLVM/Clang"

# Install Rust via rustup
if (-not (Get-Command rustup -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Rust..."
    # rustup-init downloads
    $url = "https://win.rustup.rs/x86_64"
    $installer = "$env:TEMP\rustup-init.exe"
    Invoke-WebRequest -Uri $url -OutFile $installer
    Start-Process -FilePath $installer -ArgumentList "-y --default-toolchain stable --profile default" -Wait
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
}

# Add Rust targets
rustup target add x86_64-pc-windows-msvc
rustup target add aarch64-pc-windows-msvc

# Install Vulkan SDK
Install-WithWinget "KhronosGroup.VulkanSDK" "Vulkan SDK"

# Python (for scripting)
Install-WithWinget "Python.Python.3.12" "Python 3.12"

# Terminal
Install-WithWinget "Microsoft.WindowsTerminal" "Windows Terminal"
```

## Chocolatey Alternative

```powershell
# If winget is unavailable, use Chocolatey:
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

choco install -y git vscode pwsh docker-desktop cmake llvm rust vulkan-sdk python
```

## Post-Install Config

```powershell
# Git config
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.autocrlf true

# VS Code extensions
code --install-extension rust-lang.rust-analyzer
code --install-extension ms-vscode.cpptools-extension-pack
code --install-extension ms-azuretools.vscode-docker

# Enable WSL2 (admin)
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
wsl --set-default-version 2
```

## Verify Installation

```powershell
Write-Host "=== Verification ==="
git --version
cmake --version | Select-Object -First 1
rustc --version
cargo --version
python --version
code --version | Select-Object -First 1
pwsh --version
docker --version 2>$null
vulkaninfo --version 2>$null
```

## Pitfalls

- **winget** may need `--accept-source-agreements` for non-interactive use
- **VS Build Tools** needs reboot; workload selection in VS installer
- **Rust** needs `x86_64-pc-windows-msvc` as default; the `-gnu` target is an alternative
- **Vulkan SDK** automatically adds VK_LAYER_PATH -- check after install
- **WSL2** requires reboot after enabling VirtualMachinePlatform feature
