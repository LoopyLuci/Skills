---
name: causal-inference-advanced
description: "Use when implementing advanced causal inference in ML."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [causal-inference, DAG, do-calculus, instrumental-variables, double-ML, heterogeneous-effects]
    related_skills: [causal-inference-ml, ab-testing-experimentation, deep-reinforcement-learning, model-interpretability-deep]
---

# Advanced Causal Inference

Implementing advanced causal inference in ML — from DAG discovery and instrumental variables through double/debiased ML, heterogeneous treatment effects, and causal structure learning.

## When to Use

- Estimating causal effects from observational data
- Discovering causal structure from data
- Learning heterogeneous treatment effects (CATE)
- Instrumental variable methods for unobserved confounding
- Double ML for high-dimensional causal inference

## Advanced Methods

```python
class DoubleML:
    """Double/Debiased Machine Learning for ATE estimation."""
    def __init__(self, model_y, model_t):
        self.model_y = model_y  # Outcome model
        self.model_t = model_t  # Treatment model
    
    def fit(self, X, T, Y):
        # Cross-fitting
        from sklearn.model_selection import KFold
        cv = KFold(n_splits=5)
        residuals_t = np.zeros_like(T, dtype=float)
        residuals_y = np.zeros_like(Y, dtype=float)
        
        for train_idx, test_idx in cv.split(X):
            self.model_t.fit(X[train_idx], T[train_idx])
            self.model_y.fit(X[train_idx], Y[train_idx])
            residuals_t[test_idx] = T[test_idx] - self.model_t.predict(X[test_idx])
            residuals_y[test_idx] = Y[test_idx] - self.model_y.predict(X[test_idx])
        
        # ATE = Cov(residuals_t, residuals_y) / Var(residuals_t)
        ate = np.cov(residuals_t, residuals_y)[0, 1] / np.var(residuals_t)
        return {'ate': round(ate, 4)}
```

## Verification Checklist

- [ ] Causal DAG specified or discovered from data
- [ ] Identification strategy chosen (backdoor, IV, difference-in-differences, RDD)
- [ ] Double ML with cross-fitting for high-dimensional settings
- [ ] Heterogeneous treatment effects (CATE) estimated
- [ ] Sensitivity analysis for unmeasured confounding
- [ ] Overlap and positivity assumptions checked
- [ ] Results reported with confidence intervals
