---
name: model-monitoring-drift
description: "Use when monitoring ML models for drift and degradation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [model-monitoring, drift-detection, data-drift, concept-drift, ML-observability]
    related_skills: [model-registry-management, ml-pipeline-design, anomaly-detection-ml, ml-experiment-tracking]
---

# Model Monitoring and Drift Detection

Monitoring ML models in production for data drift, concept drift, and performance degradation — from statistical drift detection through automated retraining triggers.

## When to Use

- ML models in production that may degrade over time
- Detecting when training data distribution differs from production
- Identifying when relationships between features and target change
- Automating retraining decisions based on drift signals
- Building ML observability and monitoring dashboards

## Drift Detection Methods

```python
DRIFT_TYPES = {
    'data_drift': 'Input feature distribution changes (e.g., user demographics shift)',
    'concept_drift': 'Relationship between features and target changes (e.g., buying behavior shifts)',
    'prediction_drift': 'Model output distribution shifts over time',
}

class DriftDetector:
    """Detect statistical drift in model inputs and outputs."""
    
    @staticmethod
    def psdi(data_current, data_reference, threshold: float = 0.1) -> Dict:
        """Population Stability Index — measures distribution shift."""
        from scipy import stats
        # Bin both distributions
        bins = np.histogram_bin_edges(data_reference, bins=10)
        ref_hist = np.histogram(data_reference, bins=bins)[0] + 1e-6
        cur_hist = np.histogram(data_current, bins=bins)[0] + 1e-6
        
        ref_pct = ref_hist / ref_hist.sum()
        cur_pct = cur_hist / cur_hist.sum()
        
        psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
        return {'psi': round(psi, 4), 'drifted': psi > threshold}
    
    @staticmethod
    def ks_test(data_current, data_reference, threshold: float = 0.05) -> Dict:
        """Kolmogorov-Smirnov test for distribution difference."""
        from scipy import stats
        stat, p_value = stats.ks_2samp(data_reference, data_current)
        return {'statistic': round(stat, 4), 'p_value': round(p_value, 4), 'drifted': p_value < threshold}
```

## Common Pitfalls

1. **Alert fatigue** — every feature drifts slightly; set meaningful thresholds
2. **Seasonal drift** — natural cycles (holidays, weekends) trigger false alerts; model seasonality
3. **No ground truth** — concept drift needs labels to detect; may have delayed feedback
4. **Monitoring too many metrics** — focus on key features and overall prediction drift
5. **Reaction without analysis** — drift alert leads to automatic retraining; analyze root cause first

## Verification Checklist

- [ ] Baseline reference dataset established (training data or initial production window)
- [ ] Drift detection method chosen per feature type (PSI for categorical, KS for numeric)
- [ ] Alert thresholds configured (not too sensitive, not too lenient)
- [ ] Dashboard for visualizing drift over time
- [ ] Automated response defined (alert, retraining trigger, human review)
- [ ] Seasonality accounted for in drift calculations
- [ ] Concept drift detection (if ground truth available)
