---
name: export-control-compliance
description: "Use when ensuring export control compliance."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [legal, export-control, itar, EAR]
    related_skills: [general]
---

# Export Control Compliance

"Use when ensuring export control compliance."

## Trigger

Activate this skill when the user mentions:
- legal,  export-control,  itar,  EAR workflows or issues
- Building, fixing, or optimizing export control compliance
- Questions about legal best practices

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

`legal, export-control, itar, EAR`

---

*LoopyLuci/Skills - 2026-09-24*
