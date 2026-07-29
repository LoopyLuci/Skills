---
name: custom-optimizer-design
description: "Use when implementing custom optimization algorithms for ML."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [optimization, optimizers, training, deep-learning, pytorch]
    related_skills: [custom-training-loops, custom-loss-activation-functions, model-compression-techniques]
---

# Custom Optimizer Design

Designing, implementing, and debugging custom optimization algorithms for neural network training — from classical momentum variants to modern adaptive methods and second-order approximations.

## When to Use

- Standard optimizers (Adam, SGD) don't converge for your architecture/loss
- You need optimizer-level regularization beyond weight decay
- Training is unstable (loss spikes, gradient explosion)
- You're researching new optimization algorithms
- Training at extreme batch sizes or learning rates

## Optimizer Architecture

### Base Optimizer Pattern (PyTorch)

```python
import torch
from torch.optim import Optimizer

class CustomOptimizer(Optimizer):
    """Template for custom PyTorch optimizers."""
    def __init__(self, params, lr=1e-3, **kwargs):
        defaults = dict(lr=lr, **kwargs)
        super().__init__(params, defaults)
    
    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        
        for group in self.param_groups:
            params_with_grad = [p for p in group['params'] if p.grad is not None]
            
            for p in params_with_grad:
                state = self.state[p]
                grad = p.grad
                
                # Initialize state
                if len(state) == 0:
                    self._init_state(p, state)
                
                # Apply update
                self._update_step(p, grad, state, group)
        
        return loss
    
    def _init_state(self, p, state):
        """Initialize optimizer state for parameter p."""
        pass
    
    def _update_step(self, p, grad, state, group):
        """Core update logic. Override this."""
        p.add_(grad, alpha=-group['lr'])
```

### Standard Optimizers (Reference)

```python
class SGDMomentum(CustomOptimizer):
    """SGD with Nesterov momentum. Reference implementation."""
    def _init_state(self, p, state):
        state['momentum_buffer'] = torch.zeros_like(p)
    
    def _update_step(self, p, grad, state, group):
        mu = group.get('momentum', 0.9)
        buf = state['momentum_buffer']
        buf.mul_(mu).add_(grad)
        if group.get('nesterov', False):
            grad = grad + mu * buf
        else:
            grad = buf
        p.add_(grad, alpha=-group['lr'])
```

```python
class AdamReference(CustomOptimizer):
    """Adam optimizer. Reference for comparison."""
    def _init_state(self, p, state):
        state['step'] = 0
        state['exp_avg'] = torch.zeros_like(p)
        state['exp_avg_sq'] = torch.zeros_like(p)
    
    def _update_step(self, p, grad, state, group):
        beta1, beta2 = group.get('betas', (0.9, 0.999))
        eps = group.get('eps', 1e-8)
        
        state['step'] += 1
        state['exp_avg'].mul_(beta1).add_(grad, alpha=1-beta1)
        state['exp_avg_sq'].mul_(beta2).add_(grad**2, alpha=1-beta2)
        
        bias_corr1 = 1 - beta1 ** state['step']
        bias_corr2 = 1 - beta2 ** state['step']
        
        step_size = group['lr'] / bias_corr1
        denom = (state['exp_avg_sq'] / bias_corr2).sqrt_().add_(eps)
        
        p.addcdiv_(state['exp_avg'], denom, value=-step_size)
```

## Custom Optimizer Patterns

### Pattern 1: Gradient Centralization

```python
class GCAdam(AdamReference):
    """Adam with Gradient Centralization.
    Subtracts mean from gradients for better training stability."""
    def _update_step(self, p, grad, state, group):
        # Centralize gradient
        if grad.dim() > 1:
            grad = grad - grad.mean(dim=tuple(range(1, grad.dim())), keepdim=True)
        super()._update_step(p, grad, state, group)
```

### Pattern 2: Lookahead

```python
class LookaheadWrapper:
    """Wraps any optimizer with Lookahead mechanism.
    Maintains slow weights that track fast weights' trajectory."""
    def __init__(self, optimizer, k=5, alpha=0.5):
        self.optimizer = optimizer
        self.k = k
        self.alpha = alpha
        self.slow_params = [p.clone().detach() for p in optimizer.param_groups[0]['params']]
        self.step_count = 0
    
    def step(self, closure=None):
        loss = self.optimizer.step(closure)
        self.step_count += 1
        
        if self.step_count % self.k == 0:
            # Update slow weights: slow = slow + alpha * (fast - slow)
            with torch.no_grad():
                for slow_p, fast_p in zip(self.slow_params, 
                    self.optimizer.param_groups[0]['params']):
                    slow_p.add_(fast_p - slow_p, alpha=self.alpha)
                    fast_p.copy_(slow_p)  # Reset fast to slow
        
        return loss
    
    def zero_grad(self):
        self.optimizer.zero_grad()
```

### Pattern 3: RAdam (Rectified Adam)

```python
class RAdam(CustomOptimizer):
    """Adam with dynamic rectification for warmup.
    Automatically adjusts adaptive LR based on variance."""
    def _init_state(self, p, state):
        state['step'] = 0
        state['exp_avg'] = torch.zeros_like(p)
        state['exp_avg_sq'] = torch.zeros_like(p)
    
    def _update_step(self, p, grad, state, group):
        beta1, beta2 = group.get('betas', (0.9, 0.999))
        eps = group.get('eps', 1e-8)
        
        state['step'] += 1
        state['exp_avg'].mul_(beta1).add_(grad, alpha=1-beta1)
        state['exp_avg_sq'].mul_(beta2).add_(grad**2, alpha=1-beta2)
        
        bias_corr1 = 1 - beta1 ** state['step']
        bias_corr2 = 1 - beta2 ** state['step']
        
        rho_inf = 2 / (1 - beta2) - 1
        rho_t = rho_inf - 2 * state['step'] * beta2**state['step'] / (1 - beta2**state['step'])
        
        if rho_t > 5:  # Variance is tractable
            r = ((rho_t - 4) * (rho_t - 2) * rho_inf) / ((rho_inf - 4) * (rho_inf - 2) * rho_t)
            lr = group['lr'] * r / bias_corr1
            denom = (state['exp_avg_sq'] / bias_corr2).sqrt().add_(eps)
            p.addcdiv_(state['exp_avg'], denom, value=-lr)
        else:
            # Fall back to SGD
            p.add_(state['exp_avg'] / bias_corr1, alpha=-group['lr'])
```

### Pattern 4: LARS (Layer-wise Adaptive Rate Scaling)

```python
class LARS(CustomOptimizer):
    """Layer-wise Adaptive Rate Scaling.
    Good for large-batch training (batch size > 1024)."""
    def __init__(self, params, lr=1e-3, momentum=0.9, trust_coef=0.001):
        defaults = dict(lr=lr, momentum=momentum, trust_coef=trust_coef)
        super().__init__(params, defaults)
    
    def _init_state(self, p, state):
        state['momentum_buffer'] = torch.zeros_like(p)
    
    def _update_step(self, p, grad, state, group):
        mu = group['momentum']
        tc = group['trust_coef']
        
        # LARS scaling: local_lr = lr * ||w|| / (||grad|| + weight_decay*||w|| + eps)
        weight_norm = p.data.norm().add_(1e-8)
        grad_norm = grad.norm().add_(1e-8)
        local_lr = group['lr'] * tc * (weight_norm / grad_norm)
        
        buf = state['momentum_buffer']
        buf.mul_(mu).add_(grad, alpha=local_lr)
        p.add_(buf, alpha=-1)
```

### Pattern 5: Sharpness-Aware Minimization (SAM)

```python
class SAM:
    """SAM optimizer: minimizes loss sharpness for better generalization.
    Wraps another optimizer. Two forward-backward passes per step."""
    def __init__(self, base_optimizer, model, rho=0.05):
        self.base_optimizer = base_optimizer
        self.model = model
        self.rho = rho
    
    def first_step(self, zero_grad=False):
        """First forward-backward pass to compute gradient perturbation."""
        grads = []
        for p in self.model.parameters():
            if p.grad is None:
                continue
            grad_norm = p.grad.norm()
            if grad_norm > 0:
                p.data.add_(p.grad * self.rho / grad_norm)
            grads.append(p.grad.clone())
        return grads
    
    def second_step(self, grads, zero_grad=False):
        """Second pass with original parameters."""
        for p, g in zip(self.model.parameters(), grads):
            if g is not None:
                p.grad.copy_(g)
        self.base_optimizer.step()
```

## Learning Rate Schedules as Optimizer Components

```python
class CosineWarmupSchedule:
    """Cosine LR with linear warmup. Can be integrated into optimizer."""
    def __init__(self, optimizer, warmup_steps=1000, total_steps=10000, min_lr=1e-6):
        self.optimizer = optimizer
        self.warmup = warmup_steps
        self.total = total_steps
        self.base_lr = optimizer.param_groups[0]['lr']
        self.min_lr = min_lr
        self.step_num = 0
    
    def step(self):
        self.step_num += 1
        if self.step_num < self.warmup:
            lr = self.base_lr * self.step_num / self.warmup
        else:
            progress = (self.step_num - self.warmup) / (self.total - self.warmup)
            lr = self.min_lr + 0.5 * (self.base_lr - self.min_lr) * (1 + math.cos(math.pi * progress))
        
        for group in self.optimizer.param_groups:
            group['lr'] = lr
```

## Optimizer Comparison

| Optimizer | Best For | Memory per Param | Key Advantage |
|-----------|---------|-----------------|---------------|
| SGD + Momentum | Vision, well-tuned | 1 buffer | Simple, generalizes well |
| Adam | NLP, Transformers | 2 buffers | Fast convergence |
| AdamW | Transformers | 2 buffers | Proper decoupled decay |
| RAdam | Early training | 2 buffers | No warmup needed |
| LARS | Large-batch | 1 buffer | Scales to 64K batch |
| LAMB | Large-batch Transformers | 2 buffers | Combines LARS + Adam |
| SAM | Generalization | 2x compute | Flatter minima |
| Lookahead | Any base optimizer | 1 buffer | Stabilizes training |
| AdaBelief | Noisy gradients | 2 buffers | Belief in observed gradient |

## Common Pitfalls

1. **Weight decay interaction** — standard Adam L2 regularization != AdamW weight decay; use decoupled weight decay
2. **Learning rate range** — adaptive methods need different LR than SGD; test range [1e-5, 1e-2]
3. **State memory** — custom optimizers with large state vectors double memory usage
4. **NaN from denom** — adaptive methods divide by sqrt(v); always add epsilon (1e-8)
5. **Pytorch optimizer API changes** — `state_dict`, `add_param_group` must work for checkpoint compatibility
6. **Comparing with tuned baselines** — a custom optimizer that beats poorly-tuned Adam isn't impressive; tune baselines too

## Verification Checklist

- [ ] Converges on a small synthetic task (e.g., fitting random labels)
- [ ] Converges on real task within expected steps
- [ ] GPU memory usage profiled (state buffers accounted for)
- [ ] Batchnorm running stats correctly updated
- [ ] Checkpoint save/load preserves optimizer state
- [ ] Gradient clipping doesn't break optimizer assumptions
- [ ] Mixed precision (amp) compatibility verified
- [ ] Distributed training (DDP) gradient sync verified

## See Also

- custom-training-loops — integrating custom optimizers
- custom-loss-activation-functions — loss functions that affect gradient flow
- model-compression-techniques — optimizers for quantization-aware training
