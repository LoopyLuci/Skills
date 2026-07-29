---
name: skill-maintenance-lifecycle
description: "Use when maintaining and updating existing skills."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-maintenance, lifecycle, updates, versioning, deprecation]
    related_skills: [skill-quality-standards, skill-inventory-management, skill-testing-automation, skill-content-optimization]
---

# Skill Maintenance Lifecycle

Managing the lifecycle of skills — from creation through updates, version tracking, deprecation, and retirement.

## When to Use

- Maintaining a growing skill inventory
- Updating skills for new technology versions
- Deprecating outdated skills
- Tracking skill freshness and relevance
- Scheduling regular skill reviews

## Lifecycle Model

```python
from datetime import datetime, timedelta

SKILL_LIFECYCLE = {
    'active': 'Current and maintained — latest practices',
    'needs_review': 'May be outdated — needs assessment within 30 days',
    'deprecated': 'Superseded — points to replacement skill',
    'archived': 'No longer relevant — preserved for historical reference',
}

class SkillMaintenance:
    """Track and manage skill lifecycle."""
    
    REVIEW_INTERVALS = {
        'programming': timedelta(days=90),    # Languages evolve slower
        'framework': timedelta(days=60),       # Frameworks change faster
        'cloud_service': timedelta(days=45),   # Cloud APIs change rapidly
        'security': timedelta(days=30),        # Security landscape shifts fast
        'business': timedelta(days=180),       # Business patterns are stable
    }
    
    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir
    
    def check_freshness(self, skill_path: str) -> Dict:
        """Check if a skill needs review based on its domain."""
        import os, re
        
        with open(os.path.join(skill_path, 'SKILL.md')) as f:
            content = f.read()
        
        # Estimate domain from tags or content
        domain = self._detect_domain(content)
        interval = self.REVIEW_INTERVALS.get(domain, timedelta(days=90))
        
        created = datetime.fromtimestamp(os.path.getctime(skill_path))
        modified = datetime.fromtimestamp(os.path.getmtime(skill_path))
        last_review = max(created, modified)
        
        return {
            'skill': os.path.basename(skill_path),
            'domain': domain,
            'last_review': last_review.isoformat(),
            'review_due': (last_review + interval).isoformat(),
            'needs_review': (datetime.now() - last_review) > interval,
            'days_overdue': (datetime.now() - last_review - interval).days,
        }
```

## Maintenance Schedule

```python
MAINTENANCE_SCHEDULE = """
Monthly:
- Check for technology version updates in top 50 most-used skills
- Review security skills for new vulnerabilities and mitigations

Quarterly:
- Full review of all skills in fast-moving domains (cloud, frameworks)
- Update code examples to latest syntax and APIs
- Review and update related_skills cross-references

Yearly:
- Full inventory audit — all skills reviewed
- Deprecate skills for technologies that are EOL
- Archive skills for obsolete technologies
- Publish skill inventory health report
"""
```

## Common Pitfalls

1. **Set and forget** — skills become outdated quickly; schedule regular reviews
2. **No depreciation process** — old skills confuse users; clearly mark superseded skills
3. **Missing version tracking** — no way to know what changed between updates
4. **Breaking changes without notice** — updating examples without marking the change
5. **No health metric** — can't tell which skills are becoming stale

## Verification Checklist

- [ ] Review intervals set per domain velocity
- [ ] Last review date tracked per skill
- [ ] Deprecated skills point to replacement skill
- [ ] Skill CHANGELOG maintained for significant updates
- [ ] Yearly full inventory audit scheduled
- [ ] Technology EOL dates monitored for affected skills
- [ ] User feedback collected on skill freshness
