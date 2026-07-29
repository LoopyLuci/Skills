---
name: powershell-module-creation
description: "Use when creating and publishing PowerShell modules."
category: software-development
tags: [powershell, module, psm1, psd1, publishing]
---
# PowerShell Module Creation

Creating, structuring, and publishing PowerShell modules.

## Module Structure

```
MyModule/
  MyModule.psd1    # Module manifest (required)
  MyModule.psm1    # Module script (core logic)
  en-US/
    about_MyModule.help.txt  # Help files
  Tests/
    MyModule.Tests.ps1       # Pester tests
```

## Module Manifest (.psd1)

```powershell
@{
    RootModule           = 'MyModule.psm1'
    ModuleVersion        = '1.0.0'
    GUID                 = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
    Author               = 'Your Name'
    CompanyName          = 'Your Company'
    Copyright            = '(c) 2024. All rights reserved.'
    Description          = 'Module for managing Docker environments'
    PowerShellVersion    = '5.1'
    CompatiblePSEditions = @('Desktop', 'Core')
    # Functions to export (empty = export nothing; * = export all)
    FunctionsToExport    = @('Get-DockerInfo', 'Remove-Docker')
    CmdletsToExport      = @()
    VariablesToExport    = @()
    AliasesToExport      = @()
    # Required modules
    RequiredModules      = @()
    # Tag for PSGallery
    PrivateData = @{
        PSData = @{
            Tags       = @('docker', 'windows', 'cleanup')
            ProjectUri = 'https://github.com/user/MyModule'
            LicenseUri = 'https://opensource.org/licenses/MIT'
        }
    }
}
```

## Module Script (.psm1)

```powershell
# Load helper functions
$public = Join-Path $PSScriptRoot 'Public'
$private = Join-Path $PSScriptRoot 'Private'

# Dot-source public functions
Get-ChildItem "$public\*.ps1" -ErrorAction SilentlyContinue | 
    ForEach-Object { . $_.FullName }

# Dot-source private functions
Get-ChildItem "$private\*.ps1" -ErrorAction SilentlyContinue |
    ForEach-Object { . $_.FullName }

# Export only public functions
Export-ModuleMember -Function (Get-ChildItem "$public\*.ps1" | ForEach-Object { $_.BaseName })
```

## Installing

```powershell
# Local (developer)
Import-Module .\MyModule\MyModule.psd1 -Force

# From PSGallery
Publish-Module -Name MyModule -NuGetApiKey $key

# Install from PSGallery
Install-Module -Name MyModule -Scope CurrentUser

# Update
Update-Module -Name MyModule
```

## Pitfalls

- **Module version** must increment for PSGallery updates
- **FunctionsToExport** controls what callers see -- empty = nothing, * = everything
- **$PSScriptRoot** inside modules points to module directory
- **Manifest GUID** should be unique per module; generate with `[guid]::NewGuid()`
- **Class-based modules** can't use dot-sourcing pattern -- define classes in .psm1 directly
