# Windows Firewall Automation via PowerShell (asyncio)

Pattern for managing Windows Defender Firewall rules from Python using async subprocess.

## Core Pattern

```python
async def _run_powershell(script: str, timeout: int = 30) -> str:
    proc = await asyncio.create_subprocess_exec(
        "powershell.exe",
        "-NoProfile", "-NonInteractive", "-Command", script,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout
        )
        return stdout.decode("utf-8", errors="replace").strip()
    except asyncio.TimeoutError:
        proc.kill()
        return ""
```

## Common Operations

### Create a rule
```powershell
New-NetFirewallRule -DisplayName "SENTINEL_BlockApp" -Direction Outbound -Action Block -Program "C:\path\to\app.exe" -Profile Any
```

### Remove a rule
```powershell
Remove-NetFirewallRule -DisplayName "SENTINEL_BlockApp" -ErrorAction SilentlyContinue
```

### List managed rules
```powershell
Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*SENTINEL_*" } | Select DisplayName, Direction, Action, Enabled, Protocol, LocalPort, RemotePort, RemoteAddress, Program | ConvertTo-Json
```

### Get profile status
```powershell
Get-NetFirewallProfile | Select Name, Enabled, DefaultInboundAction, DefaultOutboundAction | ConvertTo-Json
```

### Enable/disable profile
```powershell
Set-NetFirewallProfile -Profile Public -Enabled $True
```

### Check service
```powershell
Get-Service -Name "MpsSvc" | Select Status | ConvertTo-Json
```

## Requirements

- **Administrator privileges** required for rule CRUD. Check with:
  ```powershell
  [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
  | ? IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
  ```
- `New-NetFirewallRule` will error with "Access is denied" (Win32 error 5) if not elevated.
- Query operations (list, get-status) work without elevation.
- All Sentinel-managed rules are prefixed with `SENTINEL_` for clean lifecycle management.

## Rule Templates

### Block application (inbound + outbound)
```python
# Outbound block
await add_rule("Block_App_Out", "outbound", "block", program_path=path)
# Inbound block
await add_rule("Block_App_In", "inbound", "block", program_path=path)
```

### Block port
```python
await add_rule("Block_Port_443_TCP", "inbound", "block",
               protocol="TCP", local_port="443")
```

### Block IP
```python
# Inbound
await add_rule("Block_IP_1.2.3.4_In", "inbound", "block", remote_ip="1.2.3.4")
# Outbound
await add_rule("Block_IP_1.2.3.4_Out", "outbound", "block", remote_ip="1.2.3.4")
```

## Troubleshooting

- **Rule already exists**: `New-NetFirewallRule` errors with "Cannot ... already exists". Remove first, then recreate.
- **Access denied**: Run PowerShell as Administrator or elevate the Python process.
- **JSON parsing**: `ConvertTo-Json` may output single-object (not array) when only one rule matches. Check `isinstance(result, dict)` and normalize.
