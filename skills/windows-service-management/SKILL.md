---
name: windows-service-management
description: "Use when managing Windows services via PS/batch."
category: software-development
tags: [windows, services, powershell, service-control]
---
# Windows Service Management

Managing Windows services with PowerShell and batch.

## PowerShell Commands

```powershell
# List
Get-Service                              # all services
Get-Service | Where-Object { $_.Status -eq 'Running' }
Get-Service -Name docker*                # wildcard

# Lifecycle
Start-Service -Name docker
Stop-Service -Name docker -Force
Restart-Service -Name docker
Suspend-Service -Name docker             # pause
Resume-Service -Name docker

# Startup type
Set-Service -Name docker -StartupType Automatic
Set-Service -Name docker -StartupType Manual
Set-Service -Name docker -StartupType Disabled

# Create
New-Service -Name MyService -BinaryPathName "C:\path\app.exe --service" `
    -DisplayName "My Service" -StartupType Automatic `
    -Description "My custom service"

# Delete
sc.exe delete MyService
```

## sc.exe (batch-compatible)

```batch
sc query MyService
sc queryex MyService
sc start MyService
sc stop MyService
sc config MyService start= auto|demand|disabled
sc failure MyService reset= 86400 actions= restart/5000
sc create MyService binPath= "C:\path\app.exe --service" start= auto
sc delete MyService
```

## Failure Actions

```powershell
# Set restart on failure
sc.exe failure MyService reset= 86400 actions= restart/5000/restart/10000/reboot/60000

# View failure config
sc.exe qfailure MyService
sc.exe qfailureflag MyService
```

## Service Dependencies

```powershell
# Set dependency on another service
sc.exe config MyService depend= Docker

# View dependencies
Get-Service -Name Docker -DependentServices
Get-Service -Name Docker -RequiredServices
```

## Pitfalls

- **sc.exe** `=` must have space after it: `start= auto` (not `start=auto`)
- **Stop-Service -Force** sends STOP control even to services that don't accept it
- **Set-Service -StartupType Disabled** prevents manual start too
- **Failure actions** only apply to services configured with `sc failure`
- **Service accounts** -- use `VirtualAccount` or `ManagedServiceAccount` over local user
