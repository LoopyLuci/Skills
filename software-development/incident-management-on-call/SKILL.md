---
name: incident-management-on-call
description: "Use when implementing incident management and on-call."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [incident-management, on-call, pager-duty, escalation, postmortem, alerting]
    related_skills: [error-budgets-slos, site-reliability-engineering, security-incident-response, chaos-engineering]
---

# Incident Management and On-Call

Implementing incident management and on-call practices — from alert routing and escalation through incident response, communication, and blameless postmortems.

## When to Use

- Setting up on-call rotations
- Building incident response processes
- Implementing alert routing and escalation
- Conducting blameless postmortems
- Reducing MTTR (Mean Time to Resolve)

## Incident Management

```python
INCIDENT_SEVERITIES = {
    'SEV1': 'Critical — service down, data loss, security breach — <15min response',
    'SEV2': 'High — degraded service, partial outage — <30min response',
    'SEV3': 'Medium — non-critical issue, single user — <4h response',
    'SEV4': 'Low — cosmetic, non-urgent — next business day',
}

class OnCallSchedule:
    """Manage on-call rotations and escalations."""
    def __init__(self):
        self.team = []  # List of engineer IDs
        self.escalations = []  # Ordered escalation paths
    
    def current_on_call(self) -> str:
        # Determined by schedule (weekly rotation typical)
        import datetime
        week = datetime.date.today().isocalendar()[1]
        return self.team[week % len(self.team)]
    
    def escalate(self, engineer: str, reason: str) -> List[str]:
        """Escalate to next tier if no response within SLA."""
        idx = self.escalations.index(engineer) if engineer in self.escalations else -1
        path = self.escalations[idx + 1:] if idx >= 0 else self.escalations
        return [f"Escalated to {e}: {reason}" for e in path]
```

## Verification Checklist

- [ ] On-call rotation established (weekly shifts)
- [ ] Escalation path defined (primary → secondary → manager)
- [ ] Alert routing by severity and service
- [ ] Incident response runbook for common scenarios
- [ ] Communication templates (status page, internal, stakeholders)
- [ ] Blameless postmortem within 1 week of SEV1/2
- [ ] Action items tracked from postmortems
- [ ] MTTR tracked and trended
- [ ] On-call compensation or recognition program
