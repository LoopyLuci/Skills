---
name: powershell-windows-tools
description: "Use when building PS admin tools. BOM, UAC, PS5/7, exit."
category: software-development
tags: [powershell, windows, admin-tools, system-management, cli, uac-elevation, ps5-compat, ps7-compat]
---

# PowerShell Windows Tools

Author production-grade PowerShell scripts for Windows system administration, cleanup utilities, service management, and interactive CLI tools.

## When to Use

- Building an interactive CLI tool for Windows system management (Docker cleanup, registry management, service control)
- Writing a PowerShell script that needs to run on both Windows PowerShell 5.1 AND PowerShell 7
- Building a tool that needs auto-elevation for admin operations (UAC)
- Creating a recovery-capable tool (undo/restore points)
- Any task involving `Start-Process -Verb RunAs` for privilege escalation

## Critical Gotchas

### 1. UTF-8 BOM or Die

Windows PowerShell 5.1 assumes **ANSI encoding** when reading `.ps1` files without a BOM (Byte Order Mark).
If your script contains ANY Unicode characters (em-dash `—`, box-drawing `╔╗╚╝`, emoji, non-ASCII), PS5 will
corrupt them into garbage, causing parse errors or silent data corruption.

**Always save `.ps1` files with UTF-8 BOM** (`utf-8-sig` in Python, `-Encoding UTF8` in PowerShell).

```python
# Python: save with BOM
with open('script.ps1', 'w', encoding='utf-8-sig') as f:
    f.write(content)
```

```powershell
# PowerShell: save with BOM
$content | Out-File -FilePath 'script.ps1' -Encoding UTF8
```

### 2. `$var:` Colon Scope Trap

In PowerShell strings, `$varname:` is interpreted as a **namespace-qualified variable reference**
(like `$env:PATH`). Even `$varname: text` can trigger this in PowerShell 7, causing parser error.

**BAD** — crashes on PS7:
```powershell
Write-Host "  FAIL $svc: $_"
```

**GOOD** — use format operator:
```powershell
Write-Host ("  FAIL {0}: {1}" -f $svc, $_)
```

### 3. `Start-Process -Verb RunAs` Quoting

When using `Start-Process -Verb RunAs`, **never pass `-ArgumentList` as an array**.
The array-to-command-line conversion mangles quotes.

**BAD** — array-based:
```powershell
Start-Process -FilePath pwsh.exe -Verb RunAs -ArgumentList @('-NoProfile', '-File', '"C:\path\script.ps1"') -Wait
```

**GOOD** — flat string:
```powershell
$argString = '-NoProfile -File "' + $scriptPath + '" -Action ' + $actionName
Start-Process -FilePath pwsh.exe -Verb RunAs -ArgumentList $argString -Wait
```

### 4. `#Requires -RunAsAdministrator` Kills UX Silently

Causes PowerShell to **immediately exit with no visible message** if the user isn't admin.
Remove it and handle elevation gracefully.

### 5. Exit Handling (Keep Window Open)

When right-click → "Run with PowerShell 7" (no `-NoExit`), the window closes immediately.
Add a pause in the `finally` block:
```powershell
finally {
    Write-Host "`n  Press any key to close..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
}
```

### 6. Capture Return Values

PowerShell emits uncaptured return values to stdout, leaking paths/objects to console.
```powershell
$null = New-RestorePoint -Label "Snapshot"
```

## Auto-Elevation Pattern (`-AdminAction` pattern)

When building a tool that needs admin for some operations but should not require it at startup:

### 1. Add `-AdminAction` parameter to the script
```powershell
param([string]$AdminAction = '')
```

### 2. Guard in entry point — elevated child runs and exits
```powershell
if ($AdminAction) {
    Initialize-Environment
    Invoke-AdminAction -Action $AdminAction
    Write-Host "Press any key to close this window..."
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    exit 0
}
```

### 3. `Invoke-Elevated` — called from parent, spawns admin child
```powershell
function Invoke-Elevated {
    param([string]$Action, [string]$Description)
    if (Test-IsAdmin) { return Invoke-AdminAction -Action $Action }
    Write-Host "[ADMIN REQUIRED] $Description"
    $psExe = if ($PSVersionTable.PSVersion.Major -ge 7) { 'pwsh.exe' } else { 'powershell.exe' }
    # CRITICAL: flat string, NOT array
    $argString = '-NoProfile -ExecutionPolicy Bypass -File "' + $scriptPath + '" -AdminAction ' + $Action
    Start-Process -FilePath $psExe -Verb RunAs -ArgumentList $argString -Wait
}
```

### 4. `Invoke-AdminAction` — runs inside elevated child
```powershell
function Invoke-AdminAction {
    param([string]$Action)
    switch ($Action) {
        'Registry-Cleanup' { ... }
        'Services-Stop'    { ... }
        'EnvSanitizer-Machine' { ... }
    }
}
```

### 5. Startup elevation prompt
At launch when not admin, offer a choice:
```
[A] Auto-elevate now (relaunch entire script as admin)
[C] Continue (per-operation elevation via Invoke-Elevated)
[N] Exit
```

## Restore Point Pattern

```powershell
function New-RestorePoint {
    # Create dir, snapshot files/registry/WSL2 exports, save manifest.json
}

function Invoke-Rollback {
    # Restore WSL2 (wsl --import), registry (reg import), env vars
}
```

## PS5 vs PS7 Differences

| Aspect | Windows PS 5.1 | PowerShell 7 |
|---|---|---|
| Encoding | ANSI default, needs BOM | UTF-8 without BOM default |
| `$var:` in strings | Tolerant | Strict — parser error |
| `Start-ThreadJob` | Not available | Available |
| Null-coalescing `??` | Not available | Available |

## Templates

- **`templates/admin-tool-skeleton.ps1`** — fully wired admin-tool starter combining all patterns above:
  param() block with AdminAction, Test-Admin, Invoke-Elevated with flat-string ArgumentList,
  Invoke-AdminAction, menu system, confirm/pause helpers, and a finally-block exit handler.
  Copy this file to start a new tool, then extend the switch statement and menu items.

## Reference Transcripts

- **`references/error-transcripts.md`** — detailed error reproduction recipes for all patterns above:
  #Requires silent exit, UTF-8 BOM corruption, `$var:` PS7 parser trap, flat-string ArgumentList,
  return value leakage, and Docker Desktop MSI installer cleanup (Error 6).

## Verification

1. Parse clean on both `powershell.exe` and `pwsh.exe`
2. Non-admin startup shows elevation prompt, doesn't crash silently
3. `Start-Process -Verb RunAs` uses flat string, not array
4. All `$var:` patterns use `-f` format operator
5. File saved with UTF-8 BOM
