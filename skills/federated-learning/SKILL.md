---
name: federated-learning
description: "Use when implementing federated learning systems."
category: mlops
tags: [federated-learning, privacy, distributed, flower]
---
# Federated Learning

Training ML models across decentralized data without sharing raw data.

## Core Workflow

```
Server: initialize model
    │
    ▼
Client 1 ───→ local data ──→ train ──→ send gradients ──┐
Client 2 ───→ local data ──→ train ──→ send gradients ──┤
Client 3 ───→ local data ──→ train ──→ send gradients ──┤
Client N ───→ local data ──→ train ──→ send gradients ──┤
                                                │
                                                ▼
                                    Server: aggregate (FedAvg)
                                    Server: update global model
                                                │
                                                ▼
                                        Repeat for next round
```

## FedAvg Implementation

```python
import torch
from collections import OrderedDict

def fed_avg(global_model, client_updates: list[OrderedDict],
            client_weights: list[float] = None):
    """Federated Averaging algorithm."""
    global_dict = global_model.state_dict()

    if client_weights is None:
        client_weights = [1.0 / len(client_updates)] * len(client_updates)

    # Weighted average of parameters
    averaged = OrderedDict()
    for key in global_dict.keys():
        averaged[key] = sum(
            w * update[key].float()
            for w, update in zip(client_weights, client_updates)
        )

    global_model.load_state_dict(averaged)
    return global_model
```

## Client Selection

```python
import random

def select_clients(all_clients: list, fraction: float = 0.1, strategy: str = "random"):
    """Select a subset of clients for each round."""
    n = max(1, int(len(all_clients) * fraction))

    if strategy == "random":
        return random.sample(all_clients, n)

    elif strategy == "stratified":
        # Ensure diverse selection (by data size, label distribution)
        weighted = sorted(all_clients, key=lambda c: c.data_size, reverse=True)
        return weighted[:n]

    elif strategy == "targeted":
        # Select clients with most useful data
        scores = [(c, c.compute_utility_score()) for c in all_clients]
        scores.sort(key=lambda x: -x[1])
        return [c for c, _ in scores[:n]]
```

## Differential Privacy

```python
class GaussianMechanism:
    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        self.epsilon = epsilon
        self.delta = delta
        self.sensitivity = 1.0  # for gradient norm clipping

    def add_noise(self, gradients: dict, clip_norm: float = 1.0) -> dict:
        """Add calibrated Gaussian noise to gradients."""
        # Clip gradients
        total_norm = torch.sqrt(sum(g.norm()**2 for g in gradients.values()))
        scale = clip_norm / max(total_norm, clip_norm)
        clipped = {k: v * scale for k, v in gradients.items()}

        # Add noise
        sigma = (self.sensitivity * np.sqrt(2 * np.log(1.25 / self.delta))
                 / self.epsilon)
        noisy = {
            k: v + torch.randn_like(v) * sigma
            for k, v in clipped.items()
        }
        return noisy
```

## Using Flower Framework

```python
import flwr as fl

# Define client
class FlowerClient(fl.client.NumPyClient):
    def __init__(self, model, trainloader, testloader):
        self.model = model
        self.trainloader = trainloader
        self.testloader = testloader

    def get_parameters(self, config):
        return [val.cpu().numpy() for val in self.model.state_dict().values()]

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        train_model(self.model, self.trainloader, epochs=config["local_epochs"])
        return self.get_parameters(config={}), len(self.trainloader.dataset), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, accuracy = evaluate_model(self.model, self.testloader)
        return loss, len(self.testloader.dataset), {"accuracy": accuracy}

fl.client.start_numpy_client(
    server_address="localhost:8080",
    client=FlowerClient(model, trainloader, testloader),
)
```

## Pitfalls

- Non-IID data across clients hurts convergence — use FedProx or SCAFFOLD
- Communication cost is the bottleneck — compress updates
- Stragglers (slow clients) block rounds — use asynchronous aggregation
- Differential privacy reduces accuracy — tune epsilon for your task
- Client drop-out is common — design for graceful degradation (minimum clients)
