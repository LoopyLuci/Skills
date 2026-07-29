---
name: online-learning-systems
description: "Use when building models that learn incrementally."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [online-learning, incremental-learning, streaming-ml, river, vowpal-wabbit]
    related_skills: [continual-lifelong-learning, active-learning-strategies, data-pipeline-streaming, model-monitoring-drift]
---

# Online Learning Systems

Building ML models that learn incrementally from streaming data — from online gradient descent through bandit algorithms, streaming features, and production deployment.

## When to Use

- Data arrives as a stream (real-time, high volume)
- Models must adapt to changing distributions quickly
- Training on all historical data is too expensive
- Building bandit systems for real-time optimization

## Online Learning Algorithms

```python
class OnlineSGD:
    """Online Stochastic Gradient Descent."""
    def __init__(self, n_features: int, lr: float = 0.01):
        self.weights = np.zeros(n_features)
        self.lr = lr
    
    def partial_fit(self, x: np.array, y: float):
        """Update model with one sample at a time."""
        pred = np.dot(self.weights, x)
        self.weights += self.lr * (y - pred) * x
    
    def predict(self, x: np.array) -> float:
        return np.dot(self.weights, x)
```

## Common Pitfalls

1. **Concept drift** — online learning adapts slowly to sudden shifts
2. **Catastrophic interference** — new data can overwrite useful old patterns
3. **No baseline** — compare with periodically retrained batch model
4. **Cold start** — warm-start with mini-batch from historical data

## Verification Checklist

- [ ] Algorithm supports incremental updates (partial_fit)
- [ ] Feature computation consistent in training and serving
- [ ] Concept drift detection integrated
- [ ] Model checkpointing for recovery
