---
name: powershell-console-ui
description: "Use when building interactive console menus in PS."
category: software-development
tags: [powershell, console, ui, menu, interactive]
---
# PowerShell Console UI

Building interactive console menus and user interfaces in PowerShell.

## ReadKey (Single Keypress)

```powershell
function Pause-Script {
    Write-Host "Press any key to continue..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
}
```

## Simple Menu

```powershell
function Show-Menu {
    param([string[]]$Options, [string]$Title = "Menu")
    Write-Host "=== $Title ===" -ForegroundColor Cyan
    for ($i = 0; $i -lt $Options.Count; $i++) {
        Write-Host "  [$($i+1)] $($Options[$i])"
    }
    $choice = Read-Host "Select"
    if ($choice -match '^\d+$' -and [int]$choice -ge 1 -and [int]$choice -le $Options.Count) {
        return $Options[[int]$choice - 1]
    }
    return $null
}
```

## Colored Output

```powershell
function Write-Color {
    param([string]$Text, [ConsoleColor]$Color = 'White')
    Write-Host $Text -ForegroundColor $Color
}

# Standard colors
Write-Host "Error" -ForegroundColor Red
Write-Host "Warning" -ForegroundColor Yellow
Write-Host "Success" -ForegroundColor Green
Write-Host "Info" -ForegroundColor Cyan
Write-Host "Dim" -ForegroundColor DarkGray
```

## Table Formatting

```powershell
function Write-Table {
    param([array]$Data, [string[]]$Props)
    if (-not $Data) { Write-Host "(No data)"; return }
    # Header
    $h = $Props | ForEach-Object { $_.PadRight(20) }
    Write-Host " $h" -ForegroundColor DarkCyan
    Write-Host " $('-' * ($Props.Count * 20))" -ForegroundColor DarkGray
    # Rows
    foreach ($row in $Data) {
        $line = $Props | ForEach-Object {
            $val = "$($row.$_)"
            $val.PadRight(20)
        }
        Write-Host " $line"
    }
}
```

## Progress Bar

```powershell
for ($i = 1; $i -le 100; $i++) {
    Write-Progress -Activity "Processing" -Status "$i%" -PercentComplete $i
    Start-Sleep -Milliseconds 50
}
Write-Progress -Activity "Processing" -Completed
```

## Read-Host with Default

```powershell
$response = Read-Host "Continue [Y/n]"
if ($response -eq '' -or $response -match '^[yY]') {
    Write-Host "Continuing..."
}
```

## Confirmation Helper

```powershell
function Confirm {
    param([string]$Message, [string]$Default = 'N')
    $prompt = if ($Default -eq 'Y') { "$Message [Y/n] " } else { "$Message [y/N] " }
    $r = Read-Host $prompt
    if (-not $r) { return $Default -eq 'Y' }
    return $r -match '^[yY]'
}

if (Confirm "Delete all files?" 'N') { Remove-Item * }
```

## Pitfalls

- **ReadKey** fails in non-interactive contexts (CI, pipelines) -- check $Host.Name
- **ConsoleColor** is session-specific -- reset at end or user inherits colors
- **Read-Host** returns empty string on EOF -- check for $null
- **Write-Progress** impacts performance in loops over 100k+ iterations
- **Encoding** -- Unicode/emoji in console may render as boxes depending on font
