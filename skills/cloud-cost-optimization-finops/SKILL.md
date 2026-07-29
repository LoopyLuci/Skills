---
name: cloud-cost-optimization-finops
description: "Use when implementing FinOps and cloud cost optimization."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [FinOps, cloud-cost, AWS, Azure, GCP, optimization, reserved-instances, spot]
    related_skills: [infrastructure-policy-as-code, gitops-argocd-flux, cloud-operations, financial-modeling-budgeting]
---

# FinOps and Cloud Cost Optimization

Implementing FinOps practices — from cost allocation and tagging through resource optimization, reserved/compute savings, spot instances, and organizational accountability.

## When to Use

- Reducing cloud infrastructure costs
- Implementing cost allocation by team/project
- Optimizing compute, storage, and networking spend
- Building FinOps culture (engineering + finance + ops)

## FinOps Framework

```python
FINOPS_PHASES = {
    'inform': 'Tagging strategy, cost allocation, dashboards, budget alerts',
    'optimize': 'Right-sizing, reserved instances, spot, auto-scaling, storage tiering',
    'operate': 'Continuous monitoring, governance policies, engineering accountability',
}

class CostOptimizer:
    """Identify cloud cost optimization opportunities."""
    
    RECOMMENDATIONS = {
        'right_size': 'Identify over-provisioned instances (CPU < 20%, memory < 30%)',
        'reserved': 'Steady-state workloads → 1yr/3yr RI/Savings Plans (30-60% savings)',
        'spot': 'Fault-tolerant, stateless workloads → spot instances (60-90% savings)',
        'storage': 'Old data → colder tiers (S3 IA → Glacier → Deep Archive)',
        'cleanup': 'Orphaned resources (EBS, EIP, load balancers, snapshots)',
    }
    
    def estimate_savings(self, current: Dict) -> Dict:
        estimated = {}
        if current.get('on_demand_compute', 0) > 0:
            estimated['reserved'] = round(current['on_demand_compute'] * 0.4, 2)
        if current.get('storage_standard', 0) > 0:
            estimated['storage_tiering'] = round(min(current['storage_standard'], 5000) * 0.5, 2)
        return estimated
```

## Verification Checklist

- [ ] Resource tagging strategy implemented and enforced
- [ ] Cost allocation by team/project/environment
- [ ] Budgets and alerts configured (50%, 80%, 100%)
- [ ] Reserved instances/savings plans purchased for steady-state
- [ ] Spot instances used for fault-tolerant workloads
- [ ] Right-sizing analysis completed (over-provisioned resources)
- [ ] Storage lifecycle policies configured
- [ ] Orphaned resources cleaned up regularly
- [ ] FinOps dashboard with unit economics (cost per customer, per transaction)
