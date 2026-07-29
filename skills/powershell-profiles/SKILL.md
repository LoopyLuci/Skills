---
name: powershell-profiles
description: "Use when customizing PowerShell profile scripts."
category: software-development
tags: [powershell, profile, customization, prompt, aliases]
---
# PowerShell Profiles

Customizing PowerShell startup profiles.

## Profile Locations

```powershell
# Check which profiles exist
$PROFILE | Get-Member -MemberType NoteProperty | Select-Object Name

# Profile paths:
$PROFILE.AllUsersAllHosts   # All users, all hosts
$PROFILE.AllUsersCurrentHost # All users, current host
$PROFILE.CurrentUserAllHosts # Current user, all hosts
$PROFILE.CurrentUserCurrentHost # Current user, current host (most common)
```

## Typical Profile Structure

```powershell
# ~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
# ~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1 (PS5)

# ── Appearance ───────────────────────────────────────────
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\cloud-native-azure.omp.json" | Invoke-Expression

# ── Aliases ──────────────────────────────────────────────
Set-Alias g git
Set-Alias ll Get-ChildItem
Set-Alias dc docker compose
Set-Alias dps "docker ps"
New-Alias -Name which -Value Get-Command

# ── Functions ────────────────────────────────────────────
function .. { Set-Location .. }
function ... { Set-Location ..\.. }
function grep { $args | Select-String -Pattern $args[0] }
function mkcd { New-Item -ItemType Directory -Path $args[0] -Force; Set-Location $args[0] }
function touch { New-Item -ItemType File -Path $args[0] -Force }

# ── Prompt Customization ─────────────────────────────────
function prompt {
    $path = (Get-Location).Path.Replace($HOME, '~')
    "$path> "
}

# ── Startup Banner ──────────────────────────────────────
$host.UI.RawUI.WindowTitle = "PowerShell $($PSVersionTable.PSVersion)"
Write-Host "Profile loaded. $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan
```

## Module Auto-Loading

```powershell
# Modules to import at startup
$modules = @('DockerCompletion', 'PSReadLine', 'Terminal-Icons')
foreach ($m in $modules) {
    if (Get-Module -ListAvailable -Name $m) {
        Import-Module $m -ErrorAction SilentlyContinue
    }
}

# PSReadLine configuration
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -Colors @{ Command = 'Yellow'; String = 'Green' }
Set-PSReadLineKeyHandler -Key Ctrl+SpaceBar -Function MenuComplete
```

## Environment Variables

```powershell
# Docker
$env:DOCKER_HOST = "tcp://localhost:2375"
$env:DOCKER_BUILDKIT = "1"
$env:COMPOSE_DOCKER_CLI_BUILD = "1"

# Path additions
$userPaths = @(
    "$env:USERPROFILE\.cargo\bin",
    "$env:USERPROFILE\AppData\Local\Programs\Microsoft VS Code\bin"
)
foreach ($p in $userPaths) {
    if (Test-Path $p -and $env:Path -notlike "*$p*") {
        $env:Path = "$p;$env:Path"
    }
}
```

## Conditional Loading

```powershell
# Only load if module is available
if (Get-Command starship -ErrorAction SilentlyContinue) {
    Invoke-Expression (&starship init powershell)
}

# Only on certain hosts
if ($host.Name -eq 'ConsoleHost') {
    Import-Module PSReadLine
}

# Conditional by OS
if ($IsWindows) {
    Import-Module DockerCompletion
}
```

## Pitfalls

- Profile runs on EVERY PowerShell startup -- keep it fast (<100ms)
- Errors in profile prevent the rest from loading -- use try/catch
- Different profiles for PS5 (WindowsPowerShell) and PS7 (PowerShell)
- Dot-source profile changes with `. $PROFILE` without restarting
- Profile scripts are plain text -- don't store credentials in them
