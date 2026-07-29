---
name: wsl2-multiple-distros
description: "Use when managing multiple WSL2 distributions."
category: software-development
tags: [wsl2, distros, multiple, management]
---
# WSL2 Multiple Distributions

Managing multiple WSL2 distributions effectively.

## Install Multiple Distros

```powershell
# Via Microsoft Store (manual)
# Or via command line:
wsl --install -d Ubuntu
wsl --install -d Debian
wsl --install -d kali-linux
wsl --install -d Alpine

# Via direct import
wsl --import Ubuntu-22.04 "C:\WSL\Ubuntu-22.04" ubuntu-22.04.tar --version 2
```

## Set Default Distro

```powershell
wsl --set-default Ubuntu-Dev
wsl --list --verbose
# Default is marked with *
```

## Run Commands on Specific Distro

```powershell
wsl -d Ubuntu-Dev -- docker ps
wsl -d Debian -- apt-get update
wsl -d Alpine -- apk add python3
```

## Distro-Specific Config

```ini
# %USERPROFILE%\.wslconfig applies to ALL distros
# Per-distro config in /etc/wsl.conf inside each distro

# Example: Different memory for different distros
# .wslconfig only has global settings
# For per-distro limits, consider resource-constrained wsl.conf
```

## Moving Distro Install Location

```powershell
# Export and re-import to new location
wsl --export Ubuntu-Dev "C:\backup\ubuntu-dev.tar"
wsl --unregister Ubuntu-Dev
wsl --import Ubuntu-Dev "D:\WSL\Ubuntu-Dev" "C:\backup\ubuntu-dev.tar" --version 2
Remove-Item "C:\backup\ubuntu-dev.tar"
```

## Cloning a Distro

```powershell
# Export source
wsl --export Ubuntu-Source "$env:TEMP\clone.tar"

# Import as new
wsl --import Ubuntu-Clone "C:\WSL\Ubuntu-Clone" "$env:TEMP\clone.tar" --version 2
wsl -d Ubuntu-Clone -- ls

# Customize clone
wsl -d Ubuntu-Clone
sudo hostnamectl set-hostname clone-machine
```

## Pitfalls

- All distros share the same .wslconfig settings
- Each distro has its own VHDX file for its filesystem
- Distro names are case-sensitive in wsl commands
- Unregistering a distro irreversibly deletes its data
- Docker Desktop uses its own internal distros (docker-desktop, docker-desktop-data)
