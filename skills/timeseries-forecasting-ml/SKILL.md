---
name: timeseries-forecasting-ml
description: "Use when building time series forecasting systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [timeseries, forecasting, ARIMA, Prophet, LSTM, transformers, temporal]
    related_skills: [anomaly-detection-ml, data-augmentation-techniques, ml-pipeline-design, custom-neural-architecture-design]
---

# Time Series Forecasting with ML

Building time series forecasting systems — from classical methods (ARIMA, exponential smoothing) through gradient boosting and deep learning (LSTM, Transformers, PatchTST).

## When to Use

- Demand forecasting (retail, inventory, capacity planning)
- Financial forecasting (stock prices, volatility, risk)
- Resource monitoring (CPU, memory, network traffic prediction)
- Sensor data prediction (IoT, industrial)
- Anomaly detection in time series data
- Energy load or weather forecasting

## Methods Comparison

| Method | Data Requirements | Forecast Horizon | Interpretability | Complexity |
|--------|------------------|-----------------|-----------------|-------------|
| Naive/Drift | Very low | Short | High | None |
| Exponential Smoothing | Low | Short | High | Low |
| ARIMA/SARIMA | Medium | Short | High | Medium |
| Prophet | Medium | Medium | High | Low |
| LightGBM/XGBoost | High | Short-Medium | Medium | Medium |
| LSTM/GRU | High | Medium | Low | High |
| Temporal Transformers | Very high | Long | Low | Very high |
| PatchTST | High | Long | Low | High |

## Classical Methods

### Exponential Smoothing

```python
import numpy as np

class ExponentialSmoothing:
    @staticmethod
    def simple(series, alpha=0.3, forecast_steps=10):
        result = [series[0]]
        for i in range(1, len(series)):
            result.append(alpha * series[i] + (1 - alpha) * result[-1])
        forecasts = [result[-1]] * forecast_steps
        return result, forecasts
    
    @staticmethod
    def holt_winters(series, alpha=0.3, beta=0.1, gamma=0.1, seasonality=12, forecast_steps=10):
        n = len(series)
        level, trend = series[0], series[1] - series[0] if len(series) > 1 else 0
        seasons = [series[i] / (level + (i+1) * trend) for i in range(min(seasonality, n))]
        
        fitted = []
        for i in range(n):
            s_idx = i % seasonality
            forecast = (level + trend) * seasons[s_idx]
            fitted.append(forecast)
            new_level = alpha * (series[i] / seasons[s_idx]) + (1 - alpha) * (level + trend)
            new_trend = beta * (new_level - level) + (1 - beta) * trend
            seasons[s_idx] = gamma * (series[i] / new_level) + (1 - gamma) * seasons[s_idx]
            level, trend = new_level, new_trend
        
        forecasts = [(level + (i+1) * trend) * seasons[(n + i) % seasonality] for i in range(forecast_steps)]
        return fitted, forecasts
```

### ARIMA

```python
from statsmodels.tsa.arima.model import ARIMA

def fit_arima(series, order=(1,1,1), seasonal_order=(1,1,1,12)):
    model = ARIMA(series, order=order, seasonal_order=seasonal_order)
    return model.fit()
```

## Gradient Boosting with Feature Engineering

```python
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

class FeatureEngineeredForecast:
    @staticmethod
    def create_features(df, target_col, max_lag=24, window_sizes=[6, 12, 24]):
        df = df.copy()
        for lag in range(1, max_lag + 1):
            df[f'lag_{lag}'] = df[target_col].shift(lag)
        for w in window_sizes:
            df[f'rolling_mean_{w}'] = df[target_col].rolling(w).mean()
            df[f'rolling_std_{w}'] = df[target_col].rolling(w).std()
        if isinstance(df.index, pd.DatetimeIndex):
            df['hour'] = df.index.hour; df['dayofweek'] = df.index.dayofweek
            df['month'] = df.index.month; df['weekend'] = (df.index.dayofweek >= 5).astype(int)
        return df.dropna()
    
    def train(self, df, target_col, test_size=24):
        df_feat = self.create_features(df, target_col)
        train = df_feat.iloc[:-test_size]; test = df_feat.iloc[-test_size:]
        feature_cols = [c for c in train.columns if c != target_col]
        model = GradientBoostingRegressor(n_estimators=500, max_depth=5, learning_rate=0.05, random_state=42)
        model.fit(train[feature_cols], train[target_col])
        return model, model.predict(test[feature_cols])
```

## Common Pitfalls

1. **Data leakage** — using future data to predict past; always use temporal split
2. **Seasonality ignored** — many methods assume no seasonality; check and model it
3. **Stationarity** — many methods assume stationary data; difference first
4. **Error compounding** — multi-step errors compound; use direct or recursive strategies
5. **Distribution changes** — time series drift; retrain or use adaptive models
6. **Single split evaluation** — use time series cross-validation (expanding window)

## Verification Checklist

- [ ] Temporal train/test split (no future leakage)
- [ ] Stationarity checked (ADF test)
- [ ] Seasonality identified and modeled
- [ ] Multiple methods compared (naive → best)
- [ ] Walk-forward validation performed
- [ ] Prediction intervals estimated

## See Also

- anomaly-detection-ml — detecting anomalies in time series
- data-augmentation-techniques — augmenting time series data
- ml-pipeline-design — serving forecast models
