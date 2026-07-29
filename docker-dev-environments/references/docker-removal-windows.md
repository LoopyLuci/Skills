# Docker Complete Removal — Windows Guide

## Overview

Removing Docker from a Windows system requires cleaning **seven independent layers** — the engine itself is only the beginning. Docker Desktop leaves traces in: WSL2 distributions, the Windows registry, environment variables (PATH + DOCKER_*), scheduled tasks, Windows services, multiple directory trees, and Windows optional features (Containers, VirtualMachinePlatform).

A production removal tool is at `D:\Projects\DockerManager\` — two PowerShell scripts (`DockerManager.ps1` v2.0 and `DockerManager-Ultra.ps1` v3.0) that automate every layer below with an interactive menu, restore points, and rollback.

---

## The 7 Layers of Docker

### Layer 1: Docker Engine Objects

Before removing binaries, purge the Docker objects:

```powershell
# Stop all running containers
docker stop $(docker ps -aq) 2>$null

# Remove everything
docker system prune -a -f --volumes

# Or phase by phase
docker rm -f $(docker ps -aq)        # containers
docker rmi -f $(docker images -q)     # images
docker volume rm $(docker volume ls -q) # volumes
docker network prune -f               # networks
```

### Layer 2: WSL2 Docker Distributions

Docker Desktop creates/manages WSL2 distros. Check and remove:

```powershell
# List all distributions
wsl --list --verbose

# Find Docker-managed ones (typically 'docker-desktop' and 'docker-desktop-data')
# Docker will recreate these on next launch, but for clean removal:

# 1. Backup first (creates .tar)
wsl --export docker-desktop C:\backups\docker-desktop.tar
wsl --export docker-desktop-data C:\backups\docker-desktop-data.tar

# 2. Unregister (irreversible without backup)
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data
```

**Warning**: unregistering WSL2 distros is permanent without an export backup.

### Layer 3: Windows Services

```powershell
$services = @('docker','docker-desktop','com.docker.service','Docker Desktop Service')
foreach ($svc in $services) {
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($s) {
        Stop-Service $s -Force
        Set-Service $s -StartupType Disabled
        Write-Host "Stopped/disabled: $svc"
    }
}
```

### Layer 4: Scheduled Tasks

```powershell
# Find Docker tasks
Get-ScheduledTask -TaskPath '\Microsoft\Windows\Docker\'

# Disable them
Disable-ScheduledTask -TaskName 'Docker Desktop Startup' -ErrorAction SilentlyContinue
Disable-ScheduledTask -TaskName 'Docker Desktop' -ErrorAction SilentlyContinue

# Or enumerate all Docker-named tasks
Get-ScheduledTask -TaskName '*Docker*' | Where-Object State -ne Disabled | 
    ForEach-Object { Disable-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath }
```

### Layer 5: File System — Directories to Remove

```powershell
$paths = @(
    "${env:ProgramFiles}\Docker",
    "${env:ProgramFiles(x86)}\Docker",
    "${env:ProgramData}\Docker",
    "${env:ProgramData}\DockerDesktop",
    "${env:LOCALAPPDATA}\Docker",
    "${env:APPDATA}\Docker",
    "${env:USERPROFILE}\.docker",
    "C:\Docker",
    "D:\Docker"
)

foreach ($p in $paths) {
    if (Test-Path $p) {
        try {
            Remove-Item $p -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "Removed: $p"
        } catch {
            Write-Host "Locked (needs reboot): $p"
        }
    }
}
```

Some files (e.g. `C:\ProgramData\DockerDesktop\pkg.db`, WSL VHDX files) may be locked until reboot.

### Layer 6: Registry Keys

```powershell
$regPaths = @(
    'HKLM:\SOFTWARE\Docker',
    'HKLM:\SOFTWARE\Docker Inc.',
    'HKCU:\SOFTWARE\Docker',
    'HKCU:\SOFTWARE\Docker Inc.',
    'HKLM:\SYSTEM\CurrentControlSet\Services\docker',
    'HKLM:\SYSTEM\CurrentControlSet\Services\com.docker.service'
)

foreach ($reg in $regPaths) {
    if (Test-Path $reg) {
        # Export before removing (backup / safety)
        reg export $reg ("$env:TEMP\docker_reg_backup.reg") /y 2>$null
        Remove-Item $reg -Recurse -Force -ErrorAction SilentlyContinue
    }
}
```

### Layer 7: Environment Variables

```powershell
# Docker-specific env vars
$dockerEnvVars = @('DOCKER_HOST','DOCKER_CERT_PATH','DOCKER_TLS_VERIFY',
                   'DOCKER_CONFIG','DOCKER_CONTEXT','DOCKER_API_VERSION',
                   'DOCKER_HIDE_LEGACY_COMMANDS')

foreach ($scope in @('User','Machine')) {
    $target = if ($scope -eq 'Machine') { [EnvironmentVariableTarget]::Machine } else { [EnvironmentVariableTarget]::User }
    
    # Clean PATH entries
    $pathVar = [Environment]::GetEnvironmentVariable('Path', $target)
    if ($pathVar -match '(?i)docker') {
        $newPath = ($pathVar -split ';' | Where-Object { $_ -notmatch '(?i)docker' }) -join ';'
        [Environment]::SetEnvironmentVariable('Path', $newPath, $target)
    }
    
    # Clean Docker vars
    foreach ($ev in $dockerEnvVars) {
        $val = [Environment]::GetEnvironmentVariable($ev, $target)
        if ($val) {
            [Environment]::SetEnvironmentVariable($ev, $null, $target)
        }
    }
}
```

### Bonus Layer: Windows Optional Features

Docker also enables these Windows features. Only disable if no other software uses them:

```powershell
# Check state
Get-WindowsOptionalFeature -Online -FeatureName 'Containers'
Get-WindowsOptionalFeature -Online -FeatureName 'Microsoft-Hyper-V'
Get-WindowsOptionalFeature -Online -FeatureName 'VirtualMachinePlatform'

# Disable (requires reboot)
Disable-WindowsOptionalFeature -Online -FeatureName 'Containers' -NoRestart
Disable-WindowsOptionalFeature -Online -FeatureName 'VirtualMachinePlatform' -NoRestart
```

---

## Complete Removal Checklist

- [ ] Back up WSL2 Docker distros (export to .tar)
- [ ] Stop + disable Docker services
- [ ] System prune all Docker objects
- [ ] Unregister WSL2 Docker distros
- [ ] Remove Docker scheduled tasks
- [ ] Delete Docker file system directories
- [ ] Remove Docker registry keys
- [ ] Clean Docker from PATH + env vars
- [ ] (Optional) Disable Containers / VirtualMachinePlatform features
- [ ] Reboot to release file locks
- [ ] Verify: `docker` command should produce "command not found"

---

## Automated Tooling

The **DockerManager** suite (`D:\Projects\DockerManager\`) automates every step above with:

| Script | Lines | Features |
|---|---|---|
| `DockerManager.ps1` | 1,313 | Interactive menu, all 7 layers, backup, reports |
| `DockerManager-Ultra.ps1` | 1,800 | Plus: restore points, rollback, parallel scan, smart analysis, env sanitizer, export/import plans, health dashboard |

### Quick Launch

```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File "D:\Projects\DockerManager\DockerManager.ps1"
powershell -ExecutionPolicy Bypass -File "D:\Projects\DockerManager\DockerManager-Ultra.ps1"
```

Or double-click the `.bat` launchers which auto-elevate to Administrator.

### Ultra Key Features

- **Restore Point Engine**: Creates automatic snapshots (files, registry, WSL2 .tar exports, services, env vars) before any destructive action. Keep up to 5 restore points.
- **Rollback**: Full reversal including WSL2 distro restoration from .tar, registry re-import, and env var recovery.
- **Smart Analysis**: Classifies every file as Safe-to-Delete, Needs-Backup, Locked-by-Process, or Large.
- **Environment Sanitizer**: Scans User/System PATH + all DOCKER_* variables and removes them.
- **Export/Import Plans**: Save scan results as JSON, reload on another machine.
- **Health Dashboard**: Live multi-pane view of engine, objects, WSL2, registry, services, and env vars.

---

## Key Differences from Linux

| Aspect | Windows | Linux |
|---|---|---|
| Docker engine | Runs in WSL2 VM | Native daemon |
| Default data dir | `C:\ProgramData\Docker` + WSL2 VHDX | `/var/lib/docker` |
| Install method | Docker Desktop GUI / winget | apt/yum/dnf |
| WSL2 footprint | 2 extra distros (`docker-desktop`, `docker-desktop-data`) | None |
| Service model | Windows service wrapping WSL2 process | systemd unit |
| Registry traces | HKLM + HKCU keys | No registry |
| PATH | User + System PATH variables | bashrc / profile |
| Locked files | Many files locked until reboot | Fewer locks |

---

## Common Pitfalls

- **`docker-desktop-data` WSL2 distro contains all images/volumes** — the VHDX file (`%LOCALAPPDATA%\Docker\wsl\data\ext4.vhdx`) can be 10-100+ GB and won't disappear until the WSL2 distro is unregistered or deleted.
- **`docker-desktop` service restarts automatically** if the WSL2 distro is still registered — unregister both `docker-desktop` AND `docker-desktop-data` together.
- **Registry keys require Admin** or they silently fail. Non-admin cleanup is incomplete.
- **Docker Desktop re-install detection**: Docker checks for leftover config files during install. Even a single `.docker/config.json` can trigger "previous installation detected" behavior.
- **WSL2 export time**: Large VHDX files can take 10+ minutes to export. Plan for that during backup.
- **Reboot requirement**: At least 3-4 files across `ProgramData`, `AppData`, and `LocalAppData` are locked while WSL2 or Docker Desktop processes run. Reboot is the only clean way.
