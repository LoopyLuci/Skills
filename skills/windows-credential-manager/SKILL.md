---
name: windows-credential-manager
description: "Use when storing/retrieving credentials securely on Windows."
category: software-development
tags: [windows, credentials, secrets, security, vault]
---
# Windows Credential Manager

Storing and retrieving credentials securely on Windows.

## Credential Manager (Built-in)

```powershell
# Store a credential
$cred = Get-Credential
$cred | Export-CliXml -Path "C:\scripts\cred.xml"

# Load a credential (only same user can decrypt)
$cred = Import-CliXml -Path "C:\scripts\cred.xml"
$cred.UserName
$cred.GetNetworkCredential().Password
```

## Windows Credential Vault (cmdkey)

```batch
REM Add generic credential
cmdkey /add:MyServer /user:admin /pass:MyPassword

REM List
cmdkey /list

REM Delete
cmdkey /delete:MyServer
```

## PowerShell SecretManagement Module (PS 7+)

```powershell
# Install
Install-Module -Name Microsoft.PowerShell.SecretManagement -Force
Install-Module -Name Microsoft.PowerShell.SecretStore -Force

# Register vault
Register-SecretVault -Name MyVault -ModuleName Microsoft.PowerShell.SecretStore

# Store
Set-Secret -Name "DockerHubToken" -Secret "abc123"
Set-Secret -Name "DBCreds" -Secret (ConvertTo-SecureString "pass" -AsPlainText -Force)

# Retrieve
Get-Secret -Name "DockerHubToken"
Get-Secret -Name "DBCreds" | ConvertFrom-SecureString

# List
Get-Secret -Vault MyVault

# Remove
Remove-Secret -Name "DockerHubToken"
```

## CredSSP / Secure Strings

```powershell
# ConvertTo-SecureString with key (portable)
$key = (1..16)
$secure = ConvertTo-SecureString -String "MyPassword" -AsPlainText -Force
$encrypted = ConvertFrom-SecureString -SecureString $secure -Key $key
# Store $encrypted string in file
$encrypted | Out-File "pass.txt"
# Decrypt later
$secure = ConvertTo-SecureString -String (Get-Content "pass.txt") -Key $key
```

## Avoid Plain Text in Scripts

```powershell
# BAD: plain text in script
$password = "P@ssw0rd"

# GOOD: interactively prompt at runtime
$cred = Get-Credential

# GOOD: load from encrypted file
$cred = Import-CliXml -Path "cred.xml"
```

## Pitfalls

- **Export-CliXml** uses DPAPI -- only same user on same machine can decrypt
- **cmdkey** stores in plaintext (obfuscated, not encrypted) -- use with caution
- **SecretManagement** requires PS 7 and module installation
- **Get-Credential** can't be automated (always shows GUI prompt)
- **SecureString** in memory can still be dumped by malware running as same user
