---
name: penetration-testing-methodology
description: "Use when structuring penetration testing engagements."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pentest, methodology, PTES, OWASP, ethical-hacking, scope, reporting]
    related_skills: [vulnerability-assessment-scanning, webapp-penetration-testing, network-sniffing-packet-capture, bug-bounty-methodology]
---

# Penetration Testing Methodology

Structuring penetration testing engagements — from scoping and reconnaissance through exploitation, post-exploitation, and professional reporting.

## When to Use

- Planning and scoping a penetration test
- Executing a structured pentest methodology
- Writing professional pentest reports
- Understanding pentest phases and deliverables

## Pentest Phases

```python
PENTEST_PHASES = {
    'scoping': 'Define scope (IP ranges, URLs, apps), rules of engagement, exclusions',
    'reconnaissance': 'Passive (OSINT, DNS, WHOIS) and active (scanning, enumeration)',
    'vulnerability_analysis': 'Scanning, manual testing, configuration review, threat modeling',
    'exploitation': 'Validate vulnerabilities, gain initial access',
    'post_exploitation': 'Privilege escalation, lateral movement, data exfiltration testing',
    'reporting': 'Executive summary, findings (risk-ranked), remediation, evidence',
}

PENTEST_TYPES = {
    'black_box': 'No prior knowledge — simulates external attacker',
    'white_box': 'Full knowledge (source, credentials, architecture) — thorough assessment',
    'gray_box': 'Partial knowledge (limited credentials, documentation) — realistic insider',
    'covert': 'Stealth assessment — target doesn't know testing is happening',
}

class PentestEngagement:
    """Manage pentest engagement lifecycle."""
    def __init__(self, client: str, scope: Dict, type: str = 'gray_box'):
        self.client = client
        self.scope = scope
        self.type = type
        self.findings = []
        self.phase = 'scoping'
    
    def add_finding(self, name: str, severity: str, cvss: float,
                     description: str, remediation: str):
        self.findings.append({
            'name': name, 'severity': severity, 'cvss': cvss,
            'description': description, 'remediation': remediation,
        })
```

## Verification Checklist

- [ ] Rules of engagement documented and signed
- [ ] Scope clearly defined (what is in/out of scope)
- [ ] Authorization letter / penetration testing agreement in place
- [ ] Methodology followed (PTES, OWASP, OSSTMM, or custom)
- [ ] All phases completed (recon → analysis → exploitation → reporting)
- [ ] Findings risk-ranked (CVSS 1-10 or custom scoring)
- [ ] Remediation guidance provided per finding
- [ ] Report delivered with executive summary and technical appendix
- [ ] Data securely destroyed post-engagement
