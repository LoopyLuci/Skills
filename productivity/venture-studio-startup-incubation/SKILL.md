---
name: venture-studio-startup-incubation
description: "Use when building venture studios and startup incubation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [venture-studio, startup-studio, incubation, venture-building, startup-factory]
    related_skills: [fractional-executive-patterns, venture-capital-essentials, product-management-roadmap, go-to-market-strategy]
---

# Venture Studio and Startup Incubation

Building venture studios and startup incubation programs — from idea validation and MVP building through founder matching, studio operations, and portfolio management.

## When to Use

- Starting a venture studio (startup studio model)
- Incubating startups inside an existing company
- Running corporate innovation programs
- Building a startup factory approach

## Venture Studio Models

```python
STUDIO_MODELS = {
    'idea_factory': 'Studio generates ideas, builds MVPs, finds CEO co-founder — 4-6 month cycle',
    'co_founding': 'Studio provides co-founders (tech + design), external CEO brought in',
    'corporate_spinout': 'Spin out internal innovation into separate company with external investment',
    'platform_studio': 'Build multiple startups on shared platform (legal, design, engineering, distribution)',
}

class VentureStudio:
    """Manage venture studio pipeline."""
    def __init__(self, name: str, cycle_months: int = 6):
        self.name = name
        self.projects = []
        self.active_portfolio = []
        self.cycle = cycle_months
    
    def add_project(self, idea: str, stage: str = 'ideation'):
        self.projects.append({
            'idea': idea, 'stage': stage,
            'mvp_months': 3, 'total_investment': 0,
        })
    
    def graduate(self, project_idx: int, company_name: str, 
                 seed_investment: float, equity_pct: float) -> Dict:
        project = self.projects[project_idx]
        self.active_portfolio.append({
            'company': company_name, 'idea': project['idea'],
            'seed': seed_investment, 'studio_equity': equity_pct,
        })
        return self.active_portfolio[-1]
```

## Verification Checklist

- [ ] Studio model selected (idea factory, co-founding, corporate spinout, platform)
- [ ] Idea generation and validation process established
- [ ] MVP development playbook (3-month cycles)
- [ ] Founder matching and equity split framework
- [ ] Shared services playbook (design, engineering, legal, accounting)
- [ ] Portfolio management (dashboards, board reps, follow-on funding)
- [ ] Exit strategy (acquisition targets, IPO readiness)
- [ ] Studio economics: carry structure, management fees, success metrics
