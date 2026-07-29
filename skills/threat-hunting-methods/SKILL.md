---
name: threat-hunting-methods
description: "Use when implementing threat hunting and proactive security."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [threat-hunting, security, proactive, IoCs, TTPs, hypothesis, SIEM]
    related_skills: [security-incident-response, network-forensics-analysis, identity-access-management, anomaly-detection-ml]
---

# Threat Hunting Methods

Proactive threat hunting in networks and systems — from hypothesis-driven hunting through IoC/IoA detection, behavioral analysis, and threat intelligence integration.

## When to Use

- Proactively searching for threats missed by automated detection
- Investigating suspicious activity patterns
- Building threat hunting hypotheses from intelligence
- Analyzing logs, network traffic, and endpoints for compromise
- Reducing dwell time (time from compromise to detection)

## Hunting Process

```python
HUNTING_PROCESS = {
    'hypothesis': 'Form hypothesis based on threat intel, TTPs, or anomalies',
    'collect': 'Gather relevant data (logs, network, endpoints, DNS, process)',
    'analyze': 'Apply analytics, pattern matching, or ML to find evidence',
    'investigate': 'Deep-dive into findings to confirm or disprove hypothesis',
    'respond': 'Contain, eradicate, and create detection rules for confirmed threats',
}

class ThreatHunter:
    """Conduct threat hunting investigations."""
    
    HUNTING_TACTICS = [
        'DNS query anomalies — look for DGA domains, beaconing patterns',
        'Unusual outbound connections — unexpected protocols or destinations',
        'Process chain anomalies — office apps spawning cmd/powershell',
        'Lateral movement — anomalous RDP, SMB, WinRM connections',
        'Privilege escalation — unexpected service creation, scheduled tasks',
        'Data exfiltration — large outbound transfers, unusual times',
        'Credential access — excessive failed logins, LSASS dumps',
        'Persistence mechanisms — new services, run keys, startup items',
    ]
    
    def investigate_ioc(self, ip: str = None, domain: str = None, 
                        hash: str = None) -> Dict:
        """Investigate an Indicator of Compromise."""
        return {
            'ip': ip, 'domain': domain, 'hash': hash,
            'reputation': 'unknown',
            'related_indicators': [],
            'affected_assets': [],
            'recommendation': 'Isolate affected systems and investigate further',
        }
```

## Common Pitfalls

1. **No hypothesis** — random log searching wastes time; use intelligence-driven hunting
2. **Too much noise** — false positives overwhelm analysts; tune detection before hunting
3. **No automation** — manual hunting doesn't scale; automate common hypothesis checks
4. **Missing context** — hunts without asset criticality miss the most important threats
5. **No feedback loop** — hunt findings should improve automated detection rules

## Verification Checklist

- [ ] Threat intelligence feeds integrated and consumed
- [ ] Hunting hypotheses documented per quarter
- [ ] Automated hunting playbooks for common scenarios
- [ ] SIEM/analytics platform configured for hunting queries
- [ ] Hunt findings documented and shared with detection engineering
- [ ] Dwell time measured and tracked as KPI
- [ ] Purple team exercises conducted to validate detection and hunting
