---
name: federated-learning-cross-device
description: "Use when implementing cross-device federated learning."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [federated-learning, cross-device, privacy, FL, Flower, TFF, aggregation]
    related_skills: [edge-ai-tinyml, differential-privacy-training, on-device-ml-optimization, data-synthesis-generation]
---

# Cross-Device Federated Learning

Implementing federated learning across devices — from FedAvg and secure aggregation through Flower/TensorFlow Federated setup, differential privacy, and production deployment.

## When to Use

- Training ML models on user data without centralizing it
- Privacy-preserving ML across mobile or edge devices
- Improving models from on-device data
- Compliance with data residency requirements

## Federated Learning Framework

```python
import flwr as fl

class FederatedClient(fl.client.NumPyClient):
    """Flower federated learning client."""
    def __init__(self, model, train_data, val_data):
        self.model = model
        self.x_train, self.y_train = train_data
        self.x_val, self.y_val = val_data
    
    def get_parameters(self, config):
        return self.model.get_weights()
    
    def fit(self, parameters, config):
        self.model.set_weights(parameters)
        self.model.fit(self.x_train, self.y_train, epochs=1, batch_size=32)
        return self.model.get_weights(), len(self.x_train), {}
    
    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, accuracy = self.model.evaluate(self.x_val, self.y_val)
        return loss, len(self.x_val), {'accuracy': accuracy}

# Server-side aggregation strategy
strategy = fl.server.strategy.FedAvg(
    min_fit_clients=10, min_available_clients=50,
    fraction_fit=0.2, fraction_evaluate=0.1,
)
```

## Verification Checklist

- [ ] FL framework chosen (Flower, TFF, PySyft, NVIDIA FLARE)
- [ ] Client selection strategy defined (fraction_fit, min_clients)
- [ ] Secure aggregation protocol (if privacy required)
- [ ] Differential privacy added to client updates
- [ ] Communication efficiency (compression, fewer rounds)
- [ ] Heterogeneity handled (different device capabilities, data distributions)
- [ ] Privacy guarantees documented (epsilon, delta)
