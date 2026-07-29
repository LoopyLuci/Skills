---
name: data-profiling-quality
description: "Use when profiling data and assessing data quality."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-profiling, data-quality, validation, cleanup, pandas-profiling, great-expectations]
    related_skills: [data-cleaning-patterns, feature-engineering-automation, ml-pipeline-design, data-labeling-strategies]
---

# Data Profiling and Quality

Profiling datasets and assessing data quality — from automated profiling (YData Profiling, Great Expectations) through quality dimensions, anomaly detection, and data validation.

## When to Use

- Understanding a new dataset (profiling)
- Setting up data quality checks for pipelines
- Detecting data drift between training and production
- Validating data before model training
- Building data quality dashboards

## Quality Dimensions

```python
DATA_QUALITY_DIMENSIONS = {
    'completeness': 'Missing values, null rates, empty strings',
    'uniqueness': 'Duplicate records, duplicate values in unique columns',
    'validity': 'Values conform to schema (type, format, range, domain)',
    'consistency': 'Values consistent across related columns/tables',
    'accuracy': 'Values represent real-world entities correctly',
    'timeliness': 'Data is current enough for the use case',
}

class DataProfiler:
    """Profile a dataset for quality assessment."""
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.profile = {}
    
    def analyze(self) -> Dict:
        self.profile['rows'] = len(self.df)
        self.profile['columns'] = len(self.df.columns)
        self.profile['missing'] = {}
        self.profile['duplicates'] = self.df.duplicated().sum()
        
        for col in self.df.columns:
            missing = self.df[col].isnull().mean() * 100
            dtype = str(self.df[col].dtype)
            unique = self.df[col].nunique()
            
            self.profile['missing'][col] = round(missing, 1)
            if dtype.startswith('float') or dtype.startswith('int'):
                self.profile[col] = {
                    'dtype': dtype, 'missing_pct': round(missing, 1),
                    'unique': unique, 'min': self.df[col].min(),
                    'max': self.df[col].max(), 'mean': round(self.df[col].mean(), 2),
                }
        
        return self.profile
```

## Common Pitfalls

1. **Profiling without action** — running profiling once and never fixing issues
2. **No automated checks** — manual quality checks don't happen regularly
3. **Ignoring data drift** — data quality changes over time; monitor continuously
4. **Schema validation only** — valid schema doesn't mean valid data (garbage values in valid formats)
5. **No domain-specific rules** — general profiling misses business-specific quality rules

## Verification Checklist

- [ ] Automated data profiling run on new datasets
- [ ] Data quality checks defined for each pipeline stage
- [ ] Great Expectations or similar validation suite implemented
- [ ] Missing value thresholds with alerts
- [ ] Duplicate detection and handling policy
- [ ] Data drift monitoring (training vs production distributions)
- [ ] Data quality dashboard with trends over time
- [ ] Action plan for quality issues (who fixes, by when)
