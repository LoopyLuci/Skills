---
name: hr-recruiting-onboarding
description: "Use when managing HR recruiting and employee onboarding."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [HR, recruiting, hiring, onboarding, talent-acquisition, interviews]
    related_skills: [remote-team-management, performance-review-systems, sales-compensation-planning, legal-compliance-business]
---

# HR Recruiting and Onboarding

Managing HR recruiting and employee onboarding — from job descriptions and sourcing through interviews, offer negotiation, and structured onboarding programs.

## When to Use

- Hiring for open positions
- Building a structured interview process
- Designing onboarding programs for new hires
- Creating offer packages and negotiating
- Building employer brand and candidate experience

## Hiring Process

```python
HIRING_PHASES = {
    'sourcing': 'Job boards, LinkedIn, referrals, recruiters, events',
    'screening': 'Resume review, phone screen, portfolio review',
    'interviews': 'Technical, behavioral, take-home, panel',
    'decision': 'Debrief with interview panel, references check',
    'offer': 'Verbal offer, written offer, negotiation, acceptance',
    'onboarding': 'Day 1 setup, orientation, training, ramp plan',
}

class HiringPipeline:
    """Manage candidates through hiring pipeline."""
    def __init__(self, role: str):
        self.role = role
        self.candidates = {}
        self.stages = ['applied', 'screened', 'interviewed', 'offered', 'hired', 'rejected']
    
    def add_candidate(self, name: str, source: str) -> str:
        import uuid
        cid = str(uuid.uuid4())[:8]
        self.candidates[cid] = {
            'id': cid, 'name': name, 'source': source,
            'stage': 'applied', 'days_in_stage': 0,
        }
        return cid
    
    def advance(self, cid: str, stage: str):
        if cid in self.candidates and stage in self.stages:
            self.candidates[cid]['stage'] = stage
    
    def pipeline_summary(self) -> Dict:
        summary = {}
        for stage in self.stages:
            summary[stage] = len([c for c in self.candidates.values() if c['stage'] == stage])
        return summary
```

## Common Pitfalls

1. **Unstructured interviews** — different questions for each candidate makes comparison impossible
2. **Hiring too fast** — skipping reference checks or background verification leads to bad hires
3. **Slow process** — best candidates get other offers; move fast (under 2 weeks)
4. **No onboarding plan** — new hire starts without clear first week/month plan
5. **Bias in hiring** — unconscious bias affects decisions; use structured rubrics and diverse panels

## Verification Checklist

- [ ] Job description with clear requirements and responsibilities
- [ ] Structured interview rubric (questions + scoring criteria)
- [ ] Diverse interview panel
- [ ] Reference check questions defined
- [ ] Offer approval process (compensation band, equity guidelines)
- [ ] Onboarding plan for first 30/60/90 days
- [ ] Background check process (if applicable)
- [ ] Equal opportunity and diversity hiring practices
- [ ] New hire feedback collected at 30/60/90 days
