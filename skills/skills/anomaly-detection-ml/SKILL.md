---
name: anomaly-detection-ml
description: "Use when implementing ML-based anomaly detection systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [anomaly-detection, outliers, isolation-forest, autoencoder, OCSVM, fraud]
    related_skills: [ml-threat-detection, gpu-anomaly-detector, timeseries-forecasting-ml, ml-pipeline-design]
---

# Anomaly Detection with ML

Implementing anomaly detection systems — from statistical methods through isolation forests, autoencoders, and deep anomaly detection for structured data, time series, and high-dimensional spaces.

## When to Use

- Detecting fraud in financial transactions
- Catching network intrusions or security threats
- Monitoring system metrics for production incidents
- Quality control in manufacturing (defect detection)
- Data cleaning (finding outliers in datasets)
- Sensor fault detection in IoT systems

## Anomaly Types

```
Point Anomalies: single instance is anomalous (e.g., $10,000 withdraw)
Contextual Anomalies: anomalous in a specific context (e.g., 30°C in winter)
Collective Anomalies: a group of points is anomalous together (e.g., DDOS pattern)
```

## Statistical Methods

```python
import numpy as np
from scipy import stats

class StatisticalAnomalyDetector:
    """Simple statistical anomaly detection."""
    
    @staticmethod
    def z_score(data, threshold=3):
        """Z-score: points more than 3 std devs from mean."""
        z = np.abs(stats.zscore(data))
        return z > threshold
    
    @staticmethod
    def iqr(data, multiplier=1.5):
        """Interquartile Range: points outside 1.5×IQR."""
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        return (data < lower) | (data > upper)
    
    @staticmethod
    def mad(data, threshold=3.5):
        """Median Absolute Deviation: robust to outliers itself."""
        median = np.median(data)
        mad = np.median(np.abs(data - median))
        modified_z = 0.6745 * (data - median) / (mad + 1e-8)
        return np.abs(modified_z) > threshold
```

## Isolation Forest

```python
from sklearn.ensemble import IsolationForest

class IsolationForestDetector:
    """Isolation Forest: isolates anomalies by randomly splitting features.
    
    Anomalies are easier to isolate (shorter paths in the tree).
    Works well for high-dimensional data."""
    
    def __init__(self, contamination=0.1, n_estimators=100):
        self.model = IsolationForest(
            contamination=contamination,  # Expected proportion of outliers
            n_estimators=n_estimators,
            random_state=42
        )
    
    def fit(self, X):
        self.model.fit(X)
        return self
    
    def predict(self, X):
        """Returns -1 for anomalies, 1 for normal."""
        return self.model.predict(X)
    
    def score_samples(self, X):
        """Anomaly score: lower = more anomalous."""
        return self.model.score_samples(X)
```

## Autoencoder-Based Detection

```python
import torch
import torch.nn as nn

class AnomalyAutoencoder(nn.Module):
    """Autoencoder for anomaly detection.
    
    Anomalies have higher reconstruction error because the autoencoder
    is trained primarily on normal data."""
    
    def __init__(self, input_dim, encoding_dim=32):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, encoding_dim), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, input_dim)
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
    def anomaly_score(self, x):
        """Reconstruction error as anomaly score."""
        with torch.no_grad():
            reconstructed = self(x)
            error = ((x - reconstructed) ** 2).mean(dim=1)
        return error.numpy()


class VAADetector:
    """Variational Autoencoder for anomaly detection.
    Provides both reconstruction and KL-based anomaly signals."""
    
    def __init__(self, input_dim, latent_dim=16):
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.model = VAE(input_dim, latent_dim)
    
    def anomaly_score(self, x):
        with torch.no_grad():
            recon, mu, logvar = self.model(x)
            recon_error = ((x - recon) ** 2).sum(dim=1)
            kl_div = -0.5 * (1 + logvar - mu**2 - logvar.exp()).sum(dim=1)
            return (recon_error + kl_div).numpy()
```

## Deep One-Class Classification

```python
class DeepSVDD:
    """Deep Support Vector Data Description.
    Maps data into a hypersphere; anomalies fall outside."""
    
    def __init__(self, input_dim, hidden_dims=[64, 32], center=None):
        self.net = self._build_network(input_dim, hidden_dims)
        self.center = center  # Center of hypersphere
        self.R = 0.0  # Radius
    
    def _build_network(self, input_dim, hidden_dims):
        layers = []
        prev = input_dim
        for h in hidden_dims:
            layers.extend([nn.Linear(prev, h), nn.ReLU()])
            prev = h
        return nn.Sequential(*layers)
    
    def train(self, dataloader, epochs=50):
        # Initialize center as mean of network outputs
        features = []
        for x, _ in dataloader:
            features.append(self.net(x))
        self.center = torch.cat(features).mean(dim=0)
        
        optimizer = torch.optim.Adam(self.net.parameters())
        
        for epoch in range(epochs):
            for x, _ in dataloader:
                features = self.net(x)
                dist = (features - self.center).pow(2).sum(dim=1)
                loss = dist.mean()
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
    
    def predict(self, x):
        features = self.net(x)
        dist = (features - self.center).pow(2).sum(dim=1).sqrt()
        return dist > self.R
```

## Online Anomaly Detection

```python
class OnlineAnomalyDetector:
    """Streaming anomaly detection with sliding window statistics."""
    
    def __init__(self, window_size=100, threshold=3.0):
        self.window = []
        self.window_size = window_size
        self.threshold = threshold
        self.mean = 0.0
        self.std = 0.0
    
    def update(self, value):
        """Return True if value is anomalous, update statistics."""
        is_anomaly = False
        if len(self.window) >= 10:  # Need minimum samples
            if abs(value - self.mean) > self.threshold * self.std:
                is_anomaly = True
        
        # Maintain sliding window
        self.window.append(value)
        if len(self.window) > self.window_size:
            self.window.pop(0)
        
        # Update statistics
        self.mean = np.mean(self.window)
        self.std = np.std(self.window)
        
        return is_anomaly
```

## Common Pitfalls

1. **Imbalanced evaluation** — anomaly detection is extremely imbalanced; use precision@k, not accuracy
2. **Label contamination** — assumed-normal training data may contain anomalies; use robust methods
3. **Concept drift** — what's anomalous changes over time; update models continuously
4. **Threshold sensitivity** — changing threshold changes FPR dramatically; calibrate on validation
5. **Curse of dimensionality** — distance metrics become meaningless in high dimensions; use dimensionality reduction
6. **Interpretability** — "it's anomalous" is unhelpful; provide feature-level attribution (why is it anomalous?)

## Verification Checklist

- [ ] Baseline: statistical methods (z-score, IQR) established
- [ ] Multiple methods compared (isolation forest, autoencoder, DeepSVDD)
- [ ] Evaluation uses appropriate metrics (precision@k, AUC-PR)
- [ ] Training data verified to contain mostly normal samples
- [ ] Threshold calibrated on validation data
- [ ] Concept drift handling implemented for production
- [ ] Explainability: top-K contributing features per anomaly

## See Also

- ml-threat-detection — anomaly detection for security
- gpu-anomaly-detector — GPU-accelerated anomaly detection
- timeseries-forecasting-ml — anomaly detection in time series
- ml-pipeline-design — deploying detection models
