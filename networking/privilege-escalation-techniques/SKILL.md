---
name: privilege-escalation-techniques
description: "Use when escalating privileges on compromised systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [privilege-escalation, Windows, Linux, kernel-exploit, sudo, token, potato]
    related_skills: [active-directory-pentesting, lateral-movement-pivoting, web-shell-deployment, exploit-development-basics]
---

# Privilege Escalation Techniques

Escalating privileges on compromised systems — from Windows (token manipulation, potato attacks, service abuse) through Linux (SUID, sudo, capabilities, kernel exploits).

## When to Use

- Escalating from user to admin/root after initial access
- Identifying privilege escalation paths during pentests
- Exploiting misconfigured services and permissions
- Using automated enumeration tools

## Windows PrivEsc

```python
WINDOWS_PRIVESC = {
    'token_abuse': 'SeImpersonatePrivilege, SeAssignPrimaryToken — RoguePotato, SweetPotato',
    'service_abuse': 'Weak service permissions, unquoted service paths, writable binaries',
    'scheduled_tasks': 'Writable scheduled task scripts, modifiable task definitions',
    'dll_hijacking': 'Missing DLL in PATH, writable folders in DLL search order',
    'always_install_elevated': 'MSI files install as SYSTEM when registry keys are set',
    'unattend_files': 'Unattend.xml may contain admin credentials in plaintext',
    'registry_keys': 'AutoRun keys, Debugger keys, AlwaysInstallElevated',
}

LINUX_PRIVESC = {
    'sudo': 'Passwordless sudo entries, LD_PRELOAD, env_keep, vulnerable binaries',
    'suid': 'Find all SUID binaries with known vulnerabilities (GTFOBins)',
    'capabilities': 'Exploitable capabilities (cap_setuid, cap_sys_admin, cap_dac_override)',
    'kernel': 'Linux kernel exploits (CVE-2021-4034 PwnKit, CVE-2022-0847 DirtyPipe)',
    'cron': 'Writable cron scripts, wildcard injection, PATH abuse',
    'docker': 'User in docker group = root access via docker socket',
    'lxd': 'User in lxd group can mount host filesystem',
}

# Automated enumeration
AUTO_ENUM = {
    'linux': 'LinEnum.sh, LinPEAS, linux-smart-enumeration',
    'windows': 'WinPEAS, PowerUp.ps1, Seatbelt.exe, PowerSploit',
}
```

## Verification Checklist

- [ ] Automated enumeration scripts run (WinPEAS/LinPEAS)
- [ ] Current user privileges and groups identified
- [ ] Kernel/OS version checked for known exploits
- [ ] Service misconfigurations checked (writable binaries, unquoted paths)
- [ ] Scheduled tasks/cron jobs with abuse opportunities
- [ ] SUID/sudo/capabilities checked (Linux) or token/ACLs checked (Windows)
- [ ] Credentials hunted (config files, history, registry, browsers)
- [ ] Escalation path proven (not just identified)
- [ ] AV/EDR bypass considered during escalation
