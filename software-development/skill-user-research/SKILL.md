---
name: skill-user-research
description: "Use when researching user needs for skill creation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-research, user-needs, discovery, validation, interviews]
    related_skills: [skill-discovery-techniques, skill-gap-analysis, skill-content-optimization, customer-interview-techniques]
---

# Skill User Research

Researching user needs to guide skill creation — from understanding user personas and pain points through validating skill ideas and measuring skill impact.

## When to Use

- Validating that a skill idea addresses real user needs
- Understanding skill quality from user perspective
- Identifying skill gaps through user feedback
- Measuring skill effectiveness and satisfaction

## Research Methods

```python
class SkillResearch:
    """Research skill needs and validate skill ideas."""
    
    def validate_skill_idea(self, topic: str, users: List[Dict]) -> float:
        """Validate a skill idea against user needs."""
        score = 0
        for user in users:
            if topic in user.get('pain_points', []): score += 3
            if topic in user.get('current_stack', []): score += 2
            if topic in user.get('planned_stack', []): score += 1
        return score / max(len(users), 1)
    
    def analyze_search_queries(self, queries: List[str], 
                                 existing: set) -> List[Dict]:
        """Find skill opportunities from search queries."""
        opportunities = []
        for query in queries:
            words = set(query.lower().split())
            for word in words:
                skill_name = f"{word}-practices"
                if skill_name not in existing:
                    opportunities.append({
                        'query': query,
                        'suggested_skill': skill_name,
                        'frequency': 1,
                    })
        return opportunities
```

## Verification Checklist

- [ ] User persona defined for the skill's target audience
- [ ] Pain points identified through feedback or search data
- [ ] Skill idea validated with at least 3 potential users
- [ ] Existing skills reviewed to avoid duplication
- [ ] Skill value proposition clear
- [ ] Success metrics defined for measuring skill impact
