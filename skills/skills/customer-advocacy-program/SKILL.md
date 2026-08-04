---
name: customer-advocacy-program
description: "Use when building customer advocacy and referral programs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [customer-advocacy, referrals, testimonials, case-studies, community, champions]
    related_skills: [customer-success-retention, loyalty-programs-crm, influencer-affiliate-programs, community-management-engagement]
---

# Customer Advocacy Programs

Building customer advocacy programs — from identifying advocates and collecting testimonials through case studies, referral programs, and customer advisory boards.

## When to Use

- Leveraging happy customers for acquisition and retention
- Building a customer reference program for sales
- Collecting and promoting customer testimonials and case studies
- Creating a customer advisory board
- Implementing customer referral programs

## Advocacy Program Types

```python
ADVOCACY_TYPES = {
    'referral': 'Customers refer others in exchange for rewards',
    'testimonial': 'Collect and promote customer quotes and reviews',
    'case_study': 'In-depth customer success story with metrics',
    'reference_call': 'Customer speaks to prospects about their experience',
    'advisory_board': 'Key customers provide strategic product feedback',
    'community_champion': 'Active community members who help other customers',
    'review_generation': 'Encourage reviews on G2, Capterra, Trustpilot',
}

class AdvocacyProgram:
    """Manage customer advocacy activities."""
    def __init__(self):
        self.advocates = {}
        self.activities = []
    
    def enroll_advocate(self, customer: str, company: str, 
                        engagement: str = 'reference'):
        """Add customer to advocacy program."""
        import uuid
        aid = str(uuid.uuid4())[:8]
        self.advocates[aid] = {
            'id': aid, 'customer': customer, 'company': company,
            'engagement': engagement, 'activities': 0, 'status': 'active',
        }
        return aid
    
    def record_activity(self, advocate_id: str, activity_type: str):
        if advocate_id in self.advocates:
            self.advocates[advocate_id]['activities'] += 1
            self.activities.append({
                'advocate': advocate_id, 'type': activity_type,
                'date': datetime.now().isoformat(),
            })
```

## Common Pitfalls

1. **Only asking, never giving** — advocacy is reciprocal; provide early access, exclusive content, recognition
2. **Not amplifying** — collecting testimonials without promoting them; feature advocates prominently
3. **No program structure** — asking ad-hoc without a system; advocates feel undervalued
4. **Not tracking ROI** — referalls from advocacy are less expensive than paid acquisition; measure it
5. **Ignoring detractors** — unhappy customers are also vocal; address their concerns first

## Verification Checklist

- [ ] Advocate identification criteria defined
- [ ] Advocate program tiers with benefits
- [ ] Testimonial collection process (text, video)
- [ ] Case study template with ROI format
- [ ] Referral program with rewards structure
- [ ] Review generation campaign (G2, Capterra, Google)
- [ ] Advocate recognition program (badges, events, swag)
- [ ] Advocacy ROI tracked (referral revenue vs program cost)
- [ ] Customer advisory board (quarterly meetings)
