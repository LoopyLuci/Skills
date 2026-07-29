---
name: feature-engineering-automation
description: "Use when automating feature engineering for ML models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [feature-engineering, automated-features, feature-tools, feature-store, feature-selection]
    related_skills: [ml-pipeline-design, data-augmentation-techniques, embedding-models-patterns, ml-experiment-tracking]
---

# Feature Engineering Automation

Automating feature engineering for ML pipelines — from automated feature generation and selection through feature stores, embedding generation, and feature importance analysis.

## When to Use

- Engineering features for tabular ML models at scale
- Building automated feature pipelines for production
- Creating reusable feature definitions for serving
- Selecting the most important features from hundreds of candidates
- Implementing feature stores for consistency across training and serving

## Automated Feature Generation

```python
import pandas as pd
import numpy as np
from itertools import combinations
from typing import List, Callable

class AutoFeatureEngineer:
    """Generate features automatically from raw data."""
    
    TRANSFORMATIONS = {
        'log': np.log1p,
        'sqrt': np.sqrt,
        'square': lambda x: x**2,
        'inverse': lambda x: 1 / (x.abs() + 1),
    }
    
    @staticmethod
    def generate_numeric_features(df: pd.DataFrame, 
                                   numerical_cols: List[str]) -> pd.DataFrame:
        """Generate derived features from numerical columns."""
        new_features = df.copy()
        
        for col in numerical_cols:
            # Unary transformations
            for name, func in AutoFeatureEngineer.TRANSFORMATIONS.items():
                try:
                    new_features[f'{col}_{name}'] = func(df[col])
                except: pass
        
        # Pairwise interactions (top 10 highest correlation pairs)
        if len(numerical_cols) >= 2:
            for a, b in list(combinations(numerical_cols, 2))[:10]:
                new_features[f'{a}_x_{b}'] = df[a] * df[b]
                new_features[f'{a}_plus_{b}'] = df[a] + df[b]
        
        # Binning
        for col in numerical_cols[:3]:
            new_features[f'{col}_binned'] = pd.qcut(df[col], q=5, labels=False, duplicates='drop')
        
        return new_features
    
    @staticmethod
    def generate_date_features(df: pd.DataFrame, 
                                date_cols: List[str]) -> pd.DataFrame:
        """Generate features from date columns."""
        new_features = df.copy()
        for col in date_cols:
            dates = pd.to_datetime(df[col])
            new_features[f'{col}_year'] = dates.dt.year
            new_features[f'{col}_month'] = dates.dt.month
            new_features[f'{col}_day'] = dates.dt.day
            new_features[f'{col}_dayofweek'] = dates.dt.dayofweek
            new_features[f'{col}_quarter'] = dates.dt.quarter
            new_features[f'{col}_is_weekend'] = (dates.dt.dayofweek >= 5).astype(int)
        return new_features
```

## Feature Selection

```python
class FeatureSelector:
    """Select most important features from generated candidates."""
    
    @staticmethod
    def mutual_information(X: pd.DataFrame, y: pd.Series, 
                            top_k: int = 20) -> List[str]:
        """Select top K features by mutual information."""
        from sklearn.feature_selection import mutual_info_classif
        mi_scores = mutual_info_classif(X.fillna(0), y)
        top_indices = np.argsort(mi_scores)[-top_k:][::-1]
        return [X.columns[i] for i in top_indices]
    
    @staticmethod
    def feature_importance(model, X: pd.DataFrame, 
                           top_k: int = 20) -> List[str]:
        """Select top K features from trained model."""
        importances = model.feature_importances_
        top_indices = np.argsort(importances)[-top_k:][::-1]
        return [X.columns[i] for i in top_indices]
```

## Common Pitfalls

1. **Feature leakage** — generating features using future information; never use target in features
2. **Too many features** — curse of dimensionality; use selection to keep top 20-50
3. **Training/serving skew** — features computed differently at training vs serving; use feature store
4. **Expensive features** — features that require complex joins slow inference; measure cost
5. **Correlated features** — high multicollinearity; use variance inflation factor to detect

## Verification Checklist

- [ ] Feature generation produces reasonable candidates (not random noise)
- [ ] Feature selection reduces dimensionality to manageable number
- [ ] No future leakage (time series: no future data in features)
- [ ] Training and serving feature computation identical
- [ ] Feature importance correlated with business understanding
- [ ] Feature store (or equivalent) for consistent offline/online features
