---
name: custom-loss-activation-functions
description: "Use when designing custom loss functions and activations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [neural-networks, loss-functions, activations, pytorch, deep-learning]
    related_skills: [custom-neural-architecture-design, custom-training-loops, neural-network-fundamentals, custom-optimizer-design]
---

# Custom Loss and Activation Functions

Designing and implementing custom loss functions and activation functions for neural networks — from mathematical formulation to PyTorch implementation, with guidance on when custom functions beat standard ones.

## When to Use

- Standard losses (MSE, cross-entropy) don't capture what matters for your task
- Your output distribution is non-standard (heavy-tailed, bounded, multi-modal)
- You need to enforce domain-specific constraints during training
- Standard activations cause dead neurons, saturation, or training instability
- You're experimenting with biologically-plausible or novel activation forms

## Custom Loss Functions

### Base Pattern

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class CustomLoss(nn.Module):
    """Template for all custom loss functions."""
    def __init__(self, reduction='mean'):
        super().__init__()
        self.reduction = reduction
    
    def forward(self, pred, target):
        # Compute per-sample loss
        loss = self._compute_loss(pred, target)
        
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        return loss  # 'none'
    
    def _compute_loss(self, pred, target):
        raise NotImplementedError
```

### Asymmetric Loss

Penalize over- and under-predictions differently:

```python
class AsymmetricMSELoss(nn.Module):
    """Different penalty for over vs under prediction."""
    def __init__(self, over_penalty=1.0, under_penalty=2.0):
        super().__init__()
        self.over = over_penalty
        self.under = under_penalty
    
    def forward(self, pred, target):
        error = pred - target
        weights = torch.where(error > 0, self.over, self.under)
        return (weights * error ** 2).mean()
```

### Focal Loss

Focus training on hard-to-classify examples:

```python
class FocalLoss(nn.Module):
    """Reduces loss for well-classified examples, focuses on hard ones.
    gamma=0 → CrossEntropy, gamma>0 → focuses on hard examples."""
    def __init__(self, gamma=2.0, alpha=0.25):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha
    
    def forward(self, pred, target):
        ce_loss = F.cross_entropy(pred, target, reduction='none')
        pt = torch.exp(-ce_loss)  # Predicted probability for correct class
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        return focal_loss.mean()
```

### Uncertainty-Weighted Multi-Task Loss

```python
class UncertaintyWeightedLoss(nn.Module):
    """Learnable task weighting based on homoscedastic uncertainty."""
    def __init__(self, num_tasks):
        super().__init__()
        self.log_vars = nn.Parameter(torch.zeros(num_tasks))
    
    def forward(self, losses):
        """losses: list of per-task loss values (scalar tensors)."""
        total_loss = 0
        for i, loss in enumerate(losses):
            precision = torch.exp(-self.log_vars[i])
            total_loss += precision * loss + self.log_vars[i] / 2
        return total_loss
```

### Dice Loss (Segmentation)

```python
class DiceLoss(nn.Module):
    """For imbalanced segmentation. Measures overlap."""
    def __init__(self, smooth=1e-6):
        super().__init__()
        self.smooth = smooth
    
    def forward(self, pred, target):
        pred = torch.softmax(pred, dim=1)
        target_one_hot = F.one_hot(target, num_classes=pred.shape[1]).permute(0, 3, 1, 2).float()
        
        intersection = (pred * target_one_hot).sum(dim=(2, 3))
        union = pred.sum(dim=(2, 3)) + target_one_hot.sum(dim=(2, 3))
        dice = (2 * intersection + self.smooth) / (union + self.smooth)
        return 1 - dice.mean()
```

### Contrastive Loss

```python
class ContrastiveLoss(nn.Module):
    """Pull positive pairs together, push negative pairs apart."""
    def __init__(self, margin=1.0):
        super().__init__()
        self.margin = margin
    
    def forward(self, embedding1, embedding2, label):
        # label=1: similar pair, label=0: dissimilar pair
        distance = F.pairwise_distance(embedding1, embedding2)
        loss = label * distance**2 + (1 - label) * F.relu(self.margin - distance)**2
        return loss.mean()
```

### Custom Ranking Loss (NDCG-Approx)

```python
class ApproxNDCGLoss(nn.Module):
    """Approximate NDCG as a differentiable loss for ranking."""
    def __init__(self, temperature=0.1):
        super().__init__()
        self.tau = temperature
    
    def forward(self, pred_scores, true_relevance):
        # Approximate ranking with soft sort
        pred_sorted, indices = pred_scores.sort(descending=True)
        rel_sorted = true_relevance.gather(1, indices)
        
        # DCG
        dcg = (rel_sorted / torch.log2(torch.arange(2, pred_scores.shape[1]+2, device=pred_scores.device).float())).sum()
        
        # IDCG
        ideal_rel, _ = true_relevance.sort(descending=True)
        idcg = (ideal_rel / torch.log2(torch.arange(2, pred_scores.shape[1]+2, device=pred_scores.device).float())).sum()
        
        return 1 - dcg / (idcg + 1e-10)
```

## Custom Activation Functions

### Base Pattern

```python
class CustomActivation(nn.Module):
    """Template for custom activation functions.
    Must provide forward and optionally backward for custom gradient."""
    def __init__(self):
        super().__init__()
    
    def forward(self, x):
        raise NotImplementedError
```

### GELU (Gaussian Error Linear Unit)

```python
class GELU(nn.Module):
    """Smooth version of ReLU. Used in GPT, BERT, ViT.
    Self-contained implementation (don't import from PyTorch)."""
    def forward(self, x):
        return 0.5 * x * (1 + torch.tanh(
            torch.sqrt(torch.tensor(2.0 / torch.pi)) * (x + 0.044715 * x**3)
        ))
```

### Swish / SiLU

```python
class Swish(nn.Module):
    """Self-gated activation. x * sigmoid(x).
    Often outperforms ReLU in deep models."""
    def forward(self, x):
        return x * torch.sigmoid(x)
```

### Parametric Activation

```python
class PReLU(nn.Module):
    """Parametric ReLU with learnable negative slope."""
    def __init__(self, num_parameters=1):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(num_parameters) * 0.25)
    
    def forward(self, x):
        return torch.where(x >= 0, x, self.weight * x)
```

### Adaptive Activation

```python
class AdaptiveActivation(nn.Module):
    """Learnable combination of multiple activations.
    x → w1*relu(x) + w2*gelu(x) + w3*sigmoid(x)"""
    def __init__(self, num_activations=3):
        super().__init__()
        self.weights = nn.Parameter(torch.ones(num_activations) / num_activations)
        self.activations = [F.relu, F.gelu, torch.sigmoid]
    
    def forward(self, x):
        weights = F.softmax(self.weights, dim=0)
        result = 0
        for w, act in zip(weights, self.activations):
            result += w * act(x)
        return result
```

### Rational Activation

```python
class RationalActivation(nn.Module):
    """Rational function activation: P(x)/Q(x) where P, Q are polynomials.
    More expressive than fixed activations."""
    def __init__(self, degree=3):
        super().__init__()
        self.P = nn.Parameter(torch.randn(degree + 1))
        self.Q = nn.Parameter(torch.randn(degree))
    
    def forward(self, x):
        # P(x) = a0 + a1*x + a2*x^2 + ...
        P_x = sum(c * x**i for i, c in enumerate(self.P))
        # Q(x) = 1 + b0*x + b1*x^2 + ...
        Q_x = 1 + sum(c * x**(i+1) for i, c in enumerate(self.Q))
        return P_x / Q_x
```

### Periodic Activation (NeRF-style)

```python
class PeriodicActivation(nn.Module):
    """sin(omega*x) for coordinate-based MLPs.
    Used in NeRF and implicit neural representations."""
    def __init__(self, omega=30.0, trainable=False):
        super().__init__()
        if trainable:
            self.omega = nn.Parameter(torch.tensor(omega))
        else:
            self.omega = omega
    
    def forward(self, x):
        return torch.sin(self.omega * x)
```

## Design Patterns

### Gradient-Smoothing Activation

For training stability with custom losses:

```python
class SmoothReLU(nn.Module):
    """ReLU with smooth gradient transition near 0.
    Reduces dead neuron problem while keeping sparsity."""
    def __init__(self, threshold=0.1):
        super().__init__()
        self.th = threshold
    
    def forward(self, x):
        return torch.where(
            x > self.th, x,
            torch.where(x < -self.th, 0.01 * x,
                        (x + self.th)**2 / (4 * self.th))
        )
```

### Bounded Activation for Regression

```python
class BoundedScaledTanh(nn.Module):
    """Output bounded to [min, max] for regression."""
    def __init__(self, min_val=0.0, max_val=1.0):
        super().__init__()
        self.min = min_val
        self.range = max_val - min_val
    
    def forward(self, x):
        return self.min + self.range * 0.5 * (torch.tanh(x) + 1)
```

## Loss-Activation Compatibility

| Loss | Recommended Final Activation | Notes |
|------|----------------------------|-------|
| Cross-Entropy | Softmax | Standard classification |
| BCE | Sigmoid | Multi-label classification |
| MSE | Identity (Linear) | Standard regression |
| Dice | Softmax | Segmentation |
| Contrastive | L2-normalized embedding | Normalize before loss |
| CTC | LogSoftmax | Sequence alignment |
| NLL | LogSoftmax | Requires log probabilities |
| Custom bounded loss | BoundedScaledTanh | Enforce output range |
| Ranking (pairwise) | Identity | Use score differences |

## Common Pitfalls

1. **Numerical instability** — log(0), division by zero, or exp overflow; add small epsilon (1e-8)
2. **Gradient starvation** — activation saturates (tanh at extremes) killing gradients; use gradient clipping
3. **Loss scale mismatch** — custom loss values 10x larger than standard; normalize output range
4. **NaN explosion** — custom functions with unbounded growth (rational without denom guard); add checks
5. **Dead neurons from custom activations** — activations with zero gradient for negative inputs; use leaky variants
6. **Incompatible gradient flow** — custom activations blocking gradient (hard threshold); use soft relaxation

## Verification Checklist

- [ ] Loss function numerically stable (no log/exp of extreme values)
- [ ] Loss on random predictions produces expected baseline value
- [ ] Gradient flows through custom activation (check grad norm)
- [ ] No dead neurons after 100 steps (activation statistics histogram)
- [ ] Custom loss equals standard loss on standard task (regression test)
- [ ] Training converges (loss decreases steadily)
- [ ] Custom function differentiable (no explicit .detach() blocking gradient)
- [ ] Device placement correct (tensors on same device as model)

## See Also

- custom-neural-architecture-design — designing architectures that use custom functions
- custom-training-loops — training with custom losses
- custom-optimizer-design — custom optimizers for unusual gradients
- neural-network-fundamentals — foundational concepts
