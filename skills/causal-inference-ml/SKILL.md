---
name: causal-inference-ml
description: "Use when implementing causal inference methods in ML."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [causal-inference, do-calculus, treatment-effects, DAG, counterfactual]
    related_skills: [ab-testing-experimentation, deep-reinforcement-learning, ml-pipeline-design, agent-reasoning-patterns]
---

# Causal Inference in ML

Applying causal inference methods to machine learning — from causal graphs through treatment effect estimation, counterfactual reasoning, and decision-making.

## When to Use

- Determining whether X causes Y (not just correlates)
- Estimating treatment effects from observational data
- Removing confounding bias from ML models
- Answering "what if" counterfactual questions

## Causal Concepts

```python
CAUSAL_CONCEPTS = {
    'association': 'P(Y|X) — statistical correlation',
    'intervention': 'P(Y|do(X)) — causal effect of intervening',
    'counterfactual': 'P(Y_{X=x} | X=x\') — what if X had been different',
}
```

## Causal Graph (DAG)

```python
class CausalGraph:
    def __init__(self):
        self.nodes = set(); self.edges = []
    
    def add_edge(self, cause: str, effect: str):
        self.nodes.update([cause, effect]); self.edges.append((cause, effect))
    
    def get_confounders(self, x: str, y: str) -> list:
        x_parents = set(p for p, c in self.edges if c == x)
        y_parents = set(p for p, c in self.edges if c == y)
        return list(x_parents & y_parents)
```

## Treatment Effect Estimation

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

def propensity_score_matching(treatment, outcome, features):
    ps_model = LogisticRegression().fit(features, treatment)
    propensity = ps_model.predict_proba(features)[:, 1]
    
    treated = treatment == 1; control = treatment == 0
    effects = []
    for i in np.where(treated)[0]:
        nearest = np.where(control)[0][np.argmin(np.abs(propensity[control] - propensity[i]))]
        effects.append(outcome[i] - outcome[nearest])
    
    return {'ate': np.mean(effects), 'matched_pairs': len(effects)}
```

## Common Pitfalls

1. **Correlation ≠ causation** — always consider confounders
2. **Conditioning on colliders** — opens spurious paths
3. **Selection bias** — non-random treatment assignment; use matching
4. **Hidden confounders** — unmeasured variables bias estimates

## Verification Checklist

- [ ] Causal DAG drawn and reviewed
- [ ] Confounders identified and adjusted for
- [ ] Backdoor criterion satisfied
- [ ] Sensitivity analysis for unmeasured confounding

## See Also

- ab-testing-experimentation — randomized experiments
- deep-reinforcement-learning — causal effects in RL
- ml-pipeline-design — causal inference in pipelines
