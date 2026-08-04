---
name: crop-yield-modeling
description: "Use when modeling crop yields. Machine learning, agronomy."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [agriculture, crop-yield, machine-learning, agronomy, forecasting]
    related_skills: [precision-agriculture, farm-management-software]
---

# Crop Yield Modeling & Forecasting

## Overview
Develop predictive models for crop yield using weather data, soil conditions, satellite imagery, historical yields, and agronomic practices. Covers machine learning approaches (random forest, XGBoost, LSTM), feature engineering, model validation, and integration with farm management systems.

## When to Use
- "Predict crop yields using weather/soason data"
- "Build ML model for yield forecasting"
- "Analyze satellite imagery for crop health"
- "Calibrate yield models with field data"
- "Integrate yield predictions into farm planning"

## Essential Input Features

### Weather Variables
| Feature | Impact | Data Source |
|---------|--------|-------------|
| Growing Degree Days (GDD) | Primary growth driver | Weather stations, NOAA |
| Total precipitation | Water stress indicator | Rainfall gauges |
| Max temperature | Heat stress threshold | Weather stations |
| Vapor Pressure Deficit (VPD) | Transpiration rate | Weather data |
| Solar radiation | Photosynthesis driver | Weather stations |

### Soil Variables
| Feature | Impact | Measurement |
|---------|--------|-------------|
| Available water capacity | Drought resilience | Soil survey, Tensiometer |
| Soil organic matter | Nutrient retention | Soil test |
| pH level | Nutrient availability | Soil test |
| Drainage class | Waterlogging risk | Soil survey |

### Management Variables
| Feature | Impact | Data Source |
|---------|--------|-------------|
| Planting date | Growing season length | Farm records |
| Plant population | Yield potential | Seed drill settings |
| Irrigation timing | Water stress avoidance | Irrigation logs |
| Fertilizer N rate | Protein/yield correlation | Application records |
| Hybrid/varietal | Genetic yield potential | Seed catalog |

## ML Model Implementation
```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

def build_yield_model(farm_data_path, weather_data_path):
    """
    Build ML model for yield prediction
    
    Args:
        farm_data_path: historical farm data (yield, management)
        weather_data_path: weather data for growing season
    
    Returns:
        Trained model and performance metrics
    """
    # Load and merge data
    farm_df = pd.read_csv(farm_data_path)
    weather_df = pd.read_csv(weather_data_path)
    
    # Feature engineering for weather
    weather_df = weather_df.groupby('date').agg({
        'temp_max': 'max',
        'temp_min': 'min',
        'precipitation': 'sum',
        'gdd': 'sum',  # Growing degree days
        'vpd': 'mean'  # Vapor pressure deficit
    }).reset_index()
    
    weather_df['avg_temp'] = (weather_df['temp_max'] + weather_df['temp_min']) / 2
    
    # Key growing season periods (before harvest)
    critical_periods = {
        'emergence_to_vegetative': ('2023-05-01', '2023-06-15'),
        'vegetative_to_flowering': ('2023-06-16', '2023-07-30'),
        'flowering_to_grain_fill': ('2023-07-31', '2023-09-15')
    }
    
    # Calculate accumulated weather for each period
    features = {}
    for period_name, (start, end) in critical_periods.items():
        period_weather = weather_df[
            (weather_df['date'] >= start) & 
            (weather_df['date'] <= end)
        ]
        
        features[f'{period_name}_gdd'] = period_weather['gdd'].sum()
        features[f'{period_name}_precip'] = period_weather['precipitation'].sum()
        features[f'{period_name}_avg_temp'] = period_weather['avg_temp'].mean()
    
    # Merge with farm management data
    model_data = farm_df.merge(
        pd.DataFrame([features]), 
        left_index=True, right_index=True
    )
    
    # Prepare features for ML
    feature_cols = [
        'planting_density', 'fertilizer_n_rate', 'hybrid_year',
        'emergence_to_vegetative_gdd', 'flowering_to_grain_fill_precip',
        'avg_soil_moisture', 'organic_matter_pct'
    ]
    
    X = model_data[feature_cols]
    y = model_data['actual_yield']
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Try multiple models
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    best_model = None
    best_mae = float('inf')
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        
        if mae < best_mae:
            best_mae = mae
            best_model = model
    
    return {
        'model': best_model,
        'feature_importance': dict(zip(feature_cols, best_model.feature_importances_)),
        'mae': round(best_mae, 2),
        'r2_score': round(best_model.score(X_test, y_test), 3)
    }
```

## Model Validation Strategy

### Cross-Validation by Year
```python
def year_stratified_cv(model_data, feature_cols, n_years=10):
    """
    Use leave-year-out cross-validation to test model generalization
    """
    years = sorted(model_data['year'].unique())
    results = []
    
    for test_year in years[-5:]:  # Last 5 years as test
        train_years = [y for y in years if y < test_year]
        
        train_data = model_data[model_data['year'].isin(train_years)]
        test_data = model_data[model_data['year'] == test_year]
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(train_data[feature_cols], train_data['actual_yield'])
        
        predictions = model.predict(test_data[feature_cols])
        mae = mean_absolute_error(test_data['actual_yield'], predictions)
        
        results.append({
            'test_year': test_year,
            'training_years': train_years,
            'mae': round(mae, 2),
            'r2': round(r2_score(test_data['actual_yield'], predictions), 3)
        })
    
    return results
```

## Integration with Farm Management

```python
class YieldForecast:
    def __init__(self, model, current_season_data):
        self.model = model
        self.data = current_season_data
        
    def get_forecast(self, confidence_level=0.8):
        """
        Generate yield forecast with confidence intervals
        """
        point_estimate = self.model.predict([self.data])[0]
        
        # Bootstrap confidence interval
        predictions = []
        for _ in range(1000):
            # Resample training data with replacement
            bootstrap_sample = np.random.choice(
                self.training_yields, 
                size=len(self.training_yields), 
                replace=True
            )
            predictions.append(np.random.normal(
                point_estimate, 
                np.std(bootstrap_predictions)
            ))
        
        ci_lower = np.percentile(predictions, (1-confidence_level)*50)
        ci_upper = np.percentile(predictions, (1+confidence_level)*50)
        
        return {
            'point_estimate': round(point_estimate, 2),
            'confidence_interval': [round(ci_lower, 2), round(ci_upper, 2)],
            'risk_level': self.classify_risk(point_estimate)
        }

def classify_risk(self, predicted_yield):
    """
    Classify yield risk level
    """
    historical_avg = self.historical_yields.mean()
    deviation = (predicted_yield - historical_avg) / historical_avg
    
    if deviation > 0.15:
        return 'HIGH_YIELD'
    elif deviation > 0.05:
        return 'MODERATE_HIGH'
    elif deviation > -0.05:
        return 'NORMAL'
    elif deviation > -0.15:
        return 'MODERATE_LOW'
    else:
        return 'LOW_YIELD'
```

## Satellite & Remote Sensing Integration

### NDVI-Based Growth Staging
```python
def ndvi_growth_staging(ndvi_timeseries, planting_date, harvest_date):
    """
    Use NDVI to identify crop growth stages and correlate with yield impact
    """
    stages = {
        'emergence': {'ndvi_range': (0.1, 0.3), 'days_after_planting': '10-30'},
        'vegetative': {'ndvi_range': (0.3, 0.6), 'days_after_planting': '30-70'},
        'reproductive': {'ndvi_range': (0.6, 0.8), 'days_after_planting': '70-110'},
        'grain_fill': {'ndvi_range': (0.4, 0.7), 'days_after_planting': '110-140'},
        'senescence': {'ndvi_range': (0.1, 0.4), 'days_after_planting': '140+'}
    }
    
    # Identify peak NDVI timing
    peak_ndvi_date = ndvi_timeseries.loc[
        ndvi_timeseries['ndvi'].idxmax(), 'date'
    ]
    days_to_peak = (peak_ndvi_date - planting_date).days
    
    return {
        'peak_ndvi_date': peak_ndvi_date,
        'days_to_peak': days_to_peak,
        'growth_stage_at_peak': find_stage(days_to_peak, stages),
        'yield_impact_score': calculate_yield_impact(ndvi_timeseries, stages)
    }
```

## Common Pitfalls
1. **Weather data not aligned to growth stages** — accumulating all season's weather instead of critical periods
2. **Not accounting for year-to-year variability** — climate change shifts optimal timing
3. **Using too few training years** — models need 8-10+ years of data
4. **Ignoring interaction effects** — fertilizer effectiveness depends on weather
5. **Satellite cloud cover gaps** — missing data during critical growth stages
6. **Not validating with independent farms** — models overfit to local conditions
7. **Assuming linear relationships** — crop responses are often non-linear
8. **Not updating models** — conditions change annually
9. **Ignoring spatial variability** — field zones need zone-specific models
10. **Over-relying on satellite data alone** — combine with ground truth

## Verification Checklist
- [ ] Weather features calculated per growth stage, not entire season
- [ ] Model trained on ≥8 years of historical data
- [ ] Cross-validation by year (not random split)
- [ ] Feature importance analysis completed
- [ ] Confidence intervals calculated via bootstrapping
- [ ] Satellite NDVI aligned with growth staging
- [ ] Independent validation on separate farms
- [ ] Model updates scheduled for each harvest season
- [ ] Spatial variability addressed with zone-based modeling
- [ ] Risk classification aligned with farm management decisions