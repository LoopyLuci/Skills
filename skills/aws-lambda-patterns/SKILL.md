---
name: aws-lambda-patterns
description: "Use when building AWS Lambda functions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: ["aws", "lambda", "serverless", "event-driven"]
---

# Aws Lambda Patterns

"Use when building AWS Lambda functions."

## Trigger

Activate this skill when the user mentions:
- "aws",  "lambda",  "serverless",  "event-driven" workflows or issues
- Building, fixing, or optimizing aws lambda patterns
- Questions about "aws" best practices

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

`"aws", "lambda", "serverless", "event-driven"`

---

*LoopyLuci/Skills - 2026-09-24*
