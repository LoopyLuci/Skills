---
name: container-platform-security
description: "Use when securing container platforms."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [devops, container-security, k8s-security]
    related_skills: ['container-security-hardening']
---

## Overview
Secure container platforms including runtime protection and image scanning.

## When to Use
- "Container Platform Security design and implementation"
- "Best practices for Container Platform Security"
- "Container Platform Security deployment and monitoring"
- "Container Platform Security troubleshooting and scaling"

## Key Approaches
1. Define clear requirements and specifications
2. Choose appropriate tools and frameworks
3. Implement with modular, maintainable code
4. Write tests and automate verification
5. Document architecture and decisions
6. Monitor performance and iterate

## Common Pitfalls
1. **Not accounting for constraints** — resource or timeline limitations
2. **Ignoring industry standards** — not following established best practices
3. **Poor stakeholder alignment** — conflicting requirements
4. **Inadequate testing** — no validation of critical functions
5. **Not documenting decisions** — lost knowledge transfer
6. **Skipping security review** — no threat modeling performed
7. **Over-engineering** — complex solutions where simple ones suffice
8. **No rollback plan** — deployment failures cause outages
9. **Insufficient monitoring** — no observability after deployment
10. **Not planning for growth** — scalability issues in production

## Verification Checklist
- [ ] Requirements defined and validated
- [ ] Industry standards and best practices applied
- [ ] Design reviewed with stakeholders
- [ ] Implementation plan with milestones
- [ ] Testing strategy with coverage targets
- [ ] Security review and threat modeling
- [ ] Monitoring and alerting configured
- [ ] Documentation complete and accessible
- [ ] Deployment with rollback plan
- [ ] Post-deployment verification
