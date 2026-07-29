---
name: customer-journey-mapping
description: "Use when mapping customer journeys and touchpoints."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [customer-journey, experience-map, touchpoints, CX, UX, service-design]
    related_skills: [digital-marketing-strategy, customer-success-retention, product-management-roadmap, marketing-funnel-design]
---

# Customer Journey Mapping

Mapping customer journeys to understand experiences, identify pain points, and optimize touchpoints across the entire customer lifecycle.

## When to Use

- Understanding the end-to-end customer experience
- Identifying friction points in the customer journey
- Designing omnichannel customer experiences
- Aligning teams around customer-centric improvements
- Improving conversion, retention, and satisfaction

## Journey Map Template

```python
from typing import Dict, List
from datetime import timedelta

class JourneyMap:
    """Build and analyze customer journey maps."""
    
    STAGES = ['Awareness', 'Consideration', 'Decision', 'Onboarding', 'Adoption', 'Expansion', 'Advocacy']
    
    def __init__(self, persona: str, scenario: str):
        self.persona = persona
        self.scenario = scenario
        self.stages = []
    
    def add_stage(self, name: str, goals: List[str], touchpoints: List[str],
                  emotions: str, pain_points: List[str], opportunities: List[str]):
        self.stages.append({
            'name': name, 'goals': goals, 'touchpoints': touchpoints,
            'emotions': emotions, 'pain_points': pain_points,
            'opportunities': opportunities,
        })
    
    def generate_report(self) -> str:
        report = f"🗺️ Customer Journey: {self.persona} — {self.scenario}\n" + "=" * 50 + "\n"
        for stage in self.stages:
            report += f"\n## {stage['name']}\n"
            report += f"Goals: {', '.join(stage['goals'][:2])}\n"
            report += f"Emotions: {stage['emotions']}\n"
            report += f"Pain Points: {', '.join(stage['pain_points'][:3])}\n"
            report += f"Opportunities: {', '.join(stage['opportunities'][:2])}\n"
        return report
```

## Common Pitfalls

1. **Internal view, not customer view** — mapping what you THINK customers do, not what they actually do
2. **Too many touchpoints** — focus on moments that matter, not every micro-interaction
3. **No emotional journey** — customer experience is emotional; chart feelings, not just actions
4. **Static one-time map** — customer journeys evolve; update quarterly
5. **No ownership** — journey improvements need owners, or nothing changes

## Verification Checklist

- [ ] Persona-based journey (not generic)
- [ ] Emotional journey charted (highs and lows)
- [ ] Pain points identified per stage
- [ ] Moments of truth identified (make-or-break touchpoints)
- [ ] Opportunities prioritized by impact and effort
- [ ] Journey shared with cross-functional team
- [ ] Ownership assigned for key improvements
