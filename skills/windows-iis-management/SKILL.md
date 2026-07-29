---
name: windows-iis-management
description: "Use when managing IIS via PowerShell."
category: software-development
tags: [windows, iis, web-server, powershell, administration]
---
# Windows IIS Management

Managing IIS Web Server with PowerShell.

## Install IIS

```powershell
# Install IIS features
Install-WindowsFeature -Name Web-Server -IncludeManagementTools

# Specific features
Install-WindowsFeature -Name Web-WebServer, Web-Common-Http, `
    Web-Default-Doc, Web-Dir-Browsing, Web-Http-Errors, `
    Web-Static-Content, Web-Http-Redirect, `
    Web-Health, Web-Http-Logging, Web-Custom-Logging, `
    Web-Request-Monitor, Web-Stat-Compression, Web-Dyn-Compression, `
    Web-Security, Web-Filtering, Web-Basic-Auth, Web-Windows-Auth, `
    Web-Net-Ext45, Web-Asp-Net45, Web-ISAPI-Ext, Web-ISAPI-Filter, `
    Web-Mgmt-Console, Web-Mgmt-Service, Web-Scripting-Tools
```

## Website Management

```powershell
# Create website
New-Website -Name "MyApp" -Port 80 -HostHeader "myapp.local" `
    -PhysicalPath "C:\inetpub\wwwroot\myapp" `
    -ApplicationPool "MyAppPool"

# Start/Stop
Start-Website -Name "MyApp"
Stop-Website -Name "MyApp"

# List sites
Get-Website | Select-Object Name, State, PhysicalPath, Bindings

# Remove site
Remove-Website -Name "MyApp"
```

## Application Pools

```powershell
# Create pool
New-WebAppPool -Name "MyAppPool" -Force

# Configure pool
Set-ItemProperty -Path "IIS:\AppPools\MyAppPool" -Name managedRuntimeVersion -Value "v4.0"
Set-ItemProperty -Path "IIS:\AppPools\MyAppPool" -Name startMode -Value "AlwaysRunning"
Set-ItemProperty -Path "IIS:\AppPools\MyAppPool" -Name processModel.identityType -Value "ApplicationPoolIdentity"

# Start/Stop pool
Start-WebAppPool -Name "MyAppPool"
Stop-WebAppPool -Name "MyAppPool"
Restart-WebAppPool -Name "MyAppPool"

# List pools
Get-ChildItem IIS:\AppPools | Select-Object Name, State
```

## SSL Certificates

```powershell
# List certificates
Get-ChildItem Cert:\LocalMachine\My

# Bind SSL to site
New-Item -Path "IIS:\SslBindings\0.0.0.0!443" `
    -Thumbprint "ABC123DEF456..." `
    -SSLFlags 0

# Remove binding
Remove-Item -Path "IIS:\SslBindings\0.0.0.0!443" -Force
```

## URL Rewrite

```powershell
# Add URL rewrite rule
Add-WebConfigurationProperty -PSPath MACHINE/WEBROOT/APPHOST `
    -Location "MyApp" -Filter "system.webServer/rewrite/rules" `
    -Name "." -Value @{
        name = "Redirect to HTTPS"
        enabled = "true"
        stopProcessing = "true"
        match = @{ url = "(.*)" }
        conditions = @{
            input = "{HTTPS}"
            match = "off"
        }
        action = @{
            type = "Redirect"
            url = "https://{HTTP_HOST}/{R:1}"
            redirectType = "Permanent"
        }
    }
```

## Pitfalls

- IIS module (`WebAdministration`) must be imported: `Import-Module WebAdministration`
- Website path must exist before creating site
- Port 80/443 bindings require admin
- Application pool identity needs permissions on content folder
- SSL bindings need certificate thumbprint, not friendly name
