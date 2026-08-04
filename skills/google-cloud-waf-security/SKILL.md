---
name: google-cloud-waf-security
description: Use when evaluating security posture of Google Cloud workloads following Well-Architected Framework.
tags: [google-cloud, waf, security, iam, network-security, compliance]
related_skills: [google-cloud-waf-cost-optimization, google-cloud-recipe-auth, gke-productionize]
---

# Google Cloud Well-Architected Framework — Security

Design principles and best practices for building a robust security posture on Google Cloud, covering IAM, network security, data protection, and operational security.

## Core Principles

1. **Implement security by design**
2. **Implement zero trust** — Never trust, always verify
3. **Implement shift-left security** — Early in development lifecycle
4. **Implement preemptive cyber defense**
5. **Use AI securely and responsibly**
6. **Use AI for security**
7. **Meet regulatory, compliance, and privacy needs**

## Security Products

| Category | Products |
|----------|----------|
| Identity & Access | IAM, IAP, Chrome Enterprise Premium |
| Network Security | Cloud Armor, VPC Service Controls, Cloud NGFW |
| Data Security | Cloud KMS, Sensitive Data Protection, Confidential Computing |
| SecOps | Google SecOps, Security Command Center, Cloud Logging |
| Supply Chain | Cloud Build, Artifact Analysis, Binary Authorization |

## Code Example: VPC Service Controls

```bash
# Create a service perimeter
gcloud access-context-manager perimeters create my-perimeter \
  --title="Data Perimeter" \
  --resources="projects/123456789" \
  --restricted-services="storage.googleapis.com" \
  --policy=POLICY_ID
```

## Common Pitfalls

- **Default networks enabled**: Disable default networks in all projects
- **Missing IAM least privilege**: Grant minimal roles, review regularly
- **No encryption at rest**: Enable CMEK for sensitive data
- **Public buckets**: Cloud Storage buckets should not be publicly accessible
- **No incident response plan**: Have a tested response plan before going live

## Verification Checklist

- [ ] IAM least privilege applied (no broad roles)
- [ ] Default networks disabled
- [ ] VPC Service Controls perimeters established
- [ ] Cloud Armor configured for public endpoints
- [ ] Security Command Center enabled
- [ ] CI/CD pipeline includes security scanning
- [ ] Binary Authorization enforced
- [ ] Incident response plan documented
