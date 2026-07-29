---
name: bug-bounty-methodology
description: "Use when participating in bug bounty programs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [bug-bounty, vulnerability-disclosure, recon, HackerOne, Bugcrowd, triage]
    related_skills: [osint-reconnaissance-techniques, webapp-penetration-testing, api-penetration-testing, sql-injection-exploitation]
---

# Bug Bounty Methodology

Participating in bug bounty programs — from platform selection and recon through vulnerability discovery, report writing, and disclosure.

## When to Use

- Hunting bugs on HackerOne, Bugcrowd, or Intigriti
- Building a systematic bug hunting methodology
- Writing effective vulnerability reports
- Prioritizing targets and attack surfaces

## Bug Hunting Methodology

```python
BUG_BOUNTY_WORKFLOW = {
    'target_selection': 'Choose programs by scope, bounty range, response time, reputation',
    'recon': 'Subdomain enumeration, port scanning, technology fingerprinting, Wayback Machine',
    'automation': 'Nuclei templates, custom scripts for mass scanning',
    'manual_testing': 'Deep dive on interesting endpoints, business logic, auth flows',
    'exploitation': 'Validate PoC, maximize impact, chain vulnerabilities',
    'reporting': 'Clear, reproducible, triage-friendly report',
}

class BugBountyHunter:
    """Track bug bounty findings and earnings."""
    def __init__(self):
        self.findings = []
        self.total_earnings = 0.0
    
    def submit_finding(self, program: str, vulnerability: str, 
                        severity: str, payout: float = 0):
        self.findings.append({
            'program': program, 'vuln': vulnerability,
            'severity': severity, 'payout': payout,
        })
        self.total_earnings += payout
    
    def stats(self) -> Dict:
        return {
            'total_findings': len(self.findings),
            'total_earnings': self.total_earnings,
            'by_severity': {s: sum(1 for f in self.findings if f['severity'] == s)
                           for s in ['critical', 'high', 'medium', 'low', 'info']},
        }
```

## Verification Checklist

- [ ] Program scope reviewed (in/out, eligible domains, testing rules)
- [ ] Reconnaissance phase (subdomain enumeration, technology detection, endpoint discovery)
- [ ] Automated scanning (nuclei, custom tools)
- [ ] Manual testing on high-value targets (auth, payment, PII)
- [ ] Impact maximization (chaining vulnerabilities)
- [ ] Report written with reproducible steps
- [ ] Proof of concept ready (screenshots, requests, scripts)
- [ ] Disclosure timeline: report → triage → fix → public disclosure
- [ ] Program-specific rules followed (rate limits, testing times, no social engineering)
