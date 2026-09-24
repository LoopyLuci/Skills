---
name: marketing-attribution-modeling
description: Use when implementing marketing attribution and ROI models.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [marketing-attribution, roi, multi-touch, first-touch, last-touch, data-driven]
---

# Marketing Attribution Modeling

"Use when implementing marketing attribution and ROI models."

## Trigger

Activate this skill when the user mentions:
- marketing-attribution,  ROI,  multi-touch,  first-touch,  last-touch,  data-driven workflows or issues
- Building, fixing, or optimizing marketing attribution modeling
- Questions about marketing-attribution best practices

## Core Concepts

- Model selection and evaluation
- Feature engineering and data prep
- Training methodology
- Deployment and serving patterns
- Monitoring and drift detection

## Step-by-Step Workflow

1. **Frame** — Define problem, success metric, baseline
   - Expected: Clear problem statement
2. **Explore** — EDA, feature analysis
   - Expected: Understanding of data relationships
3. **Build** — Train models, track experiments
   - Expected: Logged reproducible experiments
4. **Evaluate** — Test on holdout, check bias
   - Expected: Evaluation report with confidence
5. **Deploy** — Serve with monitoring
   - Expected: Production model with drift detection

## Tools & Technologies

- Experiment tracking
- Model registry
- Feature store
- Model serving

## Best Practices

- Document decisions and rationale (ADRs, design docs, runbooks)
- Version everything - code, configs, data, and documentation
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethical standards
- Measure outcomes with meaningful metrics

## Common Pitfalls

- **Data leakage** → Overly optimistic metrics → Strict temporal splits
- **No monitoring** → Silent degradation → Monitor prediction distribution

## Tags

`marketing-attribution, ROI, multi-touch, first-touch, last-touch, data-driven`

---

*LoopyLuci/Skills - 2026-09-24*
