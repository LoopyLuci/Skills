---
name: powershell-filesystem-advanced
description: "Use when doing advanced PS filesystem operations."
category: software-development
tags: [powershell, filesystem, files, directories, io]
---
# PowerShell Advanced Filesystem

Advanced filesystem operations with PowerShell.

## Bulk File Operations

```powershell
# Recursively rename files
Get-ChildItem -Recurse -Filter "*.txt" |
    Where-Object { $_.Name -match '_old$' } |
    ForEach-Object {
        $newName = $_.Name -replace '_old$', '_new'
        Rename-Item $_.FullName -NewName $newName
    }

# Move files by date
Get-ChildItem -Recurse -Filter "*.log" |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } |
    ForEach-Object {
        $archiveDir = Join-Path $_.Directory "archive"
        New-Item -ItemType Directory -Path $archiveDir -Force
        Move-Item $_.FullName -Destination $archiveDir
    }

# Batch delete with confirmation
Get-ChildItem -Recurse -Directory -Filter "node_modules" |
    ForEach-Object {
        if (Confirm "Delete $($_.FullName)?") {
            Remove-Item $_.FullName -Recurse -Force
        }
    }
```

## File Content Manipulation

```powershell
# Replace text in multiple files
Get-ChildItem -Recurse -Filter "*.config" |
    ForEach-Object {
        (Get-Content $_.FullName) -replace 'oldhost\.com', 'newhost.com' |
            Set-Content $_.FullName -Encoding UTF8
    }

# Insert line before match
$file = "appsettings.json"
$content = Get-Content $file -Raw
$content -replace '(?="ConnectionStrings")', "`"AddedField`": `"value`",`n  " |
    Set-Content $file -Encoding UTF8

# Merge multiple files
Get-ChildItem -Filter "*.sql" | Sort-Object Name |
    ForEach-Object { Get-Content $_.FullName } |
    Set-Content "merged.sql"
```

## Symbolic Links

```powershell
# Create symlink (file)
New-Item -ItemType SymbolicLink -Path "link.txt" -Target "original.txt"

# Directory junction (works without admin)
New-Item -ItemType Junction -Path "C:\project" -Target "D:\Projects\current"

# Directory symlink (needs admin)
New-Item -ItemType SymbolicLink -Path "C:\link" -Target "D:\Projects"

# Hard link (same volume only)
New-Item -ItemType HardLink -Path "hardlink.txt" -Target "original.txt"
```

## Compare Directories

```powershell
# Find files in source not in target
$source = Get-ChildItem -Recurse "C:\source"
$target = Get-ChildItem -Recurse "C:\target"
$diff = Compare-Object $source $target -Property Name, Length
$diff | Where-Object SideIndicator -eq '<=' | Select-Object Name  # Only in source

# Find files that differ
$missing = @()
foreach ($f in $source) {
    $t = Join-Path "C:\target" $f.FullName.Substring("C:\source".Length)
    if (-not (Test-Path $t)) { $missing += $f.FullName }
}
```

## File Watching

```powershell
# Watch directory for changes
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = "C:\watch"
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true

Register-ObjectEvent $watcher "Created" -Action {
    Write-Host "Created: $($Event.SourceEventArgs.FullPath)"
}
Register-ObjectEvent $watcher "Changed" -Action {
    Write-Host "Changed: $($Event.SourceEventArgs.FullPath)"
}
Register-ObjectEvent $watcher "Deleted" -Action {
    Write-Host "Deleted: $($Event.SourceEventArgs.FullPath)"
}
```

## Pitfalls

- Get-ChildItem large directories can be slow -- use -Filter to narrow
- Set-Content uses UTF8 BOM by default in PS5 -- use -Encoding UTF8NoBOM in PS7
- Symbolic links need admin on Windows (file symlinks), junctions don't
- FileSystemWatcher misses events if buffer overflows (many changes at once)
- Paths longer than 260 chars need `\\?\` prefix or Win10 long path enabled
