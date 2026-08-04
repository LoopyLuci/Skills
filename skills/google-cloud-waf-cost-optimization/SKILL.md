---
name: google-cloud-waf-cost-optimization
description: Use when optimizing Google Cloud workload costs following the Well-Architected Framework.
tags: [google-cloud, waf, cost-optimization, finops, cloud-architecture]
related_skills: [google-cloud-waf-security, gke-productionize, google-cloud-recipe-auth]
---

# Google Cloud Well-Architected Framework — Cost Optimization

Provides a structured approach to optimize cloud costs while maximizing business value, following the FinOps lifecycle: Inform → Optimize → Operate.

## Core Principles

1. **Align cloud spending with business value**
2. **Foster a culture of cost awareness**
3. **Optimize resource usage**
4. **Optimize continuously**

## Cost Optimization Strategies

| Area | Strategy |
|------|----------|
| Compute | Use CUDs for steady workloads, Spot VMs for fault-tolerant tasks |
| Storage | Lifecycle policies (move to Nearline/Coldline/Archive) |
| Networking | Keep traffic regional, use Standard Tier, Cloud CDN |
| Managed Services | Prefer Cloud Run, GKE Autopilot, serverless |
| Visibility | Cloud Billing reports, BigQuery billing export, Looker Studio |

## Code Example: Storage Lifecycle Policy (gcloud)

```bash
# Set lifecycle policy on a bucket
gcloud storage buckets update gs://my-bucket --lifecycle-file=lifecycle.json
```

```json
// lifecycle.json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
        "condition": {"age": 30}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
        "condition": {"age": 90}
      }
    ]
  }
}
```

## Common Pitfalls

- **Retrieval fees**: Nearline/Coldline/Archive have retrieval costs — size data access patterns first
- **Over-provisioning**: Right-size based on Recommender data, not guesses
- **Missing labels**: 100% of resources should be labeled for cost attribution
- **No budgets**: Always configure billing alerts and budgets

## Verification Checklist

- [ ] All resources labeled with key metadata (env, team, app)
- [ ] BigQuery billing export enabled
- [ ] Budgets and alerts configured
- [ ] Rightsizing recommendations reviewed
- [ ] Storage lifecycle policies active
- [ ] CUD coverage optimized monthly
