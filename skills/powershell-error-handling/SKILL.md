---
name: powershell-error-handling
description: "Use when handling errors in PowerShell scripts."
category: software-development
tags: [powershell, errors, try-catch, error-handling]
---
# PowerShell Error Handling

Proper error handling patterns for PowerShell scripts.

## try/catch/finally

```powershell
try {
    # Risky operation
    Remove-Item "locked-file.txt" -ErrorAction Stop
}
catch [System.UnauthorizedAccessException] {
    Write-Error "Access denied: $_"
}
catch [System.IO.FileNotFoundException] {
    Write-Error "File not found: $_"
}
catch {
    Write-Error "Unexpected error: $_"
    Write-Debug "Line: $($_.InvocationInfo.ScriptLineNumber)"
}
finally {
    # Always runs -- cleanup
    Close-Something
}
```

## Key: -ErrorAction Stop

```powershell
# Without Stop, non-terminating errors don't trigger catch!
Get-Item "nonexistent.txt" -ErrorAction Stop

# Global setting
$ErrorActionPreference = 'Stop'

# Per-command override
Get-ChildItem "C:\" -ErrorAction SilentlyContinue  # ignore errors
Get-ChildItem "C:\" -ErrorAction Continue           # default (print + continue)
Get-ChildItem "C:\" -ErrorAction Stop               # throw on error
Get-ChildItem "C:\" -ErrorAction Inquire            # ask user what to do
Get-ChildItem "C:\" -ErrorAction Ignore             # suppress completely
```

## $? and $LASTEXITCODE

```powershell
# $? = bool: did last command succeed?
# $LASTEXITCODE = native exit code

docker version 2>$null
if (-not $?) { Write-Error "Docker not available" }

# For native commands (exe, py, etc.)
cmd /c "exit 42"
$LASTEXITCODE  # 42

# Always check native exit codes
dotnet build
if ($LASTEXITCODE -ne 0) {
    throw "Build failed with exit code $LASTEXITCODE"
}
```

## Error Records

```powershell
# Automatic error variable
$Error[0]        # most recent error
$Error.Count     # number in buffer
$Error.Clear()   # clear buffer

# Capturing full error info
try {
    1/0
} catch {
    $_.Exception.Message
    $_.Exception.GetType().FullName
    $_.InvocationInfo.ScriptName
    $_.InvocationInfo.ScriptLineNumber
    $_.InvocationInfo.Line.Trim()
}
```

## Throw / Write-Error

```powershell
# Terminating (stops execution)
throw "Fatal: missing parameter"
throw [System.IO.FileNotFoundException]::new("config.json not found")

# Non-terminating (prints error, continues)
Write-Error "Warning: config.json not found, using defaults"
```

## Trap (older approach)

```powershell
# Script-level global error handler
trap {
    Write-Error "Caught: $_"
    continue   # continue execution
    break      # stop execution
}
```

## Pitfalls

- **Missing -ErrorAction Stop** is the #1 cause of uncaught errors in PowerShell
- **Native commands** (.exe, .bat) don't throw exceptions -- always check $LASTEXITCODE
- **$ErrorActionPreference** doesn't affect native commands
- **Write-Error** is NOT terminating -- use throw or -ErrorAction Stop
- **try/catch** only catches terminating errors
