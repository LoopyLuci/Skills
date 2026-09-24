---
name: aws-cloudfront-troubleshooting-troubleshooting
description: Use when applying cloudfront troubleshooting troubleshoo.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [cloud, cdn]
---

# Aws Cloudfront Troubleshooting Troubleshooting

"Use when applying cloudfront troubleshooting troubleshoo."

## Trigger

Activate this skill when the user mentions:
- cloud,  cdn workflows or issues
- Building, fixing, or optimizing aws cloudfront troubleshooting troubleshooting
- Questions about cloud best practices

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

`cloud, cdn`

---

*LoopyLuci/Skills - 2026-09-24*
