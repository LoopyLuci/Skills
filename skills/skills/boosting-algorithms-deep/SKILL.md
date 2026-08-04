---
name: boosting-algorithms-deep
description: "Use when implementing gradient boosting algorithms."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [boosting, XGBoost, LightGBM, CatBoost, gradient-boosting, ensemble]
    related_skills: [random-forest-advanced, feature-engineering-automation, hyperparameter-optimization-ml, model-evaluation-metrics]
---

# Boosting Algorithms — Deep Dive

Deep implementation of gradient boosting algorithms — from XGBoost through LightGBM, CatBoost, and custom boosting implementations with optimization strategies.

## When to Use

- Tabular/structured data where boosting consistently wins
- Building high-performance models for classification and regression
- Feature importance analysis and model interpretability
- Kaggle competitions and benchmark tasks
- Production ML where interpretability matters

## Algorithm Comparison

```python
BOOSTING_ALGORITHMS = {
    'xgboost': {
        'strength': 'Mature, well-optimized, handles missing values, regularization',
        'weakness': 'Can be slow on high-dimensional sparse data',
        'tree_method': 'hist, approx, exact',
        'best_for': 'General purpose, small-medium datasets',
    },
    'lightgbm': {
        'strength': 'Fastest training, lowest memory, native categorical support',
        'weakness': 'Can overfit on small data, sensitive to leaf-wise growth',
        'best_for': 'Large datasets, high-dimensional, categorical features',
    },
    'catboost': {
        'strength': 'Best categorical handling, great default params, robust',
        'weakness': 'Slower on large data, less widespread than XGBoost',
        'best_for': 'Datasets with many categorical features, default performance',
    },
}

# XGBoost parameter template
XGB_PARAMS = {
    'objective': 'binary:logistic',
    'max_depth': 6,
    'learning_rate': 0.05,
    'n_estimators': 1000,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'gamma': 0.1,
    'reg_lambda': 1.0,
    'reg_alpha': 0.0,
    'min_child_weight': 5,
    'early_stopping_rounds': 50,
}
```

## Feature Importance

```python
class BoostedFeatureAnalysis:
    """Analyze feature importance from boosting models."""
    
    @staticmethod
    def plot_importance(model, feature_names: List[str], top_k: int = 20):
        importance = model.feature_importances_
        indices = np.argsort(importance)[-top_k:][::-1]
        
        print("Feature Importance (Top-k):")
        print("-" * 40)
        for i, idx in enumerate(indices, 1):
            print(f"{i:2d}. {feature_names[idx]:30s} {importance[idx]:.4f}")
```

## Common Pitfalls

1. **Overfitting with too many trees** — use early stopping on validation set
2. **Default params not optimal** — tune max_depth, learning_rate, subsample
3. **Categorical encoding mistakes** — let CatBoost/LightGBM handle categories natively
4. **Ignoring class imbalance** — use scale_pos_weight or sampling
5. **No cross-validation** — single train/val split is unreliable

## Verification Checklist

- [ ] Algorithm chosen based on data characteristics
- [ ] Early stopping configured on validation
- [ ] Hyperparameters tuned (learning rate, depth, subsample)
- [ ] Feature importance analyzed
- [ ] Model compared against baseline (simple model or linear)
- [ ] Categorical features handled correctly (native or encoded)
