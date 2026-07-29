---
name: windows-env-variable-mgmt
description: "Use when managing Windows PATH and environment variables."
category: software-development
tags: [windows, environment, path, env-vars, powershell]
---
# Windows Environment Variable Management

Managing PATH and environment variables on Windows.

## Scopes

| Scope | Visibility | Admin Needed | Storage |
|-------|-----------|-------------|---------|
| Process | Current process only | No | Memory |
| User | Current user | No | HKCU\Environment |
| Machine | All users | Yes | HKLM\SYSTEM\CurrentControlSet |

## Reading

```powershell
# Process scope (current session)
$env:PATH
$env:DOCKER_HOST

# User scope
[Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::GetEnvironmentVariable('DOCKER_HOST', 'User')

# Machine scope
[Environment]::GetEnvironmentVariable('PATH', 'Machine')

# All scopes with fallback
[Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::GetEnvironmentVariable('PATH', 'Machine')
$env:PATH  # combines User + Machine
```

## Writing

```powershell
# Process scope (temporary, current session only)
$env:MY_VAR = "value"

# User scope (persistent)
[Environment]::SetEnvironmentVariable('MY_VAR', 'value', 'User')

# Machine scope (persistent, needs admin)
[Environment]::SetEnvironmentVariable('MY_VAR', 'value', 'Machine')

# Delete
[Environment]::SetEnvironmentVariable('MY_VAR', $null, 'User')
```

## PATH Manipulation

```powershell
# Add to User PATH (idempotent)
$scope = 'User'
$path = [Environment]::GetEnvironmentVariable('PATH', $scope)
$newEntry = "C:\MyApp\bin"
if ($path -split ';' -notcontains $newEntry) {
    $path = $newEntry + ';' + $path
    [Environment]::SetEnvironmentVariable('PATH', $path, $scope)
}

# Remove Docker from PATH
$path = [Environment]::GetEnvironmentVariable('PATH', 'User')
$newPath = ($path -split ';' | Where-Object { $_ -notmatch '(?i)docker' }) -join ';'
[Environment]::SetEnvironmentVariable('PATH', $newPath, 'User')
```

## Docker Env Vars to Remove

```powershell
$dockerVars = @('DOCKER_HOST','DOCKER_CERT_PATH','DOCKER_TLS_VERIFY',
                'DOCKER_CONFIG','DOCKER_CONTEXT','DOCKER_API_VERSION')
foreach ($ev in $dockerVars) {
    [Environment]::SetEnvironmentVariable($ev, $null, 'User')
    [Environment]::SetEnvironmentVariable($ev, $null, 'Machine')
}
```

## Broadcast Change (Notify Windows)

```powershell
# After changing environment, notify running apps
$HWND_BROADCAST = 0xFFFF
$WM_SETTINGCHANGE = 0x001A
[User32.SendMessage]::SendMessage($HWND_BROADCAST, $WM_SETTINGCHANGE, 0, 'Environment')
```

## Pitfalls

- **Machine scope** requires admin -- use try/catch
- **PATH is cached** per process -- new processes pick up changes
- **`$env:PATH`** only shows Process scope (User+Machine combined at logon)
- **String length limit** -- PATH has ~2048 char limit in older Windows
- **%VARIABLE%** in PATH entries are expanded; set with `REG_EXPAND_SZ` type
- **`[Environment]::SetEnvironmentVariable`** with Machine scope auto-broadcasts
