<#>
.SYNOPSIS
    AdminTool Skeleton — Production-grade PowerShell admin tool template
.DESCRIPTION
    Combines all patterns from powershell-windows-tools: BOM, auto-elevation,
    menu system, error handling, restore points, and clean exit handling.
    Copy this file as a starting point for new admin tools.
.NOTES
    Requires: PowerShell 5.1+, Windows 10/11
#>

param(
    [string]$AdminAction = ''
)

#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Script:AppName = 'AdminTool'

# ─── Colors ────────────────────────────────────────────────────────────────
$Script:C = @{
    P = [ConsoleColor]::Cyan; S = [ConsoleColor]::Green
    W = [ConsoleColor]::Yellow; E = [ConsoleColor]::Red
    I = [ConsoleColor]::White; D = [ConsoleColor]::DarkGray
}

# ─── Helpers ───────────────────────────────────────────────────────────────
function Test-Admin {
    $p = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
    return $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Pause { Write-Host "`n  Press any key..." -ForegroundColor $Script:C.D; $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown') }

function Confirm { param([string]$M, [string]$D='N')
    $p = if ($D -eq 'Y') { "$M [Y/n] " } else { "$M [y/N] " }
    $r = Read-Host $p; if (-not $r) { return $D -eq 'Y' }; return $r -match '^[yY]'
}

# ─── Auto-Elevation ───────────────────────────────────────────────────────
function Invoke-Elevated {
    param([string]$Action)
    if (Test-Admin) { return [void](Invoke-AdminAction $Action) }
    Write-Host "`n  [ADMIN REQUIRED] $Action" -ForegroundColor $Script:C.W
    $psExe = if ($PSVersionTable.PSVersion.Major -ge 7) { 'pwsh.exe' } else { 'powershell.exe' }
    $path = $MyInvocation.MyCommand.Path
    if (-not $path -or -not (Test-Path $path)) { $path = "C:\path\to\AdminTool.ps1" }
    # FLAT STRING — never use array with -Verb RunAs (see gotcha #3)
    $args = '-NoProfile -ExecutionPolicy Bypass -File "' + $path + '" -AdminAction ' + $Action
    Start-Process -FilePath $psExe -Verb RunAs -ArgumentList $args -Wait
}

function Invoke-AdminAction {
    param([string]$Action)
    switch ($Action) {
        'SampleTask' { Write-Host "  Running elevated sample..." -ForegroundColor $Script:C.P }
        default { Write-Host "  Unknown action: $Action" -ForegroundColor $Script:C.E }
    }
}

# ─── Menu System ───────────────────────────────────────────────────────────
function Show-MainMenu {
    do {
        Write-Host "`n  [1] Sample Action" -ForegroundColor $Script:C.I
        Write-Host "  [2] Sample Elevated Task" -ForegroundColor $Script:C.I
        Write-Host "  [Q] Quit" -ForegroundColor $Script:C.I
        $ch = Read-Host "`n  Select"
        switch ($ch) {
            '1' { Write-Host "  Running sample..." -ForegroundColor $Script:C.S; Pause }
            '2' { Invoke-Elevated -Action 'SampleTask'; Pause }
        }
    } while ($ch -ne 'Q')
}

# ─── Entry Point ───────────────────────────────────────────────────────────
try {
    if ($AdminAction) {
        Write-Host "  ADMIN OPERATION: $AdminAction" -ForegroundColor $Script:C.P
        $null = Invoke-AdminAction $AdminAction
        Pause
        exit 0
    }
    if (-not (Test-Admin)) {
        Write-Host "`n  Not running as Administrator." -ForegroundColor $Script:C.W
        Write-Host "  Admin operations will auto-elevate via UAC." -ForegroundColor $Script:C.I
        Write-Host "`n  [A] Auto-elevate now   [C] Continue   [N] Exit" -ForegroundColor $Script:C.I
        switch -Wildcard (Read-Host "  Choice") {
            'A*' {
                $psExe = if ($PSVersionTable.PSVersion.Major -ge 7) { 'pwsh.exe' } else { 'powershell.exe' }
                $myPath = $MyInvocation.MyCommand.Path
                Start-Process $psExe -Verb RunAs -ArgumentList ('-NoProfile -File "' + $myPath + '"')
                exit 0
            }
            'N*' { exit 1 }
        }
    }
    Show-MainMenu
} catch {
    Write-Host "`n  FATAL: $_" -ForegroundColor $Script:C.E
    Pause
} finally {
    Write-Host "`n  Press any key to close..." -ForegroundColor $Script:C.D
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
}
