---
name: windows-task-scheduler
description: "Use when managing scheduled tasks on Windows."
category: software-development
tags: [windows, taskscheduler, scheduled-tasks, automation]
---
# Windows Task Scheduler

Creating and managing scheduled tasks with PowerShell.

## Basic Task Creation

```powershell
# Simple trigger + action
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-File C:\scripts\cleanup.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "03:00AM"
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" `
    -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "DailyCleanup" `
    -Action $action -Trigger $trigger -Principal $principal
```

## Trigger Types

```powershell
# Once (one-shot)
$t = New-ScheduledTaskTrigger -Once -At "2025-01-01T00:00:00"

# Daily
$t = New-ScheduledTaskTrigger -Daily -At "03:00AM"

# Weekly
$t = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Friday -At "02:00"

# At startup
$t = New-ScheduledTaskTrigger -AtStartup

# At logon
$t = New-ScheduledTaskTrigger -AtLogOn -User "DOMAIN\User"

# On event (event log ID)
$t = New-ScheduledTaskTrigger -EventId 1000 -EventSource "MyApp" -EventLog "Application"
```

## Management

```powershell
# List
Get-ScheduledTask
Get-ScheduledTask -TaskPath "\Microsoft\Windows\Docker\"
Get-ScheduledTask -TaskName "*Docker*"

# Enable/Disable
Enable-ScheduledTask -TaskName "MyTask"
Disable-ScheduledTask -TaskName "MyTask"

# Start (run now)
Start-ScheduledTask -TaskName "MyTask"

# Stop
Stop-ScheduledTask -TaskName "MyTask"

# Export/Import
Export-ScheduledTask -TaskName "MyTask" | Out-File "MyTask.xml"
Register-ScheduledTask -TaskName "MyTask" -Xml (Get-Content "MyTask.xml" -Raw)
```

## Task Deletion

```powershell
Unregister-ScheduledTask -TaskName "MyTask" -Confirm:$false
```

## Pitfalls

- **RunLevel Highest** required for admin operations, even if running as admin
- **Task Scheduler** can hide tasks with trailing backslash in TaskPath
- **Export** preserves credentials if stored -- sanitize before sharing
- **Start-ScheduledTask** is async -- doesn't wait for completion
- **Repetition** triggers need `RepetitionInterval` and `RepetitionDuration`
