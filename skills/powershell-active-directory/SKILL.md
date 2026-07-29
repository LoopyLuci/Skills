---
name: powershell-active-directory
description: "Use when managing AD via PowerShell."
category: software-development
tags: [powershell, active-directory, ad, domain, users]
---
# PowerShell Active Directory

Managing Active Directory with PowerShell.

## Prerequisites

```powershell
# Install RSAT tools (Windows 10/11)
Add-WindowsCapability -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0 -Online

# Import the module
Import-Module ActiveDirectory
```

## User Management

```powershell
# Get user
Get-ADUser -Identity jdoe
Get-ADUser -Filter { Name -like "John*" } -Properties Department, Title, Manager
Get-ADUser -SearchBase "OU=Staff,DC=contoso,DC=com" -Filter *

# Create user
New-ADUser -Name "John Doe" -GivenName John -Surname Doe `
    -SamAccountName jdoe -UserPrincipalName jdoe@contoso.com `
    -Title "Developer" -Department "Engineering" `
    -Path "OU=Staff,DC=contoso,DC=com" `
    -AccountPassword (ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force) `
    -Enabled $true

# Modify user
Set-ADUser -Identity jdoe -Title "Senior Developer" -Department "R&D"
Set-ADUser -Identity jdoe -Add @{ extensionAttribute1 = "DockerUser" }

# Enable/disable
Enable-ADAccount -Identity jdoe
Disable-ADAccount -Identity jdoe

# Remove
Remove-ADUser -Identity jdoe -Confirm:$false
```

## Group Management

```powershell
# Create group
New-ADGroup -Name "DockerUsers" -GroupScope Global `
    -GroupCategory Security -Path "OU=Groups,DC=contoso,DC=com"

# Add/remove members
Add-ADGroupMember -Identity "DockerUsers" -Members jdoe, asmith
Remove-ADGroupMember -Identity "DockerUsers" -Members asmith -Confirm:$false

# Get members
Get-ADGroupMember -Identity "DockerUsers" | Select-Object Name, SamAccountName

# Find groups for a user
Get-ADUser -Identity jdoe -Properties MemberOf | Select-Object -ExpandProperty MemberOf
```

## Computer Management

```powershell
# Find computers
Get-ADComputer -Filter { OperatingSystem -like "*Windows 10*" } -Properties OperatingSystem

# Get computer details
Get-ADComputer -Identity WS-001 -Properties *

# Computer last logon
Get-ADComputer -Filter * -Properties LastLogonDate |
    Where-Object { $_.LastLogonDate -lt (Get-Date).AddDays(-90) }
```

## Organizational Units

```powershell
# Create OU
New-ADOrganizationalUnit -Name "Servers" -Path "DC=contoso,DC=com"

# Move object
Move-ADObject -Identity "CN=jdoe,CN=Users,DC=contoso,DC=com" `
    -TargetPath "OU=Staff,DC=contoso,DC=com"
```

## Reports

```powershell
# Export all users
Get-ADUser -Filter * -Properties Department, Title, LastLogonDate |
    Select-Object Name, SamAccountName, Department, Title, LastLogonDate |
    Export-Csv "ad-users.csv" -NoTypeInformation

# Disabled users report
Get-ADUser -Filter { Enabled -eq $false } |
    Select-Object Name, SamAccountName, LastLogonDate
```

## Pitfalls

- AD module requires RSAT or runs on Domain Controller
- Filter uses PowerShell syntax, not LDAP -- but is converted internally
- Bulk operations need careful throttling (1000+ at a time)
- Password must meet domain password policy
- `-Confirm:$false` skips confirmation prompts -- use with caution
