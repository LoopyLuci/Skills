---
name: security-audit-standards
description: "Use when conducting security audits and assessments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security-audit, assessment, SOC2, ISO27001, penetration-testing, compliance]
    related_skills: [security-incident-response, vulnerability-scanning, identity-access-management, waf-web-application-firewall]
---

# Security Audit Standards

Conducting security audits and assessments — from SOC 2 and ISO 27001 through penetration testing, vulnerability assessments, and audit evidence collection.

## When to Use

- Preparing for SOC 2, ISO 27001, or PCI DSS audit
- Conducting internal security assessments
- Managing penetration tests and findings
- Building audit evidence and compliance documentation

## Audit Frameworks

```python
AUDIT_FRAMEWORKS = {
    'soc2': 'Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy)',
    'iso27001': 'ISMS — information security management, 114 controls over 14 domains',
    'pcidss': 'Payment Card Industry — 12 requirements for cardholder data',
    'hipaa': 'Healthcare — privacy and security of protected health information',
}

AUDIT_PHASES = [
    'Scope definition — what systems, processes, and teams are in scope',
    'Control selection — which controls apply to the scope',
    'Evidence collection — gather policies, configs, logs, screenshots',
    'Testing — validate controls are operating effectively',
    'Remediation — fix gaps found during assessment',
    'Re-testing — verify remediation closed the gaps',
    'Certification/report — final audit opinion or certificate',
]
```

## Verification Checklist

- [ ] Audit framework selected (SOC2, ISO27001, PCI DSS, HIPAA)
- [ ] Scope clearly defined (systems, locations, processes)
- [ ] Control matrix with evidence mapped per control
- [ ] Penetration test conducted by qualified third party
- [ ] Vulnerability scan results reviewed and remediated
- [ ] Policy documentation current and approved
- [ ] Evidence organized in audit-ready format
- [ ] Remediation plan with owners and timelines
