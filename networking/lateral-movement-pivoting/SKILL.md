---
name: lateral-movement-pivoting
description: "Use when moving laterally in compromised networks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [lateral-movement, pivoting, pass-the-hash, psexec, WMI, SSH-tunnel, proxy]
    related_skills: [privilege-escalation-techniques, active-directory-pentesting, port-redirection-tunneling, command-control-c2-infrastructure]
---

# Lateral Movement and Pivoting

Moving laterally through compromised networks — from pass-the-hash and pass-the-ticket through PsExec, WMI, SSH tunneling, and SOCKS proxying.

## When to Use

- Moving from initial foothold to other network segments
- Pivoting through compromised hosts to reach restricted networks
- Using harvested credentials for lateral access
- Establishing persistent access across multiple systems

## Lateral Movement Techniques

```python
LATERAL_TECHNIQUES = {
    'psexec': 'Execute commands remotely via SVCCTL (admin$ share)',
    'wmi': 'Execute via WMI (wmic /node: process call create)',
    'winrm': 'WinRM/PSRemoting — remote PowerShell execution',
    'schtasks': 'Create remote scheduled tasks for execution',
    'dcom': 'DCOM (MMC20.Application, ShellWindows, ShellBrowserWindow)',
    'smb_exec': 'SC.exe to create remote service on target',
    'pass_the_hash': 'Use NTLM hash directly (no password needed) for WMI/SMB',
    'pass_the_ticket': 'Use Kerberos TGS/TGT for remote access',
    'overpass_the_hash': 'NTLM hash → Kerberos TGT → TGS for service access',
}

# Pivoting with SSH
SSH_TUNNELS = {
    'local': "ssh -L 8080:internal-server:80 jumpbox — forward port through jumpbox",
    'remote': "ssh -R 8080:localhost:80 attacker-server — expose internal service",
    'dynamic': "ssh -D 9050 jumpbox — SOCKS5 proxy through jumpbox",
    'proxyjump': "ssh -J jumpbox target-internal — chain through jump host",
}

class PivotProxy:
    """Set up SOCKS proxy for pivoting."""
    def __init__(self, jump_host: str, port: int = 9050):
        self.jump = jump_host
        self.port = port
```

## Verification Checklist

- [ ] Initial foothold established (user-level access)
- [ ] Credentials harvested (plaintext, hashes, tickets)
- [ ] Lateral movement technique chosen (PsExec, WMI, WinRM, SCM)
- [ ] Pass-the-hash/ticket working across targets
- [ ] Pivot proxy set up (SOCKS/SSH tunnel)
- [ ] New targets enumerated through pivot
- [ ] No detection by blue team (slowed down, not stopped)
- [ ] Cleanup: remove remote services, binaries, event logs (if in scope)
