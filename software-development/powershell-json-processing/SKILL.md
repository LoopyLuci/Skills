---
name: powershell-json-processing
description: "Use when processing JSON data in PowerShell."
category: software-development
tags: [powershell, json, parsing, api]
---
# PowerShell JSON Processing

Working with JSON data in PowerShell.

## Parsing

```powershell
# From string
$json = '{"name":"test","values":[1,2,3]}'
$obj = $json | ConvertFrom-Json
$obj.name          # "test"
$obj.values[0]     # 1

# From file
$config = Get-Content "config.json" -Raw | ConvertFrom-Json

# From API
$response = Invoke-RestMethod -Uri "https://api.github.com/repos/user/repo"
$response.stargazers_count
```

## Creating

```powershell
$obj = [PSCustomObject]@{
    Name   = "Test"
    Values = @(1, 2, 3)
    Nested = @{ Key = "Value" }
}
$json = $obj | ConvertTo-Json -Depth 5
```

## Depth (Critical!)

```powershell
# Default Depth is 2 -- deep objects get truncated!
$obj = [PSCustomObject]@{
    Level1 = [PSCustomObject]@{
        Level2 = [PSCustomObject]@{ Level3 = "deep" }
    }
}
$obj | ConvertTo-Json               # Level3 MIA
$obj | ConvertTo-Json -Depth 5      # Level3 present
```

## Pretty vs Compact

```powershell
# Pretty (default)
$data | ConvertTo-Json -Depth 5

# Compact (one line, for files/API)
$data | ConvertTo-Json -Depth 5 -Compress
```

## Select-Object with JSON

```powershell
# Convert nested JSON to flat objects
$repos = Invoke-RestMethod "https://api.github.com/users/octocat/repos"
$repos | Select-Object name, full_name, @{
    Name = "Stars"; Expression = { $_.stargazers_count }
}
```

## Common Patterns

```powershell
# Read config with defaults
$cfgPath = "config.json"
$defaults = @{ host = "localhost"; port = 8080 }
$config = if (Test-Path $cfgPath) {
    Get-Content $cfgPath -Raw | ConvertFrom-Json
} else { $defaults }

# Modify JSON and save
$config = Get-Content "data.json" -Raw | ConvertFrom-Json
$config | Add-Member -NotePropertyName "newProp" -NotePropertyValue "value"
$config | ConvertTo-Json -Depth 5 | Out-File "data.json" -Encoding UTF8

# Merge deep objects
$merged = [PSCustomObject]$config1.PSObject.Properties.ForEach({
    $key = $_.Name; [PSCustomObject]@{ $key = $config2.$key ?? $_.Value }
})
```

## Pitfalls

- **Default Depth=2** truncates deep objects -- always set -Depth for complex structures
- **ConvertFrom-Json** needs **-Raw** or it parses line-by-line (array corruption)
- **PSCustomObject** property order is insertion order in PS 7+, but alphabetical in PS 5.1
- **Large JSON** can hit memory limits -- use streaming with JsonTextReader for >100MB
- **Boolean/numbers** -- JSON true becomes $true, 42 becomes [int]42
