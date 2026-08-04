---
name: docker-desktop-windows-removal
description: "Use when removing all Docker traces from Windows. 7-phase."
category: docker
tags: [docker, windows, cleanup, removal, wsl2, registry]
---

# Docker Desktop Windows Removal

Complete, production-grade removal of Docker Desktop and all Docker artifacts from a Windows system.

## When to Use

- Removing Docker Desktop completely from a Windows 10/11 machine
- Cleaning up after a failed Docker installation
- Reclaiming disk space from Docker images, volumes, and WSL2 distros
- Prepping a system for a fresh Docker install
- Removing all traces of Docker for security/auditing purposes

## Step-by-Step Removal Procedure

### Phase 1: Stop Docker Engine & Purge Objects

```powershell
docker stop $(docker ps -aq) 2>$null
docker rm -f $(docker ps -aq) 2>$null
docker rmi -f $(docker images -q) 2>$null
docker volume rm $(docker volume ls -q) 2>$null
docker system prune -a -f --volumes
```

### Phase 2: WSL2 Docker Distributions

```powershell
wsl --list --verbose
$backupDir = "$env:USERPROFILE\DockerWSLBackup"
New-Item -ItemType Directory -Path $backupDir -Force
wsl --export docker-desktop-data "$backupDir\docker-desktop-data.tar"
wsl --export docker-desktop "$backupDir\docker-desktop.tar"
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data
```

### Phase 3: Stop Windows Services

```powershell
$services = @('docker','docker-desktop','com.docker.service','Docker Desktop Service')
foreach ($svc in $services) {
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($s) { Stop-Service $s -Force; Set-Service $s -StartupType Disabled }
}
```

### Phase 4: Delete Docker Files

```powershell
$paths = @(
    "${env:ProgramFiles}\Docker","${env:ProgramFiles(x86)}\Docker",
    "${env:ProgramData}\Docker","${env:ProgramData}\DockerDesktop",
    "${env:LOCALAPPDATA}\Docker","${env:APPDATA}\Docker",
    "${env:USERPROFILE}\.docker"
)
foreach ($p in $paths) { if (Test-Path $p) { Remove-Item $p -Recurse -Force } }
```

### Phase 5: Clean Registry (Admin)

```powershell
$regPaths = @(
    'HKLM:\SOFTWARE\Docker','HKLM:\SOFTWARE\Docker Inc.',
    'HKCU:\SOFTWARE\Docker','HKCU:\SOFTWARE\Docker Inc.',
    'HKLM:\SYSTEM\CurrentControlSet\Services\docker',
    'HKLM:\SYSTEM\CurrentControlSet\Services\com.docker.service'
)
foreach ($rp in $regPaths) { if (Test-Path $rp) { Remove-Item $rp -Recurse -Force } }
```

### Phase 6: Clean Environment Variables

```powershell
foreach ($scope in @('User','Machine')) {
    $target = [EnvironmentVariableTarget]::$scope
    $p = [Environment]::GetEnvironmentVariable('Path', $target)
    $np = ($p -split ';' | Where-Object { $_ -notmatch '(?i)docker' }) -join ';'
    [Environment]::SetEnvironmentVariable('Path', $np, $target)
}
foreach ($ev in @('DOCKER_HOST','DOCKER_CERT_PATH','DOCKER_TLS_VERIFY','DOCKER_CONFIG','DOCKER_CONTEXT')) {
    foreach ($scope in @('User','Machine')) { [Environment]::SetEnvironmentVariable($ev, $null, $scope) }
}
```

### Phase 7: Disable Scheduled Tasks (Admin)

```powershell
Disable-ScheduledTask -TaskName 'Docker Desktop Startup' -ErrorAction SilentlyContinue
Disable-ScheduledTask -TaskName 'Docker Desktop' -ErrorAction SilentlyContinue
```

## Verification

```powershell
docker version 2>&1 | Select-String "not recognized"
@("${env:ProgramFiles}\Docker","${env:ProgramData}\Docker") | Where-Object { Test-Path $_ }
wsl --list --verbose 2>&1 | Select-String "docker" -SimpleMatch
Get-Service -Name docker* -ErrorAction SilentlyContinue
Test-Path 'HKLM:\SOFTWARE\Docker'
[Environment]::GetEnvironmentVariable('Path','User') -match '(?i)docker'
```

## Pitfalls

- **Reboot required** — Some file locks release only after reboot
- **Admin needed** — Service control, Machine PATH, HKLM registry require elevation
- **Encoding** — PS5 needs UTF-8 BOM for Unicode chars
- **$var: colon** — Use `-f` format operator to avoid PS7 parser errors
- **Capture returns** — `$null = FunctionCall` to prevent leaking objects
