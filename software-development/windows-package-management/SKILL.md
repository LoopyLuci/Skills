---
name: windows-package-management
description: "Use when installing software via winget, choco, or scoop."
category: software-development
tags: [windows, package-manager, winget, choco, scoop]
---
# Windows Package Management

Installing and managing software with winget, Chocolatey, and Scoop.

## winget (Built-in, Win 10+)

```powershell
# Search
winget search docker
winget search vscode

# Install
winget install -e --id Docker.DockerDesktop
winget install -e --id Microsoft.VisualStudioCode
winget install -e --id Microsoft.VisualStudio.2022.BuildTools

# List installed
winget list

# Upgrade
winget upgrade --all

# Uninstall
winget uninstall --id Docker.DockerDesktop

# Export/Import
winget export -o packages.json
winget import -i packages.json
```

## Chocolatey

```powershell
# Install choco
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Search
choco search docker

# Install
choco install docker-desktop -y
choco install vscode -y
choco install cmake --installargs '"ADD_CMAKE_TO_PATH=User"' -y

# Upgrade all
choco upgrade all -y

# Uninstall
choco uninstall docker-desktop -y

# List
choco list --local-only
```

## Scoop (Portable, no admin)

```powershell
# Install scoop
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
iex "& {$(irm get.scoop.sh)} -RunAsAdmin"

# Add buckets
scoop bucket add extras
scoop bucket add versions

# Search
scoop search docker

# Install
scoop install docker
scoop install vscode
scoop install cmake

# Update all
scoop update *
scoop update --all

# List installed
scoop list

# Uninstall
scoop uninstall docker
```

## Comparison

| Feature | winget | Chocolatey | Scoop |
|---------|--------|------------|-------|
| Built-in | Yes (Win10+) | No | No |
| Admin needed | Sometimes | Yes | No |
| Portable | No | No | Yes |
| Package count | ~6000 | ~10000 | ~5000 |
| Binary caching | No | Yes | Yes |

## Pitfalls

- **winget** sometimes has outdated versions -- use `--exact` or `--id` for specificity
- **Chocolatey** installs to Program Files -- needs admin by default
- **Scoop** installs to `~\scoop\apps` -- no admin needed, not in PATH by default
- **Mixing managers** can cause conflicts -- stick to one per tool
