---
name: windows-registry-powershell
description: "Use when reading or writing the Windows registry via PS."
category: software-development
tags: [windows, registry, powershell, hklm, hkcu]
---
# Windows Registry via PowerShell

Reading and writing the Windows registry with PowerShell.

## PSDrive Navigation

```powershell
# Available drives
Get-PSDrive -PSProvider Registry

# Navigate like filesystem
cd HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion
ls
cd HKCU:\SOFTWARE
```

## Reading Values

```powershell
# Get a specific value
Get-ItemProperty -Path "HKLM:\SOFTWARE\Docker" -Name "InstallPath"

# Get all values under a key
Get-ItemProperty -Path "HKLM:\SOFTWARE\Docker"

# List subkeys
Get-ChildItem -Path "HKLM:\SOFTWARE\Docker"

# Check if key exists
Test-Path "HKLM:\SOFTWARE\Docker"
```

## Writing Values

```powershell
# Create key (if not exists)
New-Item -Path "HKLM:\SOFTWARE\MyApp" -Force

# Set value
Set-ItemProperty -Path "HKLM:\SOFTWARE\MyApp" -Name "Version" -Value "1.0.0"
Set-ItemProperty -Path "HKLM:\SOFTWARE\MyApp" -Name "Path" -Value "C:\myapp" -Type ExpandString
Set-ItemProperty -Path "HKLM:\SOFTWARE\MyApp" -Name "Flags" -Value 1 -Type DWord
Set-ItemProperty -Path "HKLM:\SOFTWARE\MyApp" -Name "Data" -Value @(1,2,3) -Type Binary
Set-ItemProperty -Path "HKLM:\SOFTWARE\MyApp" -Name "Strings" -Value @("a","b") -Type MultiString
```

## Deleting

```powershell
# Remove a value
Remove-ItemProperty -Path "HKLM:\SOFTWARE\MyApp" -Name "Version"

# Remove an entire key and all subkeys
Remove-Item -Path "HKLM:\SOFTWARE\MyApp" -Recurse -Force
```

## Using reg.exe (batch-compatible)

```batch
reg query HKLM\SOFTWARE\Docker
reg add HKLM\SOFTWARE\MyApp /v Version /t REG_SZ /d "1.0.0" /f
reg delete HKLM\SOFTWARE\Docker /f
reg export HKLM\SOFTWARE\MyApp backup.reg
reg import backup.reg
```

## Common Tasks

```powershell
# Search registry for Docker keys
Get-ChildItem -Path "HKLM:\SOFTWARE" -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.PSPath -match 'docker' }

# Check if a service exists in registry
Test-Path "HKLM:\SYSTEM\CurrentControlSet\Services\docker"

# Get service start type from registry
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\docker" -Name "Start"
# 2=Automatic, 3=Manual, 4=Disabled
```

## Pitfalls

- **HKLM** requires admin -- only HKCU is writable without elevation
- **32-bit vs 64-bit** -- Registry redirector on 64-bit OS: `HKLM:\SOFTWARE\WOW6432Node\`
- **Remove-Item -Recurse** is destructive -- no undo
- **reg.exe import** silently merges -- there's no undo mechanism
- **REG_SZ vs REG_EXPAND_SZ** -- use ExpandString for paths with %VARIABLES%
