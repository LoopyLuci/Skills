---
name: product-management-roadmap
description: "Use when managing products and building roadmaps."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [product-management, roadmap, backlog, prioritization, RICE, user-stories, sprints]
    related_skills: [saas-metrics-reporting, project-management-workflows, customer-feedback-surveys, competitive-intelligence-analysis]
---

# Product Management and Roadmapping

Managing products end-to-end — from strategy and roadmapping through backlog prioritization, user stories, releases, and stakeholder communication.

## When to Use

- Building and maintaining a product roadmap
- Prioritizing features and managing backlog
- Writing user stories and acceptance criteria
- Running product discovery and validation
- Communicating product plans to stakeholders

## Roadmap Framework

```
Now (0-3 months) — Committed, concrete, in progress
Next (3-6 months) — Likely but not committed, being validated
Later (6-12 months) — Exploration, not yet scoped
```

## Prioritization Frameworks

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import math

class Prioritization:
    """Score and prioritize features using multiple frameworks."""
    
    @staticmethod
    def rice(features: List[Dict]) -> List[Dict]:
        """Score features using RICE: Reach, Impact, Confidence, Effort."""
        scored = []
        for f in features:
            reach = f.get('reach', 0)        # How many users per quarter
            impact = f.get('impact', 2)      # 1-massive, 2-high, 3-medium, 4-low
            confidence = f.get('confidence', 2)  # 1-high, 2-medium, 3-low
            effort = f.get('effort', 10)     # Person-weeks
            
            # Invert impact and confidence (lower = better)
            impact_score = 4 - impact
            confidence_score = 4 - confidence
            
            rice_score = (reach * impact_score * confidence_score) / max(effort, 1)
            
            scored.append({
                'feature': f.get('name', ''),
                'reach': reach,
                'impact': impact,
                'confidence': confidence,
                'effort': effort,
                'rice_score': round(rice_score, 1),
            })
        
        return sorted(scored, key=lambda x: x['rice_score'], reverse=True)
    
    @staticmethod
    def value_vs_effort(features: List[Dict]) -> Dict:
        """Plot features on a value vs effort matrix."""
        matrix = {'quick_wins': [], 'big_bets': [], 'fill_ins': [], 'time_wasters': []}
        
        for f in features:
            value = f.get('value', 5)     # 1-10
            effort = f.get('effort', 5)   # 1-10 (higher = more effort)
            
            if value >= 6 and effort <= 4:
                matrix['quick_wins'].append(f['name'])
            elif value >= 6 and effort > 4:
                matrix['big_bets'].append(f['name'])
            elif value < 6 and effort <= 4:
                matrix['fill_ins'].append(f['name'])
            else:
                matrix['time_wasters'].append(f['name'])
        
        return matrix
    
    @staticmethod
    def now_next_later(prioritized: List[Dict], 
                       quarterly_capacity: int = 50) -> Dict:
        """Distribute features into Now/Next/Later buckets."""
        buckets = {'now': [], 'next': [], 'later': []}
        effort_used = 0
        
        for item in prioritized:
            effort = item.get('effort', 5)
            if effort_used + effort <= quarterly_capacity * 0.6:
                buckets['now'].append(item)
                effort_used += effort
            elif effort_used + effort <= quarterly_capacity * 0.9:
                buckets['next'].append(item)
                effort_used += effort
            else:
                buckets['later'].append(item)
        
        return buckets
```

## User Story Builder

```python
class UserStory:
    """Write and manage user stories with acceptance criteria."""
    
    @staticmethod
    def create(role: str, goal: str, benefit: str) -> str:
        """As a [user], I want [goal], so that [benefit]."""
        return f"As a **{role}**, I want **{goal}**, so that **{benefit}**."
    
    @staticmethod
    def add_acceptance_criteria(user_story: str, criteria: List[str]) -> str:
        """Append Gherkin-style acceptance criteria."""
        result = user_story + "\n\n**Acceptance Criteria:**\n"
        for c in criteria:
            result += f"\n- [ ] {c}"
        return result
    
    @staticmethod
    def add_gherkin_scenarios(user_story: str, 
                              scenarios: List[Dict]) -> str:
        """Add Given/When/Then scenarios."""
        result = user_story + "\n\n**Scenarios:**\n"
        for s in scenarios:
            result += f"\n**Scenario:** {s.get('name', '')}"
            result += f"\n  Given {s.get('given', '')}"
            result += f"\n  When {s.get('when', '')}"
            result += f"\n  Then {s.get('then', '')}\n"
        return result
```

## Release Planning

```python
class ReleasePlanner:
    """Plan and communicate product releases."""
    
    def __init__(self, version: str, release_date: str):
        self.version = version
        self.release_date = release_date
        self.features = []
        self.bugs = []
        self.risks = []
    
    def add_feature(self, feature: str, impact: str = 'medium', 
                    effort: str = 'medium') -> 'ReleasePlanner':
        self.features.append({'feature': feature, 'impact': impact, 'effort': effort})
        return self
    
    def add_bug_fix(self, bug: str, severity: str):
        self.bugs.append({'bug': bug, 'severity': severity})
        return self
    
    def generate_release_notes(self) -> str:
        notes = f"🚀 Release v{self.version} — {self.release_date}\n"
        notes += "=" * 50 + "\n"
        
        notes += f"\n**New Features:**\n"
        for f in self.features:
            notes += f"  ✨ {f['feature']}\n"
        
        notes += f"\n**Bug Fixes:**\n"
        if self.bugs:
            for b in self.bugs:
                notes += f"  🐛 Fixed: {b['bug']}\n"
        else:
            notes += "  None\n"
        
        return notes
```

## Common Pitfalls

1. **Roadmap as a commitment** — roadmap is a plan, not a promise; communicate uncertainty
2. **No discovery before building** — building features nobody wants wastes time; validate first
3. **Everything is P1** — if everything is priority 1, nothing is; force hard trade-offs
4. **Stakeholder-driven roadmap** — every request goes to the top without prioritization
5. **No exit criteria for experiments** — run experiments with clear go/no-go thresholds
6. **Not shipping** — perfect features never ship; focus on 80% solutions that deliver value now

## Verification Checklist

- [ ] Product strategy documented (vision, target users, differentiators)
- [ ] Roadmap with Now/Next/Later buckets
- [ ] Prioritization framework chosen (RICE, value/effort, etc.)
- [ ] User stories follow standard format with acceptance criteria
- [ ] Release plan with date, scope, and risks documented
- [ ] Product discovery process defined (user research, testing)
- [ ] Success metrics defined for each major feature
- [ ] Stakeholder communication cadence established

## See Also

- saas-metrics-reporting — measuring product impact
- project-management-workflows — executing the roadmap
- customer-feedback-surveys — input for product decisions
- competitive-intelligence-analysis — market positioning
