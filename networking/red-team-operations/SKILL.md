---
name: red-team-operations
description: "Use when planning and executing red team operations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [red-team, C2, evasion, opsec, stealth, persistent-access, breach-sim]
    related_skills: [penetration-testing-methodology, command-control-c2-infrastructure, lateral-movement-pivoting, evasion-techniques-av-bypass]
---

# Red Team Operations

Planning and executing red team operations — from campaign objectives through C2 infrastructure, operational security, evasion, and reporting.

## When to Use

- Simulating advanced persistent threat (APT) tactics
- Testing detection and response capabilities
- Executing multi-stage attack campaigns
- Building C2 infrastructure
- Stealth operations and evasion

## Red Team Phases

```python
RED_TEAM_PHASES = {
    'objective_definition': 'Define campaign goals (data exfil, lateral movement, persistence)',
    'infrastructure_setup': 'C2 servers, redirectors, domains, certificates — opsec separation',
    'initial_access': 'Phishing, web app exploitation, supply chain, physical',
    'establish_beachhead': 'C2 callback, persistence, host enumeration',
    'lateral_movement': 'Pass-the-hash, pass-the-ticket, PSRemoting, WMI, DCOM',
    'objective_completion': 'Data exfiltration, ransomware simulation, or access demonstration',
    'cleanup': 'Remove artifacts, restore systems, debrief with blue team',
}

class RedTeamCampaign:
    """Plan and track red team operations."""
    def __init__(self, name: str, objective: str):
        self.name = name
        self.objective = objective
        self.phases = []
        self.indicators = []
    
    def add_indicator(self, ioc_type: str, value: str, 
                       lifetime_hours: int = 48):
        self.indicators.append({
            'type': ioc_type, 'value': value,
            'lifetime': lifetime_hours, 'burned': False,
        })
```

## Verification Checklist

- [ ] Campaign objectives defined and documented
- [ ] Rules of engagement signed (what is in/out of bounds)
- [ ] C2 infrastructure deployed (domain fronting, redirectors, CDN)
- [ ] Operational security (opsec) measures in place
- [ ] Stealth techniques: process injection, living-off-the-land
- [ ] Blue team detection time measured
- [ ] No data exfiltrated (simulated exfil only)
- [ ] Cleanup completed (all implants removed)
- [ ] Debrief conducted with findings for blue team improvement
