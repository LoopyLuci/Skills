---
name: powershell-rest-api
description: "Use when calling REST APIs from PowerShell."
category: software-development
tags: [powershell, rest, api, web, invoke-restmethod]
---
# PowerShell REST API

Calling REST APIs from PowerShell.

## Basic Requests

```powershell
# GET request
$response = Invoke-RestMethod -Uri "https://api.github.com/repos/user/repo"
$response.stargazers_count

# GET with headers
$headers = @{ Authorization = "Bearer $env:GITHUB_TOKEN" }
$response = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers

# POST with JSON body
$body = @{ name = "new-repo"; description = "Created via API" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

## Common Methods

```powershell
# PUT (update resource)
Invoke-RestMethod -Uri "https://api.example.com/items/1" `
    -Method Put -Body ($data | ConvertTo-Json) -ContentType "application/json"

# PATCH (partial update)
Invoke-RestMethod -Uri "https://api.example.com/items/1" `
    -Method Patch -Body '{"status": "active"}' -ContentType "application/json"

# DELETE
Invoke-RestMethod -Uri "https://api.example.com/items/1" -Method Delete -Headers $headers
```

## Authentication

```powershell
# Basic auth
$pair = "$($cred.UserName):$($cred.GetNetworkCredential().Password)"
$encoded = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
$headers = @{ Authorization = "Basic $encoded" }

# Bearer token
$headers = @{ Authorization = "Bearer $token" }

# API Key
$headers = @{ "X-API-Key" = $apiKey }

# Cookie-based
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$cookie = New-Object System.Net.Cookie("session", $sessionId, "/", "example.com")
$session.Cookies.Add($cookie)
Invoke-RestMethod -Uri "https://example.com/api" -WebSession $session
```

## Error Handling

```powershell
try {
    $response = Invoke-RestMethod -Uri "https://api.example.com/data" -ErrorAction Stop
} catch [System.Net.WebException] {
    $statusCode = $_.Exception.Response.StatusCode
    $stream = $_.Exception.Response.GetResponseStream()
    $reader = New-Object System.IO.StreamReader($stream)
    $errorBody = $reader.ReadToEnd()
    Write-Error "HTTP $statusCode : $errorBody"
} catch {
    Write-Error "Request failed: $_"
}
```

## Pagination

```powershell
# GitHub-style pagination (Link header)
$uri = "https://api.github.com/user/repos?per_page=100"
$allRepos = @()
while ($uri) {
    $response = Invoke-WebRequest -Uri $uri -Headers $headers
    $repos = $response.Content | ConvertFrom-Json
    $allRepos += $repos
    # Parse Link header for next page
    if ($response.Headers.Link -match '<([^>]+)>;\s*rel="next"') {
        $uri = $matches[1]
    } else { $uri = $null }
}
```

## Polling Pattern

```powershell
do {
    $status = Invoke-RestMethod -Uri "https://api.example.com/jobs/$jobId"
    Write-Host "Status: $($status.state)"
    Start-Sleep -Seconds 5
} while ($status.state -eq 'running')

if ($status.state -eq 'completed') {
    Write-Host "Job completed: $($status.result)"
} else {
    Write-Error "Job failed: $($status.error)"
}
```

## Pitfalls

- Invoke-RestMethod returns parsed objects; Invoke-WebRequest returns raw HTTP response
- Default timeout is 100 seconds -- use `-TimeoutSec` for longer operations
- TLS 1.2 required for most modern APIs: `[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12`
- Proxy issues: `$env:HTTP_PROXY` or `-Proxy` parameter
- Rate limiting: check response headers for remaining quota
