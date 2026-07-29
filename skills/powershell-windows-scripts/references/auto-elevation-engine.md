# Auto-Elevation Engine — Full Pattern Reference

The self-calling admin elevation pattern for PowerShell scripts, as implemented in DockerManager-Ultra.ps1 (1800 lines, ~105 KB).

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      MAIN PROCESS (User)                        │
│                                                                  │
│  Launch via double-click or "Run with PowerShell 7"              │
│                                                                  │
│  [A] Auto-elevate → Start-Process -Verb RunAs of same script     │
│  [C] Continue → run unprivileged, elevate per-operation          │
│                                                                  │
│  When admin action needed:                                       │
│    Invoke-Elevated -Action "Registry-Cleanup"                   │
│      ↓                                                          │
│    Start-Process pwsh.exe -Verb RunAs -ArgumentList @(           │
│      '-File', "script.ps1", '-AdminAction', 'Registry-Cleanup'   │
│    )                                                             │
└──────────────────────────────────────────────────────────────────┘
         │
         ▼  (UAC prompt → elevated process spawned)
┌──────────────────────────────────────────────────────────────────┐
│                     CHILD PROCESS (Admin)                        │
│                                                                  │
│  param([string]$AdminAction = 'Registry-Cleanup')                │
│                                                                  │
│  if ($AdminAction) {                                             │
│    Initialize-Environment                                        │
│    Invoke-AdminAction -Action $AdminAction                       │
│    Write-Host "Press any key to close..."                        │
│    exit 0                                                        │
│  }                                                               │
└──────────────────────────────────────────────────────────────────┘
```

## Implementation Details

### 1. Parameter Block (MUST be before all code)

```powershell
param(
    [string]$AdminAction = ''
)

#Requires -Version 5.1
# ... (rest of script)
```

### 2. Entry Point — Branch on AdminAction

```powershell
try {
    # Admin-action mode (elevated child process)
    if ($AdminAction) {
        Initialize-Environment
        Write-Host "  ADMIN OPERATION: $AdminAction"
        $success = Invoke-AdminAction -Action $AdminAction
        Write-Host "  Script ended. Press any key to close this window..."
        $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
        exit 0
    }

    # Interactive mode
    Initialize-Environment
    if (-not (Test-IsAdmin)) {
        Show-ElevationPrompt  # [A]uto-elevate, [C]ontinue, [N]o
    }
    Show-MainMenu
}
```

### 3. Invoke-Elevated (the dispatcher)

```powershell
function Invoke-Elevated {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Action,
        [switch]$Wait = $true,
        [string]$Description = ""
    )

    # Already admin — run directly
    if (Test-IsAdmin) {
        return Invoke-AdminAction -Action $Action
    }

    Write-Host "  [ADMIN REQUIRED] $Description"
    Write-Host "  Requesting Administrator privileges..."

    # Resolve script path using multiple fallbacks
    $scriptPath = $Script:MyInvocation.MyCommand.Path
    if (-not $scriptPath -or -not (Test-Path $scriptPath)) {
        $scriptPath = $MyInvocation.MyCommand.Path
    }
    if (-not $scriptPath -or -not (Test-Path $scriptPath)) {
        $scriptPath = "$PSScriptRoot\MyScript.ps1"
    }
    if (-not (Test-Path $scriptPath)) {
        $scriptPath = "C:\Full\Path\MyScript.ps1"  # last resort hardcode
    }

    $psExe = if ($Script:IsPSCore) { 'pwsh.exe' } else { 'powershell.exe' }

    try {
        $proc = Start-Process -FilePath $psExe -Verb RunAs -ArgumentList @(
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-File', "`"$scriptPath`"",
            '-AdminAction', $Action
        ) -PassThru -WindowStyle Normal -Wait:$Wait

        if ($Wait) {
            $proc.WaitForExit()
            return $proc.ExitCode -eq 0
        }
        return $true
    }
    catch {
        Write-Host "  FAILED: $_" -ForegroundColor Yellow
        Write-Host "  Try running the script as Administrator directly."
        return $false
    }
}
```

### 4. Invoke-AdminAction (runs in elevated child)

```powershell
function Invoke-AdminAction {
    param([string]$Action)
    $result = $true

    switch ($Action) {
        'EnvSanitizer-Machine' {
            # Clean Machine PATH
            $pathVar = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
            if ($pathVar) {
                $newPath = ($pathVar -split ';' | Where-Object { $_ -notmatch '(?i)docker' }) -join ';'
                if ($newPath -ne $pathVar) {
                    [Environment]::SetEnvironmentVariable('Path', $newPath, [EnvironmentVariableTarget]::Machine)
                }
            }
            # Clean Machine DOCKER_* vars
            foreach ($ev in @('DOCKER_HOST','DOCKER_CERT_PATH','DOCKER_TLS_VERIFY','DOCKER_CONFIG','DOCKER_CONTEXT')) {
                $val = [Environment]::GetEnvironmentVariable($ev, [EnvironmentVariableTarget]::Machine)
                if ($val) { [Environment]::SetEnvironmentVariable($ev, $null, [EnvironmentVariableTarget]::Machine) }
            }
        }

        'Registry-Cleanup' {
            foreach ($rp in @('HKLM:\SOFTWARE\Docker','HKLM:\SOFTWARE\Docker Inc.',
                              'HKCU:\SOFTWARE\Docker','HKCU:\SOFTWARE\Docker Inc.',
                              'HKLM:\SYSTEM\CurrentControlSet\Services\docker',
                              'HKLM:\SYSTEM\CurrentControlSet\Services\com.docker.service')) {
                if (Test-Path $rp) { Remove-Item $rp -Recurse -Force -ErrorAction SilentlyContinue }
            }
        }

        'Services-Stop' {
            foreach ($svc in @('docker','docker-desktop','com.docker.service','Docker Desktop Service')) {
                $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
                if ($s) { Stop-Service $s -Force; Set-Service $s -StartupType Disabled }
            }
        }

        'WinFeatures-Disable' {
            $f = Get-WindowsOptionalFeature -Online -FeatureName 'Containers' -ErrorAction SilentlyContinue
            if ($f -and $f.State -eq 'Enabled') {
                Disable-WindowsOptionalFeature -Online -FeatureName 'Containers' -NoRestart
            }
        }

        'CompleteRemoval-Admin' {
            # Runs all admin actions in sequence for full removal
            Invoke-AdminAction -Action 'Registry-Cleanup'
            Invoke-AdminAction -Action 'Services-Stop'
            Invoke-AdminAction -Action 'EnvSanitizer-Machine'
        }

        default {
            Write-Host "  Unknown admin action: $Action" -ForegroundColor Red
            $result = $false
        }
    }
    return $result
}
```

### 5. Startup Elevation Prompt (when not admin)

```powershell
if (-not (Test-IsAdmin)) {
    Write-Host "  NOT RUNNING AS ADMINISTRATOR"
    Write-Host "  [A] Auto-elevate now (recommended)"
    Write-Host "  [C] Continue without elevation"
    Write-Host "  [N] No, exit"
    $ch = Read-Host "  Choice"
    if ($ch -match '^[aA]') {
        $psExe = if ($Script:IsPSCore) { 'pwsh.exe' } else { 'powershell.exe' }
        $myPath = $MyInvocation.MyCommand.Path
        if (-not $myPath) { $myPath = "C:\Fallback\Path.ps1" }
        Start-Process -FilePath $psExe -Verb RunAs -ArgumentList @(
            '-NoProfile', '-ExecutionPolicy', 'Bypass',
            '-File', "`"$myPath`""
        ) -WindowStyle Normal
        exit 0
    }
    elseif ($ch -match '^[nN]') { exit 1 }
}
```

## Critical Constraints

| Constraint | Why | Fix |
|---|---|---|
| `param()` must be before ALL code | PowerShell reads params before any execution | Place as first non-comment code |
| `$MyInvocation.MyCommand.Path` is script-only | Empty in REPL or dot-sourcing | Fall back to `$PSScriptRoot` |
| Admin actions run in a fresh process | No variable state is inherited from parent | Each action must be fully self-contained |
| `Start-Process -ArgumentList @(array)` | Avoids quoting nightmare of CMD-style strings | Use array, NOT a single string |
| `exit 0` after admin action | Without it, window closes before user reads output | Always pair with `ReadKey` |
| UAC may be disabled | `-Verb RunAs` silently fails | Detect with `Test-IsAdmin` before calling Invoke-Elevated |
| Script path may be relative | Resolved differently in elevated context | Test the resolved path and fall back |

## Self-Test Checklist

- [ ] `param([string]$AdminAction = '')` is the first code line
- [ ] Entry point checks `$AdminAction` before interactive start
- [ ] `Invoke-Elevated` checks `Test-IsAdmin` first (short-circuit)
- [ ] `$MyInvocation.MyCommand.Path` has fallback chain
- [ ] Each admin action is a standalone `switch` case in `Invoke-AdminAction`
- [ ] Admin child exits with `ReadKey` + `exit 0`
- [ ] UAC decline is caught by try/catch, returns $false, parent continues
