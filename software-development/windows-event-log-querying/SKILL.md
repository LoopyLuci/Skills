---
name: windows-event-log-querying
description: "Use when searching/filtering Windows Event Logs."
category: software-development
tags: [windows, eventlog, event-viewer, logging, powershell]
---
# Windows Event Log Querying

Searching and filtering Windows Event Logs with PowerShell.

## Basic Queries

```powershell
# Last 50 system events
Get-WinEvent -LogName System -MaxEvents 50

# Filter by level
Get-WinEvent -LogName Application -MaxEvents 100 | Where-Object { $_.Level -eq 2 }  # Error

# Level values: 1=Critical, 2=Error, 3=Warning, 4=Info, 5=Verbose

# Filter by date
Get-WinEvent -LogName System | Where-Object { $_.TimeCreated -gt (Get-Date).AddHours(-24) }

# Count by level
Get-WinEvent -LogName System -MaxEvents 1000 | Group-Object Level | Select-Object Name, Count
```

## Advanced Filtering

```powershell
# Filter XML (fastest for large logs)
$filter = @"
<QueryList>
  <Query Id="0">
    <Select Path="Application">
      *[System[(EventID=1000 or EventID=1001) and TimeCreated[timediff(@SystemTime) &lt;= 86400000]]]
    </Select>
  </Query>
</QueryList>
"@
Get-WinEvent -FilterXml $filter

# FilterHashtable (PS 5.1+)
Get-WinEvent -FilterHashtable @{
    LogName   = 'System'
    ID        = 1000, 1001, 1002
    Level     = 1, 2   # Critical or Error
    StartTime = (Get-Date).AddDays(-1)
    EndTime   = (Get-Date)
}
```

## Find Docker Events

```powershell
# Docker-related events
Get-WinEvent -LogName Application -MaxEvents 500 |
    Where-Object { $_.ProviderName -match 'docker' }

# Service start/stop events
Get-WinEvent -LogName System -MaxEvents 200 |
    Where-Object { $_.ProviderName -eq 'Service Control Manager' -and $_.Message -match 'docker' }

# Docker Desktop crashes
Get-WinEvent -LogName Application -MaxEvents 1000 |
    Where-Object { $_.Message -match 'Docker Desktop' -and $_.Level -le 2 }
```

## Export Results

```powershell
# Export to CSV
Get-WinEvent -LogName System -MaxEvents 100 |
    Select-Object TimeCreated, Id, LevelDisplayName, Message |
    Export-Csv "events.csv" -NoTypeInformation

# Export to HTML
Get-WinEvent -LogName Application -MaxEvents 50 |
    ConvertTo-Html -Property TimeCreated, Id, Message |
    Out-File "events.html"
```

## Clear/Archive Logs

```powershell
# Clear log
Clear-WinEvent -LogName "Docker-Container"
Remove-Item "$env:SystemRoot\System32\winevt\Logs\*.evtx" -Force  # Admin only

# Log max size
Get-WinEvent -ListLog * | Select-Object LogName, FileSize, MaximumSizeInBytes

# Set max size (512MB)
Limit-WinEventLog -LogName Application -MaximumSize 512MB
```

## Pitfalls

- Get-WinEvent is faster than Get-EventLog (deprecated)
- FilterHashtable is much faster than Where-Object for large logs
- Event logs have size limits -- older events are discarded
- Some logs require admin (Security, System)
- Remote event log queries need WinRM permissions
