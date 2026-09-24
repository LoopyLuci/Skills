---
name: aws-guard-duty-best-practices
description: Use when applying aws guardduty best practices.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [aws, guardduty, security, threat-detection]
---

# Aws Guard Duty Best Practices

"Use when applying aws guardduty best practices."

## Trigger

Activate this skill when the user mentions:
- aws,  guardduty,  security,  threat-detection workflows or issues
- Building, fixing, or optimizing aws guard duty best practices
- Questions about aws best practices

## Core Concepts

- Infrastructure as Code (IaC)
- Well-Architected Framework
- Identity and access management
- Networking and security groups
- Cost optimization and tagging

## Step-by-Step Workflow

1. **Design** — Architecture review against WAF pillars
   - Expected: Approved architecture diagram
2. **Implement** — IaC templates with least-privilege IAM
   - Expected: Reviewable version-controlled infra
3. **Validate** — Security scan, cost estimate, plan review
   - Expected: Clean plan within budget
4. **Deploy** — Apply with change management
   - Expected: Deployed infrastructure matches plan
5. **Monitor** — Alarms, dashboards, cost alerts
   - Expected: Full observability and cost allocation

## Tools & Technologies

- Terraform/Pulumi
- Cloud-native IaC
- Security scanning
- Cost management

## Best Practices

- Document decisions and rationale (ADRs, design docs, runbooks)
- Version everything - code, configs, data, and documentation
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethical standards
- Measure outcomes with meaningful metrics

## Common Pitfalls

- **Manual console changes** → Configuration drift → All changes through IaC
- **Over-privileged IAM** → Blast radius risk → Least privilege by default

## Tags

`aws, guardduty, security, threat-detection`

---

*LoopyLuci/Skills - 2026-09-24*
