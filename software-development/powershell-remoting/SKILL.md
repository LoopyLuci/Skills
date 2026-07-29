---
name: powershell-remoting
description: "Use when managing remote machines via PowerShell Remoting."
category: software-development
tags: [powershell, remoting, winrm, pssession, remote]
---
# PowerShell Remoting

Managing remote machines via PowerShell Remoting (WinRM/PSSession).

## One-Off Commands

```powershell
# Single machine
Invoke-Command -ComputerName SERVER01 -ScriptBlock { Get-Service -Name docker }

# Multiple machines
Invoke-Command -ComputerName SERVER01, SERVER02 -ScriptBlock { Get-Process | Sort-Object CPU -Descending | Select -First 5 }

# With credentials
$cred = Get-Credential
Invoke-Command -ComputerName SERVER01 -Credential $cred -ScriptBlock { Get-EventLog -LogName Application -Newest 10 }
```

## Persistent Sessions (PSSession)

```powershell
# Create session
$session = New-PSSession -ComputerName SERVER01 -SessionOption (New-PSSessionOption -IdleTimeout 3600000)

# Run multiple commands in same session (state persists)
Invoke-Command -Session $session -ScriptBlock { $data = @() }
Invoke-Command -Session $session -ScriptBlock { $data += Get-Process }
Invoke-Command -Session $session -ScriptBlock { $data.Count }

# Enter interactive session
Enter-PSSession -Session $session

# Disconnect (for long-running tasks)
Disconnect-PSSession -Session $session

# Reconnect later
Connect-PSSession -InstanceId $session.InstanceId

# Remove session
Remove-PSSession -Session $session
```

## Background Jobs on Remote

```powershell
# Start a job on remote machine
$job = Invoke-Command -ComputerName SERVER01 -ScriptBlock {
    Start-Sleep 60
    Get-Process
} -AsJob

# Check status & get results
$job | Wait-Job | Receive-Job
```

## File Transfer

```powershell
# Copy to remote
Copy-Item -Path "C:\local\script.ps1" -Destination "C:\remote\script.ps1" -ToSession $session

# Copy from remote
Copy-Item -Path "C:\remote\results.csv" -Destination "C:\local\results.csv" -FromSession $session
```

## Enable PSRemoting (Admin)

```powershell
# On target machine (one-time setup)
Enable-PSRemoting -Force

# Check if enabled
Test-WSMan SERVER01

# Set trusted hosts (for non-domain/workgroup)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "SERVER01,SERVER02" -Force

# WinRM config
winrm quickconfig
winrm set winrm/config/winrs '@{MaxMemoryPerShellMB="2048"}'
```

## Pitfalls

- **WinRM** needs port 5985 (HTTP) or 5986 (HTTPS) open in firewall
- **Double-hop** -- credentials from one remote session can't authenticate to another resource without CredSSP
- **IdleTimeout** defaults to 15min; increase for long-running tasks
- **TrustedHosts** uses unencrypted auth -- use HTTPS in production
- **PowerShell Core** remoting works cross-platform (Linux to Windows and vice versa)
