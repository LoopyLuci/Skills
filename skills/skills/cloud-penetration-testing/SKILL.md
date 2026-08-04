---
name: cloud-penetration-testing
description: "Use when testing cloud infrastructure security."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cloud-pentest, AWS, Azure, GCP, IAM, S3, metadata, privilege-escalation]
    related_skills: [cloud-cost-optimization-finops, identity-access-management, container-security-testing, webapp-penetration-testing]
---

# Cloud Penetration Testing

Testing cloud infrastructure security — from AWS/Azure/GCP IAM enumeration through S3 bucket to privilege escalation, metadata service, and container escape.

## When to Use

- Assessing cloud infrastructure security posture
- Testing cloud IAM policies for privilege escalation
- Auditing cloud storage (S3, Blob, GCS) configuration
- Cloud metadata service exploitation
- Container escape within cloud environments

## Cloud Attack Techniques

```python
CLOUD_ATTACKS = {
    'iam_enumeration': 'Enumerate IAM permissions, users, roles, policies via CLI or API',
    's3_bucket': 'List bucket contents, upload/download, ACL misconfiguration, public access',
    'metadata_service': 'Query http://169.254.169.254/latest/meta-data/ for instance creds',
    'lambda_injection': 'Exploit event injection into Lambda functions for privilege escalation',
    'cloudtrail_logs': 'Disable or modify logging to cover tracks (cloudtrail:StopLogging)',
    'kms_key_abuse': 'Decrypt data using misconfigured KMS key policies',
    'privilege_escalation': 'iam:PassRole, iam:CreatePolicyVersion, ec2:RunInstances with admin role',
}

# AWS metadata service attacks
AWS_METADATA_QUERY = [
    "curl http://169.254.169.254/latest/meta-data/iam/security-credentials/",
    "curl http://169.254.169.254/latest/user-data/",
    "curl http://169.254.169.254/latest/meta-data/iam/security-credentials/[ROLE]/",
]

# GCP metadata
GCP_METADATA = "curl -H 'Metadata-Flavor: Google' http://169.254.169.254/computeMetadata/v1/"

# Azure IMDS
AZURE_IMDS = "curl -H 'Metadata: true' http://169.254.169.254/metadata/instance?api-version=2021-02-01"
```

## Verification Checklist

- [ ] IAM policy enumeration (users, roles, policies, trust relationships)
- [ ] Privilege escalation paths identified (iam:PassRole, etc.)
- [ ] Storage services audited (S3, Blob, GCS — ACLs, public access)
- [ ] Metadata service accessible (if running in cloud)
- [ ] CloudTrail/CloudWatch logs checked for sensitive data
- [ ] Lambda/Cloud Functions checked for secrets in env vars
- [ ] KMS keys checked for overly permissive policies
- [ ] VPC security groups reviewed for overly broad rules
- [ ] Container images scanned for vulnerabilities
