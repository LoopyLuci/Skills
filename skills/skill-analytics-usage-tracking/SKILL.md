---
name: skill-analytics-usage-tracking
description: "Use when tracking skill usage and performance analytics."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-analytics, usage-tracking, performance, metrics, dashboards]
    related_skills: [skill-inventory-management, skill-maintenance-lifecycle, skill-review-feedback-loops, business-metrics-kpis]
---

# Skill Analytics and Usage Tracking

Tracking skill usage and performance — from load frequency and user engagement through quality scores, trend analysis, and data-driven improvement decisions.

## When to Use

- Understanding which skills are most valuable
- Identifying underperforming skills that need improvement
- Tracking skill usage trends over time
- Making data-driven decisions about skill investment

## Analytics Framework

```python
class SkillAnalytics:
    """Track and analyze skill performance metrics."""
    
    METRICS = {
        'load_count': 'How often the skill is loaded/referenced',
        'completion_rate': '% of users who reach the checklist',
        'user_rating': 'Average user rating (1-5)',
        'error_report_count': 'Number of reported issues',
        'age_days': 'Days since last update',
        'related_refs': 'Number of other skills referencing this one',
    }
    
    def __init__(self):
        self.events = []
    
    def track_load(self, skill_name: str, user_id: str = None):
        self.events.append({
            'skill': skill_name, 'event': 'load',
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'user': user_id,
        })
    
    def skill_health_score(self, skill_name: str) -> Dict:
        """Calculate composite health score for a skill."""
        loads = sum(1 for e in self.events if e['skill'] == skill_name)
        return {
            'skill': skill_name,
            'total_loads': loads,
            'popularity': 'high' if loads > 100 else 'medium' if loads > 20 else 'low',
            'status': 'healthy',  # Placeholder for real logic
        }
    
    def top_skills(self, limit: int = 10) -> List[str]:
        """Get most frequently loaded skills."""
        from collections import Counter
        skill_counts = Counter(e['skill'] for e in self.events if e['event'] == 'load')
        return [skill for skill, _ in skill_counts.most_common(limit)]
```

## Metrics Dashboard

```python
DASHBOARD_METRICS = [
    'Total skills available vs created per month',
    'Top 10 most-loaded skills (trending)',
    'Bottom 10 least-loaded skills (needs review)',
    'Skill health scores (traffic light: green/yellow/red)',
    'User ratings distribution (1-5 stars)',
    'Error report rate per skill',
    'Category coverage (% of categories with active skills)',
    'Skill freshness (days since last update per skill)',
]
```

## Common Pitfalls

1. **Vanity metrics** — total skills count without quality measure
2. **No user distinction** — all loads counted equally whether useful or not
3. **Ignoring recency** — old skills may have high historical counts but be outdated
4. **No trend detection** — can't see which skills are gaining or losing relevance
5. **No quality signal** — usage ≠ quality; add rating or feedback metrics

## Verification Checklist

- [ ] Skill load events tracked with timestamps
- [ ] User ratings collected (thumbs up/down or 1-5)
- [ ] Error/issue reports tracked per skill
- [ ] Dashboard with key metrics available
- [ ] Monthly skill health report generated
- [ ] Trend detection (which skills are gaining/losing popularity)
- [ ] Low-performing skills flagged for review
- [ ] Data drives skill creation roadmap
