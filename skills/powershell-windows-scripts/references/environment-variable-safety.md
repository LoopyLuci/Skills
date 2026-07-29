# Environment Variable Safety (PowerShell on Windows)

## Machine vs User Scope

| Scope | Requires Admin | Affects | Example |
|---|---|---|---|
| `User` | No | Current user only | `[EnvironmentVariableTarget]::User` |
| `Machine` | Yes | All users | `[EnvironmentVariableTarget]::Machine` |
| `Process` | No | Current process only | Default (no target) |

## Correct Reading Order

When checking a variable like DOCKER_HOST:

```powershell
# Process scope overrides User, which overrides Machine
$procVal = [Environment]::GetEnvironmentVariable('DOCKER_HOST', 'Process')
$userVal  = [Environment]::GetEnvironmentVariable('DOCKER_HOST', 'User')
$machVal  = [Environment]::GetEnvironmentVariable('DOCKER_HOST', 'Machine')
```

## PATH Manipulation

The PATH variable is a semicolon-delimited string. To remove Docker entries:

```powershell
$pathVar = [Environment]::GetEnvironmentVariable('Path', $target)
$newPath = ($pathVar -split ';' | Where-Object { $_ -notmatch '(?i)docker' }) -join ';'
```

**Always try/catch Machine-scope writes:**

```powershell
try {
    [Environment]::SetEnvironmentVariable('Path', $newPath, [EnvironmentVariableTarget]::Machine)
} catch {
    # Need admin - fall back gracefully
    Write-Host "Skipping Machine PATH (need admin)" -ForegroundColor Yellow
}
```

## Restore Point for Env Vars

Before modifying environment variables, create a snapshot:

```powershell
$snapshot = @{}
foreach ($var in @('DOCKER_HOST','DOCKER_CERT_PATH','DOCKER_TLS_VERIFY','DOCKER_CONFIG','DOCKER_CONTEXT')) {
    foreach ($scope in @('User','Machine')) {
        $val = [Environment]::GetEnvironmentVariable($var, $scope)
        if ($val) { $snapshot["${scope}:${var}"] = $val }
    }
}
```

## Pitfalls

- Reading PATH with `[Environment]::GetEnvironmentVariable` returns the raw string. Use `-split ';'` to iterate entries.
- The `Process` scope PATH is a **composite** of User + Machine at the time the shell started. Changing User or Machine scope does NOT affect the current process's PATH — a reboot or new process is needed.
- `[Environment]::SetEnvironmentVariable($null, $target)` does NOT remove a variable — use `[Environment]::SetEnvironmentVariable($var, $null, $target)` explicitly.
