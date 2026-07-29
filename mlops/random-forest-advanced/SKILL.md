---
name: random-forest-advanced
description: "Use when implementing advanced random forest models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [random-forest, ensemble, bagging, decision-trees, feature-importance]
    related_skills: [boosting-algorithms-deep, hyperparameter-optimization-ml, feature-engineering-automation, interpretable-ml]
---

# Advanced Random Forest

Implementing advanced random forest models — from ensemble construction and hyperparameter tuning through feature importance, out-of-bag evaluation, and interpretability.

## When to Use

- Tabular data where interpretability matters
- Building robust models that resist overfitting
- Feature importance analysis and selection
- Unsupervised learning (proximity matrices, anomaly detection)
- Handling missing data and mixed data types

## Random Forest Internals

```python
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class AdvancedRandomForest:
    """Advanced random forest with interpretation tools."""
    
    OPTIMAL_PARAMS = {
        'n_estimators': 300,  # More trees = better convergence
        'max_depth': 10,      # Control overfitting
        'min_samples_leaf': 5, # Smoother decision boundaries
        'max_features': 'sqrt', # sqrt(p) for classification
        'bootstrap': True,
        'oob_score': True,     # Out-of-bag score (internal validation)
        'class_weight': 'balanced',  # Handle imbalance
    }
    
    @staticmethod
    def feature_importance(rf, feature_names: List[str], top_k: int = 20):
        importances = rf.feature_importances_
        std = np.std([tree.feature_importances_ for tree in rf.estimators_], axis=0)
        indices = np.argsort(importances)[-top_k:][::-1]
        
        results = []
        for i in indices:
            results.append({
                'feature': feature_names[i],
                'importance': round(importances[i], 4),
                'std': round(std[i], 4),
                'ci_95': round(1.96 * std[i] / np.sqrt(len(rf.estimators_)), 4),
            })
        return results
    
    @staticmethod
    def partial_dependence(rf, X, feature_idx: int, 
                           grid_resolution: int = 50) -> np.array:
        """Calculate partial dependence for a single feature."""
        from sklearn.inspection import partial_dependence
        pd_results = partial_dependence(rf, X, [feature_idx], 
                                         grid_resolution=grid_resolution)
        return pd_results['average'][0], pd_results['values'][0]
```

## Common Pitfalls

1. **Too many trees for no gain** — 300 trees vs 1000 trees: minimal improvement, double the inference time
2. **Overfitting on noisy data** — random forest can still overfit on very noisy data; limit max_depth
3. **Correlated features dominate** — highly correlated features split importance; use permutation importance
4. **Poor extrapolation** — random forests can't extrapolate beyond training range; use linear model for trends
5. **Imbalanced classes** — default random forest optimizes for accuracy, not recall for minority class

## Verification Checklist

- [ ] n_estimators chosen (300+ for final model, 100 for prototyping)
- [ ] max_depth and min_samples_leaf tuned via cross-validation
- [ ] oob_score enabled for internal validation
- [ ] Feature importance analyzed (permutation + impurity-based)
- [ ] Partial dependence plots for top features
- [ ] Class imbalance handled (class_weight or sampling)
- [ ] Model compared with gradient boosting baseline
- [ ] Inference performance optimized (tree pruning, ONNX export)
