---
name: security-incident-response
description: "Use when building incident response and security operations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [incident-response, security-operations, SOC, forensics, threat-hunting, IR]
    related_skills: [waf-web-application-firewall, network-forensics-analysis, ddos-mitigation-strategies, identity-access-management]
---

# Security Incident Response

Building incident response capabilities — from preparation and detection through containment, eradication, recovery, and post-mortem analysis.

## When to Use

- Setting up a CSIRT (Computer Security Incident Response Team)
- Responding to security breaches and incidents
- Building incident response playbooks
- Conducting post-incident analysis
- Improving security posture through lessons learned

## Incident Response Lifecycle

```python
IR_LIFECYCLE = {
    'preparation': 'Tools, playbooks, training, communication plans',
    'detection_and_analysis': 'Monitoring, alerts, triage, investigation',
    'containment': 'Short-term (isolate) and long-term (system rebuild)',
    'eradication': 'Remove threat, patch vulnerabilities',
    'recovery': 'Restore systems, monitor for reinfection',
    'post_mortem': 'Root cause, lessons learned, improvements',
}

IR_SEVERITY = {
    'SEV1': 'Critical — active data breach, ransomware, full system compromise',
    'SEV2': 'High — confirmed intrusion, malware outbreak, denial of service',
    'SEV3': 'Medium — suspicious activity, single workstation compromise',
    'SEV4': 'Low — phishing reports, policy violations, low-risk alerts',
}

class IncidentHandler:
    """Track and manage security incidents."""
    def __init__(self, name: str, severity: str):
        self.name = name
        self.severity = severity
        self.timeline = []
        self.actions = []
        self.status = 'detected'
    
    def add_action(self, action: str, owner: str, timestamp: str = None):
        import datetime
        self.actions.append({
            'action': action, 'owner': owner,
            'timestamp': timestamp or datetime.datetime.now().isoformat(),
        })
    
    def generate_report(self) -> str:
        report = f"🛡️ Incident Report: {self.name} ({self.severity})\n" + "=" * 50 + "\n"
        for a in self.actions:
            report += f"\n{a['timestamp'][:19]} — {a['action']} ({a['owner']})"
        report += f"\n\nStatus: {self.status}\n"
        return report
```

## Common Pitfalls

1. **No playbooks** — improvising during a breach wastes time; have documented procedures
2. **Not isolating fast enough** — malware spreads in minutes; containment is priority #1
3. **Skipping forensics** — wiping systems before forensic analysis destroys evidence
4. **Poor communication** — stakeholders (legal, PR, exec, customers) need timely updates
5. **No post-mortem** — repeating same mistakes because causes weren't documented

## Verification Checklist

- [ ] Incident response plan documented and reviewed
- [ ] Playbooks for common scenarios (ransomware, data breach, DDoS)
- [ ] Severity definitions clear (SEV1/2/3/4)
- [ ] Communication templates (internal, customer, regulatory, PR)
- [ ] Forensic tools available and tested
- [ ] Backup restoration tested (not just backups exist)
- [ ] Post-mortem conducted within 2 weeks of any SEV1/2 incident
- [ ] Lessons learned tracked and improvements implemented
