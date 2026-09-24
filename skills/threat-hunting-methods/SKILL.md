---
name: threat-hunting-methods
description: Use when implementing threat hunting and proactive security.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [threat-hunting, security, proactive, iocs, ttps, hypothesis, siem]
---

# Threat Hunting Methods

"Use when implementing threat hunting and proactive security."

## Trigger

Activate this skill when the user mentions:
- threat-hunting,  security,  proactive,  IoCs,  TTPs,  hypothesis,  SIEM workflows or issues
- Building, fixing, or optimizing threat hunting methods
- Questions about threat-hunting best practices

## Core Concepts

- Threat modeling and risk assessment
- Attack surface analysis
- Defense in depth
- Zero-trust architecture
- Compliance and audit requirements

## Step-by-Step Workflow

1. **Scope** — Define assets, threats, attack surface
   - Expected: Documented scope with trust boundaries
2. **Assess** — Identify vulnerabilities, evaluate risk
   - Expected: Prioritized findings with CVSS scores
3. **Remediate** — Apply secure-by-design fixes
   - Expected: Vulnerabilities closed
4. **Verify** — Re-test and validate remediation
   - Expected: Independent verification complete
5. **Document** — Record findings and lessons learned
   - Expected: Audit-ready report

## Tools & Technologies

- Vulnerability scanners
- SAST/DAST tools
- SIEM platforms
- Pen-testing frameworks

## Best Practices

- Document decisions and rationale (ADRs, design docs, runbooks)
- Version everything - code, configs, data, and documentation
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethical standards
- Measure outcomes with meaningful metrics

## Common Pitfalls

- **Scope creep** → Unclear boundaries → Define scope explicitly
- **Tool reliance without analysis** → False positives → Manual validation required

## Tags

`threat-hunting, security, proactive, IoCs, TTPs, hypothesis, SIEM`

---

*LoopyLuci/Skills - 2026-09-24*
