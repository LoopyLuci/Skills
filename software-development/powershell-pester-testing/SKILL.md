---
name: powershell-pester-testing
description: "Use when unit-testing PowerShell with Pester."
category: software-development
tags: [powershell, testing, pester, unit-test, bdd]
---
# Pester Testing for PowerShell

Writing and running unit tests with Pester.

## Install

```powershell
Install-Module -Name Pester -Force -Scope CurrentUser
Import-Module Pester -PassThru
```

## Basic Test Structure

```powershell
# script.tests.ps1
BeforeAll {
    # Setup -- runs once before all tests
    . .\MyModule.psm1
    $testData = @(1, 2, 3)
}

Describe "Get-DockerInfo" {
    Context "When Docker is running" {
        BeforeEach {
            # Runs before each It block
            Mock Get-Service { return [PSCustomObject]@{ Status = 'Running' } }
        }

        It "Should return container count" {
            $result = Get-DockerInfo
            $result | Should -Not -BeNullOrEmpty
        }

        It "Should be a PSObject" {
            $result = Get-DockerInfo
            $result | Should -BeOfType [PSCustomObject]
        }
    }

    Context "When Docker is not running" {
        It "Should return null" {
            Mock Get-Service { return $null }
            $result = Get-DockerInfo
            $result | Should -BeNullOrEmpty
        }
    }
}

Describe "Format-FileSize" {
    It "Converts 0 bytes" {
        Format-FileSize 0 | Should -Be "0 B"
    }
    It "Converts 1 KB" {
        Format-FileSize 1024 | Should -Be "1.0 KB"
    }
    It "Converts 1 MB" {
        Format-FileSize 1048576 | Should -Be "1.00 MB"
    }
}

AfterAll {
    # Cleanup -- runs once after all tests
    Remove-Variable testData
}
```

## Mocking

```powershell
# Mock a command
Mock Get-Service { return [PSCustomObject]@{ Status = 'Running' } }

# Mock with parameters
Mock Get-Service {
    if ($Name -eq 'docker') { return [PSCustomObject]@{ Status = 'Running' } }
    return $null
} -ParameterFilter { $Name -eq 'docker' }

# Verify mock was called
Assert-MockCalled Get-Service -Times 1 -Exactly
Assert-MockCalled Get-Service -Times 0 -Exactly  # Should not have been called

# Mock with parameter filtering
Mock Remove-Item { throw "Access denied" } -ParameterFilter { $Path -match 'protected' }
```

## Running Tests

```powershell
# Run specific test file
Invoke-Pester -Script .\MyModule.Tests.ps1

# Run all tests in directory
Invoke-Pester -Path .\Tests\

# Output results
Invoke-Pester -Output Detailed
Invoke-Pester -Output NUnitXml -OutputFile results.xml

# Run specific Describe block
Invoke-Pester -Script .\MyModule.Tests.ps1 -TestName "Format-FileSize"
```

## CI Integration

```powershell
# PowerShell script for CI
$config = @{
    Run = @{ Path = ".\Tests\" }
    Output = @{ Verbosity = 'Detailed' }
    CodeCoverage = @{
        Enabled = $true
        Path = ".\source\*.ps1"
        OutputPath = ".\coverage.xml"
    }
}
$result = Invoke-Pester -Configuration $config
exit $result.FailedCount
```

## Pitfalls

- Pester v5+ has breaking changes from v4 -- check version
- `Should -Be` uses exact equality; use `Should -BeLike` for wildcards
- Mocks only work for commands the test file actually calls
- `BeforeAll` vs `BeforeEach` -- use BeforeAll for expensive setup
- Code coverage requires Pester v5 and PS 7+
