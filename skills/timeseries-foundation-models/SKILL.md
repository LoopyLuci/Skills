---
name: timeseries-foundation-models
description: "Use when using foundation models for time series."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [timeseries, foundation-models, Lag-Llama, TimesFM, forecasting, patchTST]
    related_skills: [timeseries-forecasting-ml, anomaly-detection-ml, embedding-models-patterns, transformer-architectures]
---

# Time Series Foundation Models

Using foundation models for time series forecasting and analysis — from Lag-Llama and TimesFM through prompt-based forecasting, zero-shot transfer, and fine-tuning.

## When to Use

- Zero-shot time series forecasting without training
- Transfer learning across different time series datasets
- Few-shot fine-tuning for domain-specific series
- Probabilistic forecasting with foundation models

## Foundation Models

```python
FOUNDATION_MODELS = {
    'lag_llama': 'LLaMA-based, lag features as tokens, probabilistic forecasts, uncertainty',
    'timesfm': 'Google, decoder-only, 100M-200M params, patch-based, zero-shot',
    'patchtst': 'Transformer with patching, self-supervised pretraining, interpretable',
    'chronos': 'Amazon, tokenized time series, language model architecture, zero-shot',
}

class TimeSeriesFoundation:
    """Use foundation models for zero-shot forecasting."""
    
    def forecast_zero_shot(self, past_values: np.array, 
                           model: str = 'timesfm', horizon: int = 24) -> Dict:
        if model == 'timesfm':
            import timesfm
            tfm = timesfm.TimesFm(hparams=timesfm.TimesFmHparams(
                backend='gpu', num_layers=20, context_len=512, horizon_len=horizon))
            forecast = tfm.forecast_on_df(
                inputs=[past_values], freq='H'
            )
            return {'mean': forecast.mean, 'std': forecast.std}
        return {}

# Lag feature construction (Lag-Llama style)
def create_lag_features(series: np.array, lags: List[int] = [1, 7, 30, 90]) -> np.array:
    return np.column_stack([np.roll(series, -lag) for lag in lags])
```

## Verification Checklist

- [ ] Foundation model selected (Lag-Llama, TimesFM, Chronos, PatchTST)
- [ ] Zero-shot performance baseline established
- [ ] Context length appropriate for forecast horizon
- [ ] Fine-tuning data (if few-shot) prepared
- [ ] Probabilistic forecasts (mean + quantiles) evaluated
- [ ] Seasonality and trend handling verified
- [ ] Model compared against statistical baseline (ARIMA, ETS)
