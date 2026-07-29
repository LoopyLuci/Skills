---
name: physics-informed-neural-networks
description: "Use when building physics-informed neural networks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PINNs, physics-informed, PDE, scientific-ML, neural-operator, simulation]
    related_skills: [custom-training-loops, custom-loss-activation-functions, transformer-architectures, timeseries-foundation-models]
---

# Physics-Informed Neural Networks

Building physics-informed neural networks (PINNs) — from PDE residual loss through neural operators, Fourier features, and scientific ML applications.

## When to Use

- Solving PDEs with neural networks
- Incorporating physical laws into ML models
- Surrogate modeling for simulations
- Inverse problems (parameter discovery from data)
- Scientific ML applications

## PINN Implementation

```python
import torch
import torch.nn as nn

class PINN(nn.Module):
    """Physics-Informed Neural Network for solving PDEs."""
    def __init__(self, layers: List[int]):
        super().__init__()
        self.net = self._build(layers)
    
    def _build(self, layers):
        modules = []
        for i in range(len(layers)-1):
            modules.append(nn.Linear(layers[i], layers[i+1]))
            if i < len(layers)-2: modules.append(nn.Tanh())
        return nn.Sequential(*modules)
    
    def forward(self, x, t):
        return self.net(torch.cat([x, t], dim=1))

def pde_loss(model, x, t):
    """Loss: PDE residual (Burgers equation: u_t + u*u_x = ν*u_xx)."""
    x.requires_grad_(True); t.requires_grad_(True)
    u = model(x, t)
    
    # Compute gradients
    u_t = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]
    u_x = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
    u_xx = torch.autograd.grad(u_x, x, torch.ones_like(u_x), create_graph=True)[0]
    
    nu = 0.01  # Viscosity
    residual = u_t + u * u_x - nu * u_xx
    return torch.mean(residual**2)
```

## Verification Checklist

- [ ] PDE defined with initial/boundary conditions
- [ ] Network architecture deep enough for solution complexity
- [ ] Fourier features for high-frequency solutions
- [ ] Collocation points sampled (Latin Hypercube, adaptive)
- [ ] Loss terms weighted (PDE residual + BC + IC + data)
- [ ] Training converges (monitor each loss component)
- [ ] Solution validated against analytical or numerical reference
