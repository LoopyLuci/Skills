---
name: wsl2-distro-management
description: "Use when managing WSL2 distributions: import, export, backup."
category: software-development
tags: [wsl2, linux, distro, windows, backup]
---
# WSL2 Distro Management

Managing WSL2 distributions: import, export, register, unregister, backup.

## Basic Commands

```powershell
# List all distros with status
wsl --list --verbose

# Set default version (1 or 2)
wsl --set-default-version 2

# Set default distro
wsl --set-default Ubuntu

# Run a command in a specific distro
wsl -d Ubuntu -- ls -la

# Terminate a distro
wsl --terminate Ubuntu

# Shutdown all WSL2
wsl --shutdown

# Check WSL2 status
wsl --status
```

## Export / Import (Full Backup)

```powershell
# Export distro to tar file
$backupDir = "C:\WSLBackups"
New-Item -ItemType Directory -Path $backupDir -Force
wsl --export Ubuntu "$backupDir\Ubuntu_$(Get-Date -Format yyyyMMdd).tar"

# Import distro from tar
wsl --import MyUbuntu "C:\WSL\MyUbuntu" "$backupDir\Ubuntu_20240101.tar" --version 2

# Import with specific name and path
wsl --import DockerDesktop "C:\ProgramData\Docker\wsl" docker-desktop.tar --version 2
```

## Clone a Distro

```powershell
# Export existing
wsl --export Ubuntu "$env:TEMP\clone.tar"
# Import as new
wsl --import Ubuntu-Dev "C:\WSL\Ubuntu-Dev" "$env:TEMP\clone.tar" --version 2
# Cleanup temp
Remove-Item "$env:TEMP\clone.tar"
```

## Unregister (Delete Entire Distro)

```powershell
# WARNING: This PERMANENTLY DELETES all data in the distro
wsl --unregister Ubuntu
```

## Manual Distro Registration

```powershell
# You can download and import any Linux distro .tar:
# 1. Download from official sources (Alpine, Ubuntu, Debian, etc.)
# 2. Import with custom name
wsl --import Alpine "C:\WSL\Alpine" "C:\Downloads\alpine.tar" --version 2
```

## Set Distribution as Docker Backend

```powershell
# Docker Desktop uses two internal distros
# These are managed by Docker Desktop -- don't modify directly
wsl --list --verbose | Select-String docker

# Restart Docker WSL2 distros:
# Docker Desktop > Troubleshoot > Restart Docker Desktop
# Or:
wsl --terminate docker-desktop
# Docker Desktop auto-restarts it
```

## Pitfalls

- **wsl --shutdown** terminates all WSL2 distros, including Docker
- **Export** creates large files (multi-GB for Docker data distros)
- **Import** path is the install location, not the tar file path
- **Version 1 to 2 conversion** can take time for large distros
- **VHDX files** grow over time but rarely shrink -- compact with `diskpart` or wsl --shutdown + Optimize-VHD
