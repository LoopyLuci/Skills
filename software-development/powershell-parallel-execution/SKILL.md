---
name: powershell-parallel-execution
description: "Use when running tasks in parallel with PowerShell."
category: software-development
tags: [powershell, parallel, threading, runspace, jobs]
---
# PowerShell Parallel Execution

Running tasks concurrently in PowerShell.

## ForEach-Object -Parallel (PS 7+)

```powershell
# Simple parallel
Get-ChildItem "*.jpg" | ForEach-Object -Parallel {
    $_.Name + " processed"
} -ThrottleLimit 5

# With variables (use $using: scope)
$folder = "C:\images"
Get-ChildItem "*.jpg" | ForEach-Object -Parallel {
    $dest = Join-Path $using:folder "processed"
    # process $_
} -ThrottleLimit 10
```

## Start-ThreadJob (PS 6+, cross-platform)

```powershell
$jobs = @()
$paths = @("C:\logs1", "C:\logs2")

foreach ($path in $paths) {
    $jobs += Start-ThreadJob -ScriptBlock {
        param($p)
        Get-ChildItem $p -Recurse | Measure-Object -Property Length -Sum
    } -ArgumentList $path
}

# Wait for all
$results = $jobs | Receive-Job -Wait -AutoRemoveJob
```

## Classic Job System (PS 3+, slower)

```powershell
$j1 = Start-Job -ScriptBlock { Start-Sleep 5; "Job 1 done" }
$j2 = Start-Job -ScriptBlock { Start-Sleep 3; "Job 2 done" }
$results = $j1, $j2 | Wait-Job | Receive-Job
$j1, $j2 | Remove-Job
```

## Runspaces (advanced, fastest)

```powershell
$runspacePool = [RunspaceFactory]::CreateRunspacePool(1, 5)  # min 1, max 5
$runspacePool.Open()

$ps = [PowerShell]::Create()
$ps.RunspacePool = $runspacePool
$ps.AddScript({ param($x) $x * 2 }).AddArgument(21)

$async = $ps.BeginInvoke()
$result = $ps.EndInvoke($async)
$ps.Dispose()
$runspacePool.Dispose()
```

## Throttle Control

```powershell
# ForEach-Object -Parallel already throttles via -ThrottleLimit
# Default ThrottleLimit = 5

# For ThreadJob, manage manually
$maxConcurrent = 3
$batch = @()
Get-ChildItem "C:\logs" -Directory | ForEach-Object {
    $batch += Start-ThreadJob -ScriptBlock { param($d) Get-ChildItem $d -Recurse | Measure-Object } -ArgumentList $_.FullName
    if ($batch.Count -ge $maxConcurrent) {
        $batch | Receive-Job -Wait -AutoRemoveJob
        $batch = @()
    }
}
# Process remaining
if ($batch) { $batch | Receive-Job -Wait -AutoRemoveJob }
```

## Pitfalls

- **$using:scope** required in ForEach-Object -Parallel for parent variables
- **No interactive cmds** inside parallel blocks -- no Read-Host, no Show-Forms
- **ThreadJob** uses threads, not processes -- watch for thread-safe issues
- **Start-Job** is heavy (each job = new process) -- avoid for many small tasks
- **Runspaces** are most efficient but need careful resource management
