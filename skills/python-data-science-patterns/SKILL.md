---
name: python-data-science-patterns
description: "Use when doing data science with Python: pandas, numpy, viz."
category: mlops
tags: [python, data-science, pandas, numpy, visualization]
---
# Python Data Science Patterns

Core data science patterns with pandas, numpy, matplotlib, and scikit-learn.

## Pandas Workflow

```python
import pandas as pd
import numpy as np

# Load with type optimization
df = pd.read_csv("data.csv", 
    dtype={"category_col": "category"},
    parse_dates=["date_col"],
    usecols=lambda c: c != "unnecessary_column")

# Quick profile
df.info()           # dtypes, non-null, memory
df.describe()       # stats
df.isnull().sum()   # missing values
df.nunique()        # unique counts

# Filtering (use .query for readability)
df_filtered = df.query("age > 25 and city == 'New York'")

# Group-aggregate
result = (df.groupby("category", as_index=False)
    .agg(
        total=("price", "sum"),
        avg=("price", "mean"),
        count=("id", "nunique"),
        std=("price", "std"),
    ))
```

## NumPy Techniques

```python
# Vectorized operations (always prefer over loops)
arr = np.random.randn(1000000)
result = np.where(arr > 0, arr * 2, arr / 2)  # fast C-level

# Broadcasting
matrix = np.random.randn(100, 50)
row_mean = matrix.mean(axis=1, keepdims=True)
centered = matrix - row_mean  # broadcasts automatically

# Efficient reductions
np.add.reduceat(arr, indices)   # segmented sum
np.cumsum(arr)                  # cumulative sum
```

## Visualization Patterns

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Distribution analysis
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.histplot(df["price"], kde=True, ax=axes[0,0])
sns.boxplot(x="category", y="price", data=df, ax=axes[0,1])
sns.scatterplot(x="feature1", y="feature2", hue="target", data=df, ax=axes[1,0])
sns.heatmap(df.corr(), annot=True, cmap="RdBu", ax=axes[1,1])
plt.tight_layout()
```

## Pitfalls

- Pandas chained indexing (df[df.a > 0]["b"]) is unpredictable — use .loc
- GroupBy without as_index=False leaves a MultiIndex
- CSV loading without dtype optimization uses excessive memory
- Matplotlib state machine causes cross-plot contamination — use figures explicitly
- Seaborn default styles override matplotlib globals
