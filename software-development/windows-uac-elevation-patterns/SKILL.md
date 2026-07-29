---
name: windows-uac-elevation-patterns
description: "Use when auto-elevating scripts to admin on Windows."
category: software-development
tags: [windows, uac, elevation, admin, powershell, batch]
---
# Windows UAC Elevation Patterns

Auto-elevating scripts to Administrator on Windows.

## PowerShell to PowerShell

```powershell
# Detect admin
$isAdmin = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
$isElevated = $isAdmin.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

# Self-relaunch as admin
if (-not $isElevated) {
    $psExe = if ($PSVersionTable.PSVersion.Major -ge 7) { 'pwsh.exe' } else { 'powershell.exe' }
    $argString = '-NoProfile -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '"'
    Start-Process -FilePath $psExe -Verb RunAs -ArgumentList $argString
    exit
}
```

## Key Rule: Flat String, Not Array

```powershell
# BAD -- array-based ArgumentList mangles quotes with -Verb RunAs
Start-Process pwsh.exe -Verb RunAs -ArgumentList @(
    '-File', '"C:\path\script.ps1"', '-Flag value'
)

# GOOD -- flat string with proper quoting
$args = '-File "C:\path\script.ps1" -Flag value'
Start-Process pwsh.exe -Verb RunAs -ArgumentList $args
```

## Passing Parameters to Elevated Instance

```powershell
# Script accepts -AdminAction parameter
if ($AdminAction) {
    # Elevated child -- run the action
    Invoke-AdminAction -Action $AdminAction
    exit
}

# Parent calls elevated child
function Invoke-Elevated {
    param([string]$Action, [string]$Description)
    if (Test-Admin) { return Invoke-AdminAction -Action $Action }
    Write-Host "[ADMIN REQUIRED] $Description"
    $psExe = if ($PSVersionTable.PSVersion.Major -ge 7) { 'pwsh.exe' } else { 'powershell.exe' }
    $args = '-NoProfile -ExecutionPolicy Bypass -File "' + $scriptPath + '" -AdminAction ' + $Action
    Start-Process -FilePath $psExe -Verb RunAs -ArgumentList $args -Wait
}
```

## Batch to PowerShell Elevation

```batch
@echo off
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
REM ... admin code here ...
```

## Batch with PowerShell 7 Detection

```batch
@echo off
where pwsh.exe >nul 2>&1
if %errorlevel% equ 0 ( set "PS_EXE=pwsh.exe" ) else ( set "PS_EXE=powershell.exe" )

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting admin...
    powershell -Command "Start-Process '%PS_EXE%' -Verb RunAs -ArgumentList '-NoProfile -File \"%~dp0script.ps1\"'"
    exit /b
)
%PS_EXE% -NoProfile -File "%~dp0script.ps1"
pause
```

## COM Elevation (No UAC Prompt, Same Process)

```powershell
# ShellExecute bypass (limited use cases)
$shell = New-Object -ComObject Shell.Application
$shell.ShellExecute('powershell.exe', '-NoProfile -Command "Write-Host Admin"', '', 'runas')
```

## Pitfalls

- **#Requires -RunAsAdministrator** kills UX silently -- remove, use graceful elevation
- **Array-based ArgumentList** with -Verb RunAs corrupts quoting -- use flat string
- **Start-Process -Wait** with UAC returns immediately -- child runs separately
- **Double elevation** -- if child is already admin, detect and skip
- **No-Exit** for debugging -- use -NoExit in dev, remove for production
