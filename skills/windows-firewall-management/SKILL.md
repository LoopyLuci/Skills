---
name: windows-firewall-management
description: "Use when configuring Windows Firewall via PowerShell."
category: software-development
tags: [windows, firewall, networking, security, powershell]
---
# Windows Firewall Management

Configuring Windows Defender Firewall with PowerShell.

## Rules Overview

```powershell
# List all rules
Get-NetFirewallRule | Select-Object DisplayName, Enabled, Direction, Action

# Rules by profile
Get-NetFirewallRule -Profile Domain, Private
Get-NetFirewallRule -Profile Public

# Rules by direction
Get-NetFirewallRule -Direction Inbound
Get-NetFirewallRule -Direction Outbound
```

## Allow/Block Ports

```powershell
# Allow inbound port 8080
New-NetFirewallRule -DisplayName "Allow Web App 8080" `
    -Direction Inbound -Protocol TCP -LocalPort 8080 `
    -Action Allow -Profile Any

# Block inbound port 23 (Telnet)
New-NetFirewallRule -DisplayName "Block Telnet" `
    -Direction Inbound -Protocol TCP -LocalPort 23 `
    -Action Block

# Allow port range
New-NetFirewallRule -DisplayName "Docker Swarm" `
    -Direction Inbound -Protocol TCP `
    -LocalPort 2377,7946,4789 `
    -Action Allow

# Allow with remote IP restriction
New-NetFirewallRule -DisplayName "Admin SSH" `
    -Direction Inbound -Protocol TCP -LocalPort 22 `
    -RemoteAddress 192.168.1.0/24,10.0.0.0/8 `
    -Action Allow
```

## Allow Programs

```powershell
# Allow a program through firewall
New-NetFirewallRule -DisplayName "Docker Desktop" `
    -Direction Inbound -Program "C:\Program Files\Docker\Docker\Docker Desktop.exe" `
    -Action Allow
```

## Enable/Disable

```powershell
# Enable/disable a rule
Enable-NetFirewallRule -DisplayName "Docker Swarm"
Disable-NetFirewallRule -DisplayName "Block Telnet"

# Remove a rule
Remove-NetFirewallRule -DisplayName "Allow Web App 8080"

# Enable firewall itself
Set-NetFirewallProfile -Profile Domain,Private,Public -Enabled True
```

## Logging

```powershell
# Enable logging
Set-NetFirewallProfile -Profile All -LogAllowed True -LogBlocked True `
    -LogFileName "%SystemRoot%\System32\LogFiles\Firewall\pfirewall.log" `
    -LogMaxSizeKilobytes 4096

# View logs
Get-Content "$env:SystemRoot\System32\LogFiles\Firewall\pfirewall.log" -Tail 50
```

## Pitfalls

- Rules with same DisplayName overwrite -- use unique names
- RemoteAddress can be IP, subnet, or range -- not hostnames
- `-Action Block` rules take precedence over `-Action Allow` rules
- Default inbound policy blocks, outbound allows
