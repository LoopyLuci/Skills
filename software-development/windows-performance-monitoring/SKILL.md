---
name: windows-performance-monitoring
description: "Use when monitoring perf counters and system metrics."
category: software-development
tags: [windows, performance, monitoring, counters, perfmon]
---
# Windows Performance Monitoring

Monitoring system performance via PowerShell and PerfMon.

## CPU

```powershell
# Current CPU usage
Get-Counter "\Processor(_Total)\% Processor Time"

# Per-core CPU
Get-Counter "\Processor(*)\% Processor Time"

# CPU over time (5 samples, 2s间隔)
Get-Counter "\Processor(_Total)\% Processor Time" -SampleInterval 2 -MaxSamples 5

# Top CPU processes
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, CPU, WorkingSet
```

## Memory

```powershell
# Available memory
Get-Counter "\Memory\Available MBytes"

# Memory breakdown
Get-Counter "\Memory\*"

# Process memory usage
Get-Process | Sort-Object WorkingSet -Descending | Select -First 10 Name, WorkingSet

# Page file usage
Get-Counter "\Paging File(_Total)\% Usage"
```

## Disk

```powershell
# Disk activity
Get-Counter "\PhysicalDisk(_Total)\% Disk Time"
Get-Counter "\PhysicalDisk(_Total)\Avg. Disk Queue Length"

# Disk read/write speed
Get-Counter "\PhysicalDisk(*)\Disk Reads/sec"
Get-Counter "\PhysicalDisk(*)\Disk Writes/sec"

# Free space
Get-PSDrive -PSProvider FileSystem | Select-Object Name, Used, Free
```

## Network

```powershell
# Network throughput
Get-Counter "\Network Interface(*)\Bytes Total/sec"

# Per-adapter stats
Get-Counter "\Network Interface(*)\Packets Sent/sec"
Get-Counter "\Network Interface(*)\Packets Received/sec"
```

## Docker-Specific Monitoring

```powershell
# Docker container CPU
Get-Counter "\Docker Container(*)\CPU %"

# Docker container memory
Get-Counter "\Docker Container(*)\Memory Usage"

# Docker container network
Get-Counter "\Docker Container(*)\Network Bytes Received/sec"
```

## Log Performance Data

```powershell
# Log to CSV for analysis
$samples = Get-Counter "\Processor(_Total)\% Processor Time" `
    "\Memory\Available MBytes" `
    "\PhysicalDisk(_Total)\% Disk Time" `
    -SampleInterval 5 -MaxSamples 60

$samples | ForEach-Object {
    [PSCustomObject]@{
        Timestamp = $_.TimeStamp
        CPU = $_.CounterSamples[0].CookedValue
        MemoryMB = $_.CounterSamples[1].CookedValue
        Disk = $_.CounterSamples[2].CookedValue
    }
} | Export-Csv "perf-log.csv" -NoTypeInformation
```

## Real-Time Dashboard

```powershell
while ($true) {
    Clear-Host
    Get-Counter "\Processor(_Total)\% Processor Time" |
        ForEach-Object { "CPU: $($_.CounterSamples[0].CookedValue)%" }
    Get-Counter "\Memory\Available MBytes" |
        ForEach-Object { "RAM Free: $($_.CounterSamples[0].CookedValue) MB" }
    Start-Sleep -Seconds 2
}
```

## Pitfalls

- Some counters need admin (disk, network)
- First counter sample is often invalid -- discard it
- High-frequency polling impacts performance
- Docker counters only available when Docker Desktop is running
- Counter paths are locale-dependent on non-English Windows
