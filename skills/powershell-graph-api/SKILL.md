---
name: powershell-graph-api
description: "Use when calling Microsoft Graph API from PowerShell."
category: software-development
tags: [powershell, graph, microsoft, api, azure, entra]
---
# Microsoft Graph API with PowerShell

Calling Microsoft Graph API from PowerShell.

## Authentication

```powershell
# Device code flow (interactive)
$body = @{
    client_id = "your-client-id"
    scope = "User.Read Mail.Read Files.Read.All"
} | ConvertTo-Json
$deviceCode = Invoke-RestMethod -Method Post `
    -Uri "https://login.microsoftonline.com/organizations/oauth2/v2.0/devicecode" `
    -Body $body -ContentType "application/json"
Write-Host $deviceCode.message  # User visits URL and enters code

# Poll for token
do {
    Start-Sleep -Seconds 5
    $token = Invoke-RestMethod -Method Post `
        -Uri "https://login.microsoftonline.com/organizations/oauth2/v2.0/token" `
        -Body @{
            grant_type = "urn:ietf:params:oauth:grant-type:device_code"
            client_id = "your-client-id"
            device_code = $deviceCode.device_code
        }
} until ($token.access_token)
```

## Basic Queries

```powershell
$headers = @{ Authorization = "Bearer $($token.access_token)" }
$base = "https://graph.microsoft.com/v1.0"

# Get current user
$me = Invoke-RestMethod -Uri "$base/me" -Headers $headers
$me.displayName

# Get user's messages
$messages = Invoke-RestMethod -Uri "$base/me/messages?`$top=10" -Headers $headers
$messages.value | Select-Object subject, receivedDateTime

# Get files from OneDrive
$files = Invoke-RestMethod -Uri "$base/me/drive/root/children" -Headers $headers
$files.value | Select-Object name, size, lastModifiedDateTime
```

## Using Graph PowerShell SDK

```powershell
# Install
Install-Module Microsoft.Graph -Scope CurrentUser

# Connect
Connect-MgGraph -Scopes "User.Read", "Mail.Read", "Files.Read.All"

# Get current user
Get-MgUser -UserId me | Select-Object DisplayName, Mail, UserPrincipalName

# List users
Get-MgUser -All -Top 100 | Select-Object DisplayName, UserPrincipalName

# Get messages
Get-MgUserMessage -UserId me -Top 10 | Select-Object Subject, ReceivedDateTime

# Get files
Get-MgUserDriveRootChild -UserId me | Select-Object Name, Size
```

## Common Tasks

```powershell
# Search for users
Get-MgUser -Search '"DisplayName:John"' -ConsistencyLevel eventual

# Send email
$body = @{
    message = @{
        subject = "Hello from Graph"
        body = @{ contentType = "Text"; content = "This is a test message" }
        toRecipients = @(@{ emailAddress = @{ address = "user@contoso.com" } })
    }
}
Send-MgUserMail -UserId me -BodyParameter $body

# Create team
New-MgTeam -DisplayName "New Team" -Description "Created via Graph API"
```

## Pitfalls

- Graph requires registered app in Azure AD/Entra ID
- Permissions are consented per-user or admin -- some need admin consent
- Pagination uses `@odata.nextLink` -- use `-All` flag in SDK
- Beta API endpoints differ from v1.0 -- check documentation
- SDK modules are large -- install only needed submodules (`Microsoft.Graph.Users`, etc.)
