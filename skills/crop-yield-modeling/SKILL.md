---
name: crop-yield-modeling
description: Use when modeling crop yields. Machine learning, agronomy.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [agriculture, crop-yield, machine-learning, agronomy, forecasting]
---

# Crop Yield Modeling

"Use when modeling crop yields. Machine learning, agronomy."

## Trigger

Activate this skill when the user mentions:
- agriculture,  crop-yield,  machine-learning,  agronomy,  forecasting workflows or issues
- Building, fixing, or optimizing crop yield modeling
- Questions about agriculture best practices

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

`agriculture, crop-yield, machine-learning, agronomy, forecasting`

---

*LoopyLuci/Skills - 2026-09-24*
