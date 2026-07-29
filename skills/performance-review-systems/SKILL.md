---
name: performance-review-systems
description: "Use when designing performance review and feedback systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [performance-review, feedback, 360-review, OKRs, evaluation, growth]
    related_skills: [remote-team-management, hr-recruiting-onboarding, business-metrics-kpis, okr-goal-setting-advanced]
---

# Performance Review Systems

Designing performance review and feedback systems — from 360 reviews and OKR alignment through continuous feedback, calibration, and growth-based evaluation.

## When to Use

- Building or improving performance review processes
- Moving from annual reviews to continuous feedback
- Aligning reviews with OKRs and company goals
- Training managers on effective performance conversations
- Implementing peer feedback and 360 reviews

## Review Models

```python
REVIEW_MODELS = {
    'annual': 'Yearly comprehensive review (traditional, often disliked)',
    'quarterly': 'Quarterly check-in on goals and development (responsive)',
    'continuous': 'Ongoing feedback via lightweight tools (modern approach)',
    '360': 'Feedback from manager, peers, direct reports, cross-functional',
    'self_assessment': 'Employee evaluates their own performance first',
    'peer_review': 'Feedback from team members and collaborators',
}

class PerformanceReview:
    """Structure a performance review cycle."""
    def __init__(self, employee: str, reviewer: str, period: str):
        self.employee = employee
        self.reviewer = reviewer
        self.period = period
        self.scores = {}
        self.comments = {}
    
    def add_category(self, name: str, score: int, 
                     strengths: str = '', growth: str = ''):
        self.scores[name] = score
        self.comments[name] = {'strengths': strengths, 'growth': growth}
    
    def summary(self) -> Dict:
        avg_score = sum(self.scores.values()) / len(self.scores) if self.scores else 0
        return {
            'employee': self.employee,
            'overall_score': round(avg_score, 1),
            'categories': self.scores,
            'top_strength': max(self.comments.items(), key=lambda x: x[1].get('strengths', ''))[0] if self.comments else '',
            'priority_growth': min(self.comments.items(), key=lambda x: x[1].get('growth', ''))[0] if self.comments else '',
        }
```

## Common Pitfalls

1. **Recency bias** — recent events overshadow the full period; document throughout
2. **Surprise feedback** — nothing in review should be a surprise; give real-time feedback
3. **Rating inflation** — everyone gets 4/5; use calibration across teams for fairness
4. **No development focus** — reviews should be about growth, not just rating
5. **Biased evaluations** — gender, racial, and cultural biases affect reviews; train reviewers

## Verification Checklist

- [ ] Review cycle cadence defined (annual, quarterly, or continuous)
- [ ] Evaluation criteria aligned with company values and role expectations
- [ ] Manager training on effective feedback conversations
- [ ] Calibration process to ensure fairness across teams
- [ ] Self-assessment as first step in review
- [ ] Development goals linked to review outcomes
- [ ] Continuous feedback channel (not just formal reviews)
- [ ] Bias training for all reviewers
- [ ] Review data used for promotions and compensation decisions
