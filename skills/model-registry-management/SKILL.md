---
name: model-registry-management
description: "Use when managing ML model versions and registries."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [model-registry, model-versioning, deployment, governance, staging, production]
    related_skills: [ml-experiment-tracking, ml-deployment-serving, ml-pipeline-design, model-evaluation-metrics]
---

# Model Registry Management

"Use when managing ML model versions and registries."

## Trigger

Activate this skill when the user mentions:
- model-registry,  model-versioning,  deployment,  governance,  staging,  production workflows or issues
- Building, fixing, or optimizing model registry management
- Questions about model-registry best practices

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

`model-registry, model-versioning, deployment, governance, staging, production`

---

*LoopyLuci/Skills - 2026-09-24*
