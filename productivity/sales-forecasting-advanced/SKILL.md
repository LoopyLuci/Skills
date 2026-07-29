---
name: sales-forecasting-advanced
description: "Use when building advanced sales forecasting models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales-forecasting, pipeline-analysis, stages, probability, velocity, predictions]
    related_skills: [revenue-operations-revops, crm-sales-pipeline, saas-metrics-reporting, business-metrics-kpis]
---

# Advanced Sales Forecasting

Building accurate sales forecasts — from pipeline-based and historical methods through AI-driven predictions, forecast categories, and deal inspection.

## When to Use

- Building a repeatable sales forecasting process
- Moving beyond "gut feel" forecasts to data-driven predictions
- Forecasting at different levels (rep, team, company, product)
- Identifying forecast risks and upside opportunities
- Presenting forecasts to board and investors

## Forecasting Methods

```python
FORECASTING_METHODS = {
    'pipeline_weighted': 'Deal value × probability per stage, weighted sum',
    'historical_velocity': 'Based on historical win rates and velocity by rep/segment',
    'time_series': 'Statistical projection from historical booking trends',
    'ai_predicted': 'ML model trained on historical deal data predicting close likelihood',
    'commit_plus_best': 'Committed (high confidence) + best case (medium confidence)',
}

class SalesForecast:
    """Generate sales forecasts from pipeline data."""
    def __init__(self):
        self.deals = []
        self.historical_win_rate = 0.2
        self.historical_velocity = 45  # avg days to close
    
    def weighted_forecast(self) -> Dict:
        total_weighted = sum(d['value'] * d['probability'] for d in self.deals)
        total_pipeline = sum(d['value'] for d in self.deals)
        
        return {
            'weighted_forecast': total_weighted,
            'pipeline_total': total_pipeline,
            'deal_count': len(self.deals),
            'commit_deals': [d for d in self.deals if d['probability'] >= 0.9],
            'upside': [d for d in self.deals if 0.5 <= d['probability'] < 0.9],
        }
```

## Common Pitfalls

1. **Optimism bias** — reps overestimate close dates and probabilities; use data-driven calibration
2. **No stage-based probability** — flat 50% for all deals ignores actual conversion patterns
3. **Ignoring historical trends** — seasonal patterns (Q4 spikes, summer slumps) affect forecast
4. **No bottoms-up + top-down** — only bottoms-up misses macro trends; use both
5. **Forecast as target** — forecast should be what you'll likely close, not your goal

## Verification Checklist

- [ ] Forecasting method documented (weighted pipeline, historical, AI, or hybrid)
- [ ] Stage probabilities based on actual historical conversion data
- [ ] Forecast categories defined (commit, best case, pipeline)
- [ ] Deal inspection process (common forecast risks)
- [ ] Forecast accuracy tracked and reported
- [ ] Bias correction applied (optimism discount)
- [ ] Forecast updated weekly with latest pipeline data
