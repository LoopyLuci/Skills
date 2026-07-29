---
name: powershell-windows-scripts
description: 'PowerShell script patterns: admin, encoding, launchers.'
category: software-development
tags:
  - powershell
  - windows
  - scripting
  - interactive-console
  - admin-elevation
  - encoding
version: 1.0.0
---

# PowerShell Windows Scripts

Production-grade patterns for building interactive PowerShell scripts on Windows.

## Trigger

Use when building, debugging, or fixing a PowerShell script that:
- Runs as an interactive console tool (menu-driven)
- Requires Administrator elevation
- Uses Unicode characters
- Ships with a `.bat` launcher
- Manages Windows services, registry, WSL2, or environment variables

## Patterns

### 1. Admin Elevation — NO `#Requires -RunAsAdministrator`

```powershell
# BAD — silent exit on non-admin:
#Requires -RunAsAdministrator

# GOOD — runtime check:
if (-not (Test-IsAdmin)) {
    Write-Host "WARNING: Not running as Administrator." -ForegroundColor Yellow
    if (-not (Confirm-Action "Continue anyway?" 'N')) { exit 1 }
}
```

### 2. UTF-8 BOM (Critical for PS 5.1)

Windows PowerShell 5.1 reads UTF-8 without BOM as ANSI, corrupting multi-byte characters.

- Save `.ps1` files with **UTF-8 BOM** (`utf-8-sig` in Python)
- OR strip all non-ASCII characters to ASCII equivalents
- PowerShell Core 7+ handles BOM-less UTF-8 fine

```python
with open('script.ps1', 'w', encoding='utf-8-sig') as f:
    f.write(content)
```

### 3. Batch Launcher (with -NoExit)

```batch
@echo off
set "PS_SCRIPT=%~dp0MyScript.ps1"
net session >nul 2>&1
if %errorlevel% neq 0 (
    PowerShell -NoProfile -ExecutionPolicy Bypass ^
        -Command "Start-Process PowerShell -Verb RunAs ^
            -ArgumentList '-NoExit -File \"%PS_SCRIPT%\"'"
) else (
    PowerShell -NoProfile -ExecutionPolicy Bypass -NoExit -File "%PS_SCRIPT%"
)
pause
```

**Always use `-NoExit`** so errors stay visible.

### 4. String Interpolation — `$var:` Pitfall

```powershell
# BAD — parser reads $svc: as scope reference
$svcLines += " $svc: $($s.Status)"

# GOOD
$svcLines += " ${svc}: $($s.Status)"

# Also good
$svcLines += "{0}: {1}" -f $svc, $s.Status
```

### 5. Console UI Patterns

Single-key menu: `$Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')`
Color palette in `$Script:Colors` global hashtable
Auto-width tables with alternate row colors
Progress bars via `Write-Progress`

### 6. Mixed-Context Error Handling

```powershell
function Confirm-Action {
    param([string]$Message, [string]$Default = 'N')
    try { $r = Read-Host; if (-not $r) { return $Default -eq 'Y' }; return $r -match '^[yY]' }
    catch { return $Default -eq 'Y' }
}
```

## Pitfall Quick-Reference

| Pitfall | Symptom | Fix |
|---|---|---|
| `#Requires -RunAsAdministrator` | Silent exit without admin | Runtime check |
| No UTF-8 BOM in PS5.1 | Unicode chars corrupt | BOM or strip |
| Missing `-NoExit` in launcher | Window closes on error | Add `-NoExit` |
| `$var:` in strings | Parse error | `${var}:` or `-f` |
| `"$var: $_"` in catch | Parse error | `-f` operator |
| `Read-Host` non-interactive | Script hangs | try/catch default |
| **Return value leaked to stdout** | Raw path/variable appears in console | `$null = FunctionCall` |
| **Machine env var without admin** | Crash on SetEnvironmentVariable | try/catch with graceful fallback |
| **Menu action crashes** | Entire script exits | Per-action try/catch, do/while loop |
| **No ReadKey in finally** | Window closes instantly | Add ReadKey in finally block |

## Patterns (cont.)

### 7. Function Return Value Leakage

When a function returns a value and is called as a standalone statement, the return value is emitted to stdout and appears on the console as raw output.

```powershell
# BAD - leaks $rpDir path to console:
New-RestorePoint -Label "Pre-Cleanup"

# GOOD - capture or discard:
$null = New-RestorePoint -Label "Pre-Cleanup"
```

### 8. Admin-Sensitive Operations - Always try/catch

Setting Machine-scope environment variables, modifying registry, and stopping services require admin. Always wrap these in try/catch so one failure does not crash the entire script:

```powershell
try {
    [Environment]::SetEnvironmentVariable('Path', $newPath, [EnvironmentVariableTarget]::Machine)
    Write-Host "  OK Updated Machine PATH"
} catch {
    Write-Host "  FAIL Cannot modify Machine PATH - need admin" -ForegroundColor Yellow
    Write-Log "WARN" "Failed to update Machine PATH: $_"
}
```

### 9. Restore Point Snapshot Pattern

Before destructive operations, create a snapshot that can be rolled back:

```powershell
function New-RestorePoint {
    param([string]$Label)
    $id = [Guid]::NewGuid().ToString().Substring(0, 8)
    $ts = Get-Date -Format 'yyyyMMdd_HHmmss'
    $rpDir = Join-Path $Script:RestorePath "RP_${ts}_${id}"
    New-Item -ItemType Directory -Path $rpDir -Force | Out-Null
    $manifest = @{
        Id = $id; Timestamp = (Get-Date -Format 'o'); Label = $Label
        Files = @(); Registry = @(); Services = @()
        WSL2Distros = @(); EnvVars = @()
    }
    # Snapshot file metadata, export registry keys, export WSL2 distros as tar
    $manifest | ConvertTo-Json -Depth 5 | Out-File (Join-Path $rpDir 'manifest.json')
    Write-Host "  OK Restore point: RP_${ts}_${id}" -ForegroundColor Green
    # Keep last 5 restore points
    $all = @(Get-ChildItem $Script:RestorePath -Directory | Sort-Object Name -Descending)
    if ($all.Count -gt 5) { $all[5..($all.Count-1)] | Remove-Item -Recurse -Force }
    return $rpDir  # CALLER MUST CAPTURE WITH $null =
}
```

### 10. finally Block - Window-Stay-Open Pattern

Always keep the window open after script exit regardless of how it ended:

```powershell
try {
    # main logic
}
catch {
    Write-Host "FATAL: $_" -ForegroundColor Red
    Pause-Script
}
finally {
    try { Stop-Transcript -ErrorAction SilentlyContinue } catch {}
    Write-Host "`n  Script ended. Press any key to close this window..." -ForegroundColor DarkGray
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
}
```

This ensures right-click to Run with PowerShell users see the exit message instead of a blank flash.

### 11. Menu Action Resilience

Wrap each interactive menu action so one failure does not exit the entire script:

```powershell
do {
    $choice = Show-Menu -Items $items
    switch ($choice) {
        'risky-action' {
            try {
                # potentially failing operation
            } catch {
                Write-Host "  FAIL: $_" -ForegroundColor Red
            }
        }
    }
} while ($true)
```

### 12. Auto-Elevation Engine (Self-Calling Admin Pattern)

For operations requiring admin, instead of crashing or asking user to relaunch, spawn an elevated child process that runs only the specific admin action:

```powershell
# ── Script entry point ────────────────────────────────────────────
param([string]$AdminAction = '')

# If launched with -AdminAction, run that action and exit (elevated child mode)
if ($AdminAction) {
    Initialize-Environment
    $success = Invoke-AdminAction -Action $AdminAction
    Write-Host "`n  Script ended. Press any key to close this window..."
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    exit 0
}

# ── Normal interactive mode ───────────────────────────────────────
# ... show menu ...

# ── Invoke-Elevated: the elevation dispatcher ─────────────────────
function Invoke-Elevated {
    param([string]$Action, [string]$Description)

    # Already admin? Run directly
    if (Test-IsAdmin) { return Invoke-AdminAction -Action $Action }

    Write-Host "  [ADMIN REQUIRED] $Description"
    Write-Host "  Requesting Administrator privileges..."

    # Find this script's own path
    $scriptPath = $MyInvocation.MyCommand.Path
    if (-not (Test-Path $scriptPath)) {
        $scriptPath = "$PSScriptRoot\MyScript.ps1"
    }

    # Relaunch as admin with -AdminAction
    $psExe = 'powershell.exe'  # or 'pwsh.exe' for PS Core
    Start-Process -FilePath $psExe -Verb RunAs -ArgumentList @(
        '-NoProfile', '-ExecutionPolicy', 'Bypass',
        '-File', "`"$scriptPath`"",
        '-AdminAction', $Action
    ) -Wait:$Wait

    Write-Host "  Admin operation completed.`n"
}

# ── Invoke-AdminAction: runs inside the elevated child ─────────────
function Invoke-AdminAction {
    param([string]$Action)
    switch ($Action) {
        'Registry-Cleanup' {
            Remove-Item 'HKLM:\SOFTWARE\Docker' -Recurse -Force -ErrorAction SilentlyContinue
        }
        'Services-Stop' {
            Stop-Service 'docker' -Force -ErrorAction SilentlyContinue
            Set-Service 'docker' -StartupType Disabled -ErrorAction SilentlyContinue
        }
    }
}
```

**Key constraints:**
- The `param()` block MUST be before any `#Requires` or code
- The script path must be resolved via `$MyInvocation.MyCommand.Path` or `$PSScriptRoot`
- Admin actions must be self-contained (they run in a fresh process with no variable state)
- Use `Start-Process -ArgumentList @(array)` to avoid PowerShell quoting nightmares
- Always return `exit 0` after the admin action so the child window shows the message

### 13. Multi-Phase Operation Pattern

For complex destructive workflows (like full Docker removal), use a phased approach where each phase handles its own errors and recovery:

```powershell
function Invoke-CompleteRemoval {
    param([switch]$DryRun)
    Write-Host ">>> Phase 1/7: Engine Cleanup <<<"
    Stop-DockerContainers
    Remove-DockerEnvironment -Containers -Images -Volumes -System -Force

    Write-Host ">>> Phase 2/7: WSL2 Distros <<<"
    Backup-WSL2Distro
    foreach ($d in Get-WSL2DockerDistros) { wsl --unregister $d.Name }

    Write-Host ">>> Phase 3/7: File Scan <<<"
    $scan = Scan-DockerFiles -Force

    Write-Host ">>> Phase 4/7: Services <<<"
    Invoke-Elevated -Action "Services-Stop"

    Write-Host ">>> Phase 5/7: File Deletion <<<"
    foreach ($d in $knownPaths) { Remove-Item $d -Recurse -Force }

    Write-Host ">>> Phase 6/7: Registry <<<"
    Invoke-Elevated -Action "Registry-Cleanup"

    Write-Host ">>> Phase 7/7: Report <<<"
    New-DockerReport -SaveToFile
}
```

**Four pillars of phase resilience:**
1. Each phase has its own try/catch (no cascade)
2. Admin phases use `Invoke-Elevated` (not inline env calls)
3. Dry-run mode skips all execution but shows what would happen
4. A restore point is created before phase 1

### 14. Dual-Format Logging

Log to both plain text (human-readable) and JSONL (machine-parseable) simultaneously:

```powershell
$Script:LogFile     = Join-Path $LogPath "session_$(Get-Date -Format 'yyyyMMdd').log"
$Script:JsonLogFile = Join-Path $LogPath "session_$(Get-Date -Format 'yyyyMMdd').jsonl"

function Write-Log {
    param([string]$Level, [string]$Message, [hashtable]$Data = @{})
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff'
    $textEntry = "[$timestamp] [$Level] $Message"

    # Console
    $color = switch ($Level) { 'ERROR' { Red } 'WARN' { Yellow } default { White } }
    Write-Host $textEntry -ForegroundColor $color

    # Plain text file
    Add-Content -Path $Script:LogFile -Value $textEntry -Encoding UTF8

    # JSONL file
    $jsonEntry = @{ Timestamp=$timestamp; Level=$Level; Message=$Message }
    if ($Data.Count -gt 0) { $jsonEntry.Data = $Data }
    Add-Content -Path $Script:JsonLogFile -Value ($jsonEntry | ConvertTo-Json -Compress)
}
```

### 15. Configuration Persistence

Save and load user preferences as JSON:

```powershell
# Load on startup
if (Test-Path $Script:ConfigFile) {
    $loaded = Get-Content $Script:ConfigFile -Raw | ConvertFrom-Json
    foreach ($prop in $loaded.PSObject.Properties) {
        if ($Script:UltraConfig.ContainsKey($prop.Name)) {
            $Script:UltraConfig[$prop.Name] = $prop.Value
        }
    }
}

# Save on quit or before admin elevation
Save-UltraConfig  # ConvertTo-Json | Out-File
```

## References

- `references/powershell-encoding-pitfalls.md` — detailed encoding edge cases
- `references/dockermanager-architecture.md` — 1800-line interactive tool example
- `references/environment-variable-safety.md` — Machine vs User scope patterns
- `references/auto-elevation-engine.md` — full Invoke-Elevated pattern with error handling
