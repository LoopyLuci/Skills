---
name: data-cleaning-patterns
description: "Clean messy datasets nulls outliers duplicates normalization"
---

# Data Cleaning Patterns

## With pandas
```python
import pandas as pd

df = pd.read_csv("data.csv")

# Drop duplicates
df = df.drop_duplicates()

# Handle nulls
df = df.fillna(0)           # Fill with default
df = df.dropna(subset=["id"])  # Drop rows missing key

# Outliers (IQR method)
Q1, Q3 = df["price"].quantile([0.25, 0.75])
iqr = Q3 - Q1
mask = (df["price"] >= Q1 - 1.5*iqr) & (df["price"] <= Q3 + 1.5*iqr)
df = df[mask]

# Type coercion
df["date"] = pd.to_datetime(df["date"])
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
```
