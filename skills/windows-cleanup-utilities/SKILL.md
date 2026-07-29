---
name: windows-cleanup-utilities
description: "Use when cleaning temp files and disk space on Windows."
category: software-development
tags: [windows, cleanup, disk, temp-files, maintenance]
---
# Windows Cleanup Utilities

Cleaning temporary files, caches, and reclaiming disk space on Windows.

## Temp Files

```powershell
# Windows temp
Get-ChildItem "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Windows system temp
Get-ChildItem "$env:SystemRoot\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# User temp (multiple locations)
$env:TEMP, $env:TMP, "$env:LOCALAPPDATA\Temp" | ForEach-Object {
    Get-ChildItem "$_\*" -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object { -not $_.PSIsContainer } |
        Remove-Item -Force -ErrorAction SilentlyContinue
}
```

## Disk Cleanup (built-in)

```powershell
# Launch the disk cleanup UI
cleanmgr.exe

# Cleanup automatically (savesettings first)
cleanmgr.exe /sagerun:1

# Or use Dism
DISM.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase
```

## WinSxS

```powershell
# Check WinSxS size
DISM.exe /Online /Cleanup-Image /AnalyzeComponentStore

# Clean WinSxS
DISM.exe /Online /Cleanup-Image /StartComponentCleanup

# Remove superseded components (cannot rollback updates)
DISM.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase
```

## Delivery Optimization Cache

```powershell
Get-ChildItem "$env:SystemRoot\SoftwareDistribution\DeliveryOptimization\*" -Recurse |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Or via Settings
Start-Process "ms-settings:delivery-optimization"
```

## Windows Update Cache

```powershell
net stop wuauserv
Remove-Item "$env:SystemRoot\SoftwareDistribution\Download\*" -Recurse -Force
net start wuauserv
```

## Browser Caches

```powershell
# Edge/Chrome
Remove-Item "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache\*" -Recurse -Force
Remove-Item "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache\*" -Recurse -Force

# Firefox
Remove-Item "$env:LOCALAPPDATA\Mozilla\Firefox\Profiles\*\cache2\*" -Recurse -Force
```

## Docker Cleanup (Specific)

```powershell
docker system prune -a -f --volumes
# Also see docker-volume-backup-restore and docker-desktop-windows-removal skills
```

## Pitfalls

- **Some temp files are locked** -- skip errors with -ErrorAction SilentlyContinue
- **WinSxS /ResetBase** prevents uninstalling current Windows update
- **Cleanmgr /sagerun** needs pre-configured settings
- **Delivery Optimization** cache is used for peer-to-peer updates
