---
name: skill-review-feedback-loops
description: "Use when implementing skill review and feedback processes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-review, feedback, quality-assurance, iteration, improvement]
    related_skills: [skill-quality-standards, skill-testing-framework, skill-maintenance-lifecycle, code-review-checklist]
---

# Skill Review and Feedback Loops

Implementing review and feedback processes for skills — from peer review workflows through user feedback collection, iteration cycles, and continuous improvement.

## When to Use

- Reviewing skills for quality before publishing
- Collecting user feedback on skill usefulness
- Iteratively improving existing skills
- Building a skill improvement cycle

## Review Framework

```python
class SkillReview:
    """Review skills for quality and completeness."""
    
    REVIEW_CRITERIA = {
        'accuracy': 'Technical content is correct and up-to-date',
        'clarity': 'Content is understandable for the target audience',
        'completeness': 'All required sections are present and substantial',
        'practicality': 'Examples are realistic and applicable',
        'usefulness': 'Skill addresses a real user need',
    }
    
    def __init__(self):
        self.reviews = []
    
    def conduct_review(self, skill_md: str, reviewer: str) -> Dict:
        """Conduct a review of skill content."""
        issues = []
        
        if not skill_md or len(skill_md) < 200:
            issues.append('Skill content too short (< 200 chars)')
        if '## Common Pitfalls' not in skill_md:
            issues.append('Missing Common Pitfalls section')
        if '## Verification Checklist' not in skill_md:
            issues.append('Missing Verification Checklist')
        if '```' not in skill_md:
            issues.append('No code examples')
        
        return {
            'reviewer': reviewer,
            'issues': issues,
            'pass': len(issues) <= 2,
            'score': max(0, 10 - len(issues) * 2),
        }
```

## Feedback Loop

```python
FEEDBACK_LOOP = """
Collect → Analyze → Prioritize → Improve → Verify → Measure

Collect: Inline feedback, surveys, usage analytics
Analyze: Tag and categorize feedback (accuracy, depth, missing topics)
Prioritize: By frequency + impact (how many users affected? how bad?)
Improve: Update skill content, add examples, fix inaccuracies
Verify: Re-review updated skill against quality standards
Measure: Track improvement in user satisfaction scores
"""
```

## Common Pitfalls

1. **Review bottlenecks** — single reviewer blocks publishing; use rotating reviewers
2. **Vague feedback** — "This could be better" without specifics; require actionable comments
3. **No iteration limit** — skills that keep getting revised without publishing
4. **Ignoring negative feedback** — critical feedback is the most valuable for improvement
5. **No feedback channel** — users can't report issues; add an inline feedback mechanism

## Verification Checklist

- [ ] Peer review completed before publishing significant skills
- [ ] Review criteria defined (accuracy, clarity, completeness, practicality)
- [ ] User feedback channel exists (inline rating, issues link)
- [ ] Feedback analyzed and prioritized regularly
- [ ] Improvement cycle: feedback → prioritize → update → verify
- [ ] Skill satisfaction score tracked over time
- [ ] Review turnaround time < 48 hours
