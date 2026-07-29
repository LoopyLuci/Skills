---
name: boosting-optimization-advanced
description: "Use when optimizing gradient boosting performance."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [boosting, XGBoost, LightGBM, CatBoost, optimization, hyperparameter-tuning]
    related_skills: [boosting-algorithms-deep, hyperparameter-optimization-ml, feature-engineering-automation, random-forest-advanced]
---

# Advanced Boosting Optimization

Optimizing gradient boosting model performance — from hyperparameter tuning strategies (Bayesian, Optuna) through custom loss functions, GPU training, early stopping, and model calibration.

## When to Use

- Squeezing maximum performance from gradient boosting
- Tuning hyperparameters efficiently with Bayesian optimization
- Custom objectives for business-specific metrics
- Training on large datasets with GPU acceleration
- Calibrating probabilities for classification

## Optimization Strategies

```python
class BoostingOptimizer:
    """Optimize gradient boosting hyperparameters with Optuna."""
    
    def optimize_xgboost(self, X, y, n_trials: int = 100) -> Dict:
        import optuna
        
        def objective(trial):
            params = {
                'max_depth': trial.suggest_int('max_depth', 3, 12),
                'learning_rate': trial.suggest_float('lr', 0.01, 0.3, log=True),
                'subsample': trial.suggest_float('subsample', 0.5, 1.0),
                'colsample_bytree': trial.suggest_float('colsample', 0.3, 1.0),
                'min_child_weight': trial.suggest_int('min_child', 1, 10),
                'reg_lambda': trial.suggest_float('lambda', 1e-3, 10, log=True),
                'reg_alpha': trial.suggest_float('alpha', 1e-3, 10, log=True),
            }
            cv_score = cross_val_score(XGBClassifier(**params), X, y, cv=3, scoring='roc_auc')
            return cv_score.mean()
        
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        return study.best_params
```

## Verification Checklist

- [ ] Hyperparameter tuning method chosen (grid, random, Bayesian, Optuna)
- [ ] Cross-validation strategy matches data structure (time series: temporal CV)
- [ ] Custom objective/loss aligned with business metric
- [ ] Early stopping configured (n_estimators + early_stopping_rounds)
- [ ] GPU training enabled for large datasets
- [ ] Model calibration (Platt scaling or isotonic regression)
- [ ] Feature importance and partial dependence analyzed
- [ ] Ensemble: blending with other model types (stacking)
