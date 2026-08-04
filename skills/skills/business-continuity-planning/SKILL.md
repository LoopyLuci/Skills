---
name: business-continuity-planning
description: "Use when designing business continuity and disaster plans."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [business-continuity, disaster-recovery, BCP, DRP, RTO, RPO, failover]
    related_skills: [security-incident-response, certificate-management-pki, remote-team-management, data-pipeline-streaming]
---

# Business Continuity and Disaster Recovery

Designing business continuity plans and disaster recovery procedures.

## When to Use

- Ensuring business operations continue during disruptions
- Defining RTO (Recovery Time Objective) and RPO (Recovery Point Objective)
- Building DR plans for IT systems
- Complying with regulations requiring business continuity

## BCP Framework

```python
BCP_PHASES = {
    'analysis': 'Business Impact Analysis (BIA) — identify critical functions',
    'strategy': 'Define recovery strategies (active-passive, active-active, hot/warm/cold)',
    'planning': 'Document recovery procedures, roles, communication',
    'testing': 'Regular DR tests (tabletop, walkthrough, full failover)',
}

def business_impact_analysis(processes: List[Dict]) -> List[Dict]:
    for p in processes:
        if p.get('max_downtime_hours', 72) <= 4: p['priority'] = 'critical'
        elif p.get('max_downtime_hours', 72) <= 24: p['priority'] = 'high'
        else: p['priority'] = 'normal'
    return sorted(processes, key=lambda p: p.get('max_downtime_hours', 72))
```

## Common Pitfalls

1. **No testing** — untested DR plans fail when needed
2. **Unrealistic RTO** — claiming 1-hour RTO for 4-hour restores
3. **Only IT focus** — BCP includes people, facilities, suppliers too
4. **Single region failure** — backup site in same disaster zone as primary

## Verification Checklist

- [ ] BIA completed for critical processes
- [ ] RTO and RPO defined per system
- [ ] DR plan documented and versioned
- [ ] Crisis communication plan with contact lists
- [ ] DR test schedule (tabletop quarterly, full failover annually)
- [ ] Backup restoration tested regularly
- [ ] Off-site or cloud-based backups
