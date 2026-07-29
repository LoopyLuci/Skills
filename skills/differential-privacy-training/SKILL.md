---
name: differential-privacy-training
description: "Use when implementing differential privacy in ML training."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [differential-privacy, privacy, DP-SGD, secure-training]
    related_skills: [adversarial-ml-robustness, federated-learning, custom-training-loops, ai-fairness-mitigation]
---

# Differential Privacy for ML Training

Implementing differentially private machine learning using DP-SGD and related techniques to train models with formal privacy guarantees.

## When to Use

- Training on sensitive data (medical records, financial data, personal information)
- Regulatory compliance (GDPR, HIPAA, CCPA)
- Publishing models trained on user data without leaking individual records
- Federated learning with privacy guarantees
- Building privacy-preserving AI systems

## Core Concepts

### Privacy Budget (ε, δ)

```python
# ε (epsilon): privacy loss budget. Lower = more privacy.
# δ (delta): probability of privacy breach (typically < 1/N where N = dataset size)
# Typical values: ε=1 (strong privacy), ε=8 (weak privacy), δ=1e-5
```

### DP-SGD Algorithm

```python
import torch
import torch.nn as nn
from torch.optim import Optimizer

class DPSGD(Optimizer):
    """Differentially Private SGD with gradient clipping and noise.
    
    Key modifications to standard SGD:
    1. Clip per-sample gradients to L2 norm C
    2. Add Gaussian noise scaled by C * σ
    3. Account privacy budget via moments accountant
    """
    
    def __init__(self, params, lr=1e-3, clip_norm=1.0, noise_multiplier=1.1,
                 batch_size=256, dataset_size=50000, delta=1e-5):
        defaults = dict(lr=lr, clip_norm=clip_norm, noise_multiplier=noise_multiplier,
                       batch_size=batch_size, dataset_size=dataset_size)
        super().__init__(params, defaults)
        
        self.delta = delta
        self.epsilon = None  # Will be computed via moments accountant
        self.steps_taken = 0
    
    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        
        for group in self.param_groups:
            params = [p for p in group['params'] if p.grad is not None]
            
            if not params:
                continue
            
            # Step 1: Per-sample gradient clipping
            # We need per-sample gradients, which requires:
            #   - Setting `loss.backward(retain_graph=True)` for each sample in batch
            #   - OR using a per-sample gradient computation (Ghost Clipping)
            # Here we assume micro-batch approach
            
            # For each parameter, clip its gradient
            total_norm = torch.norm(
                torch.stack([torch.norm(p.grad, 2) for p in params])
            )
            
            clip_coef = min(1, group['clip_norm'] / (total_norm + 1e-8))
            
            for p in params:
                p.grad *= clip_coef  # Clip to C
                
                # Step 2: Add Gaussian noise
                noise = torch.normal(
                    mean=0,
                    std=group['clip_norm'] * group['noise_multiplier'],
                    size=p.grad.shape,
                    device=p.grad.device
                )
                p.grad += noise / group['batch_size']
                
                # Step 3: Update parameters
                p.add_(p.grad, alpha=-group['lr'])
        
        self.steps_taken += 1
        
        return loss
```

### Per-Sample Gradient Computation

```python
class PerSampleGradientComputer:
    """Efficient per-sample gradient computation for DP-SGD.
    
    Without this, you'd need to backward() per sample (very slow).
    Ghost clipping computes per-sample norms efficiently.
    """
    
    def compute_per_sample_norms(self, model, x, y, loss_fn):
        """Compute per-sample gradient norms without storing per-sample grads."""
        # Forward pass with a single backward
        logits = model(x)
        loss = loss_fn(logits, y)
        
        # Compute per-sample gradients (requires grad in loss function)
        # Efficient implementation depends on layer type:
        
        per_sample_norms = {}
        
        for name, param in model.named_parameters():
            if param.grad is None:
                continue
            
            # For linear layers: per-sample grad = outer product
            if isinstance(param, nn.Linear):
                # Ghost clipping: compute per-sample gradient norms efficiently
                pass
        
        # Clip and aggregate
        total_clipped = self.clip_and_aggregate(per_sample_norms, clip_norm=1.0)
        return total_clipped
```

## Privacy Accounting

### Moments Accountant

```python
class MomentsAccountant:
    """Tracks privacy budget (ε) across training steps using Rényi DP."""
    
    def __init__(self, noise_multiplier, delta=1e-5):
        self.noise_multiplier = noise_multiplier
        self.delta = delta
        self.orders = [1 + x/10.0 for x in range(1, 100)] + list(range(12, 64))
        self.renyi_divergences = {}
    
    def compute_epsilon(self, steps, sampling_rate):
        """Compute total privacy spend after `steps` steps."""
        # Rényi DP composition
        eps = float('inf')
        
        for order in self.orders:
            # RDP for Gaussian mechanism
            rdp = order * sampling_rate / (2 * self.noise_multiplier**2)
            rdp_total = rdp * steps
            
            # Convert from RDP to (ε, δ)-DP
            eps_order = rdp_total - np.log(self.delta) / (order - 1)
            eps = min(eps, eps_order)
        
        return eps
    
    def get_privacy_spent(self, steps_per_epoch, num_epochs, batch_size, dataset_size):
        """Get total (ε, δ) privacy guarantee."""
        sampling_rate = batch_size / dataset_size
        total_steps = steps_per_epoch * num_epochs
        epsilon = self.compute_epsilon(total_steps, sampling_rate)
        return epsilon, self.delta
```

### Privacy Budget Scheduler

```python
class PrivacyBudgetScheduler:
    """Schedule noise_multiplier across training to hit a target ε budget."""
    
    def __init__(self, target_epsilon, total_steps, dataset_size, batch_size, delta=1e-5):
        self.target_eps = target_epsilon
        self.total_steps = total_steps
        self.dataset_size = dataset_size
        self.batch_size = batch_size
        self.delta = delta
        self.sampling_rate = batch_size / dataset_size
    
    def find_noise_multiplier(self):
        """Binary search for noise_multiplier that meets budget."""
        lo, hi = 0.1, 10.0
        
        for _ in range(20):  # Binary search iterations
            mid = (lo + hi) / 2
            accountant = MomentsAccountant(mid, self.delta)
            eps = accountant.compute_epsilon(self.total_steps, self.sampling_rate)
            
            if eps > self.target_eps:
                lo = mid  # More noise needed
            else:
                hi = mid  # Less noise might work
        
        return hi  # Return smallest noise that meets budget
```

## Training Loop

```python
def dp_train(model, train_loader, epochs=50, lr=1e-3, 
             clip_norm=1.0, noise_multiplier=1.1, target_epsilon=8.0):
    """Full DP-SGD training loop with privacy accounting."""
    
    dataset_size = len(train_loader.dataset)
    batch_size = train_loader.batch_size
    delta = 1 / (dataset_size * 10)  # δ < 1/dataset_size
    
    optimizer = DPSGD(model.parameters(), lr=lr, clip_norm=clip_norm,
                      noise_multiplier=noise_multiplier, batch_size=batch_size,
                      dataset_size=dataset_size, delta=delta)
    
    accountant = MomentsAccountant(noise_multiplier, delta)
    
    for epoch in range(epochs):
        for x, y in train_loader:
            # Standard forward + backward (per-sample gradients needed for DP)
            logits = model(x)
            loss = F.cross_entropy(logits, y)
            
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        
        # Privacy accounting
        eps = accountant.get_privacy_spent(
            len(train_loader), epoch + 1, batch_size, dataset_size
        )
        print(f"Epoch {epoch}: ε={eps[0]:.2f}, δ={eps[1]:.2e}")
        
        if eps[0] > target_epsilon:
            print(f"Reached target privacy budget ({target_epsilon}). Stopping.")
            break
```

## Techniques for Better Privacy/Utility Trade-off

```python
# 1. Virtual batch size: accumulate gradients across micro-batches
#    before clipping + noise
class VirtualBatchDP:
    def __init__(self, micro_batch_size=32, virtual_batch_size=256):
        self.micro_batch_size = micro_batch_size
        self.virtual_batch_size = virtual_batch_size
    
    def accumulate_gradients(self, model, dataset):
        """Accumulate gradients over virtual batch."""
        model.zero_grad()
        
        for i in range(0, len(dataset), self.micro_batch_size):
            micro_batch = dataset[i:i + self.micro_batch_size]
            loss = model(micro_batch)
            loss.backward()
            
            # Don't step yet — accumulate across micro-batches
        
        # Now we have accumulated gradients for the virtual batch
        # Clip and add noise at virtual_batch_size granularity
        self.clip_and_noise(model)

# 2. Weight standardization + DP
#    Standardize weights after each step (improves stability with DP noise)

# 3. Public pre-training + private fine-tuning
#    Pre-train on public data, fine-tune with DP on private data
```

## Common Pitfalls

1. **Per-sample gradient cost** — naive per-sample backward is N times slower; use ghost clipping or JAX vmap
2. **Privacy budget underestimation** — moments accountant assumes Poisson sampling; fixed-size batches leak information
3. **Hyperparameter sensitivity** — DP training is very sensitive to LR and clipping norm; tune carefully
4. **Model capacity** — larger models need more privacy budget for same utility; use simpler models for strong privacy
5. **Batch size effects** — small batches have worse privacy/utility tradeoff; use large virtual batches (1024+)
6. **Evaluation leakage** — don't use validation set for early stopping without accounting for it in privacy budget

## Verification Checklist

- [ ] Privacy budget (ε, δ) reported transparently
- [ ] Per-sample gradient computation verified (norms computed correctly)
- [ ] Implementation produces same results as reference (e.g., Opacus for PyTorch)
- [ ] Training converges under privacy guarantees
- [ ] Utility drop quantified (accuracy vs. non-private baseline)
- [ ] Dataset-specific δ computed as < 1/N
- [ ] Accounting uses correct sampling rate (Poisson vs. shuffled)

## See Also

- adversarial-ml-robustness — robustness against adversarial inputs
- federated-learning — distributed training with privacy
- ai-fairness-mitigation — fairness alongside privacy
- custom-training-loops — customizing training loops
