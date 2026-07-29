---
name: adversarial-ml-robustness
description: "Use when implementing adversarial attacks and ML defenses."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [adversarial, robustness, attacks, defenses, security]
    related_skills: [agent-safety-alignment, differential-privacy-training, explainable-ai-xai-patterns]
---

# Adversarial ML — Attacks and Defenses

Implementing adversarial attacks to evaluate ML model robustness, and defenses to protect against them. Covers evasion, poisoning, extraction, and inference attacks.

## When to Use

- Testing model robustness before production deployment
- Building defenses against adversarial inputs
- Red-teaming ML systems for security vulnerabilities
- Researching new attack/defense methods
- Regulatory compliance for high-stakes ML (medical, finance, autonomous driving)

## Attack Taxonomy

```
Attacks
├── Evasion (perturb inputs at inference)
├── Poisoning (corrupt training data)
├── Extraction (steal model parameters)
└── Inference (leak training data membership)
    ├── Membership inference
    └── Attribute inference
```

## Evasion Attacks

### Fast Gradient Sign Method (FGSM)

```python
import torch
import torch.nn.functional as F

def fgsm_attack(model, x, y, epsilon=0.1):
    """Fast Gradient Sign Method: one-step adversarial attack."""
    x.requires_grad = True
    
    # Forward pass
    logits = model(x)
    loss = F.cross_entropy(logits, y)
    
    # Backward pass to get gradient
    model.zero_grad()
    loss.backward()
    
    # Create adversarial example
    x_adv = x + epsilon * x.grad.sign()
    x_adv = torch.clamp(x_adv, 0, 1)  # Keep in valid range
    
    return x_adv.detach()
```

### Projected Gradient Descent (PGD)

```python
def pgd_attack(model, x, y, epsilon=0.3, alpha=0.01, num_steps=40, random_start=True):
    """Projected Gradient Descent: iterative, stronger than FGSM."""
    x_adv = x.clone().detach()
    
    if random_start:
        x_adv = x_adv + torch.empty_like(x_adv).uniform_(-epsilon, epsilon)
    
    for _ in range(num_steps):
        x_adv.requires_grad = True
        
        logits = model(x_adv)
        loss = F.cross_entropy(logits, y)
        
        model.zero_grad()
        loss.backward()
        
        # Gradient ascent step
        with torch.no_grad():
            x_adv = x_adv + alpha * x_adv.grad.sign()
            
            # Project back to epsilon-ball around original x
            delta = torch.clamp(x_adv - x, -epsilon, epsilon)
            x_adv = torch.clamp(x + delta, 0, 1)
    
    return x_adv.detach()
```

### Carlini-Wagner (C&W) Attack

```python
def cw_attack(model, x, y, num_classes=10, confidence=0, lr=1e-2, max_iter=1000):
    """Carlini-Wagner L2 attack. Finds minimal perturbation."""
    x_adv = x.clone().detach().requires_grad_(True)
    optimizer = torch.optim.Adam([x_adv], lr=lr)
    
    # Convert labels to one-hot
    y_onehot = F.one_hot(y, num_classes).float()
    
    for i in range(max_iter):
        logits = model(x_adv)
        
        # CW loss: maximize logit of target class - max of others
        real = (logits * y_onehot).sum(dim=1)
        other = ((1 - y_onehot) * logits - (1 - y_onehot) * 1e9).max(dim=1)[0]
        loss = torch.max(real - other, -confidence + other - real).sum()
        
        # L2 regularization
        l2_loss = (x_adv - x).pow(2).sum()
        total_loss = loss + l2_loss
        
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
    
    return x_adv.detach()
```

## Poisoning Attacks

### Data Poisoning (Backdoor)

```python
def inject_backdoor(dataset, target_label=0, trigger_pattern="square", poison_ratio=0.1):
    """Inject backdoor triggers into training data."""
    poisoned_x, poisoned_y = [], []
    
    for i, (x, y) in enumerate(dataset):
        if random.random() < poison_ratio:
            # Apply trigger to input
            x_poisoned = apply_trigger(x, trigger_pattern)
            # Label flipping
            poisoned_x.append(x_poisoned)
            poisoned_y.append(target_label)
        else:
            poisoned_x.append(x)
            poisoned_y.append(y)
    
    return poisoned_x, poisoned_y

def apply_trigger(x, pattern="square"):
    """Add a trigger pattern to the image."""
    x_adv = x.clone()
    if pattern == "square":
        # White square in bottom-right corner
        x_adv[..., -5:, -5:] = 1.0
    elif pattern == "pixel":
        x_adv[..., 0, 0] = 1.0
    return x_adv
```

### Gradient Matching Poisoning

```python
def gradient_matching_poison(clean_model, target_example, target_label, 
                             n_poison=100, steps=100, lr=0.1):
    """Craft poisons that maximize loss on target example."""
    # Initialize poison data
    poison_data = torch.randn(n_poison, *clean_model.input_shape)
    poison_labels = torch.zeros(n_poison, dtype=torch.long)
    poison_data.requires_grad_(True)
    
    optimizer = torch.optim.SGD([poison_data], lr=lr)
    
    for _ in range(steps):
        # Train on poison data
        logits = clean_model(poison_data)
        train_loss = F.cross_entropy(logits, poison_labels)
        
        # Maximize loss on target
        target_logits = clean_model(target_example)
        target_loss = F.cross_entropy(target_logits, target_label)
        
        # Combined: minimize train loss, maximize target loss
        total_loss = train_loss - target_loss
        
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
        poison_data.data = torch.clamp(poison_data.data, 0, 1)
    
    return poison_data.detach(), poison_labels
```

## Defenses

### Adversarial Training

```python
def adversarial_training(model, train_loader, epochs=50, epsilon=0.1, alpha=0.01):
    """Train on adversarial examples to build robustness."""
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    
    for epoch in range(epochs):
        total_loss = 0
        for x, y in train_loader:
            # Generate adversarial examples
            x_adv = pgd_attack(model, x, y, epsilon=epsilon, alpha=alpha, num_steps=7)
            
            # Train on both clean and adversarial examples
            logits_clean = model(x)
            logits_adv = model(x_adv)
            
            loss_clean = F.cross_entropy(logits_clean, y)
            loss_adv = F.cross_entropy(logits_adv, y)
            loss = (loss_clean + loss_adv) / 2
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch}, Loss: {total_loss/len(train_loader):.4f}")
```

### Gradient Masking (Not Recommended)

```python
# Note: gradient masking gives false sense of security
# Attacks often work around it via transfer or black-box methods
class GradientMaskedModel(nn.Module):
    """Shattered gradients defense (limited effectiveness)."""
    def forward(self, x):
        x = self.features(x)
        # Clip gradients during backward pass
        x.register_hook(lambda grad: torch.where(grad.abs() > 0.1, 
                                                   torch.zeros_like(grad), grad))
        return self.classifier(x)
```

### Certified Defenses (Randomized Smoothing)

```python
class RandomizedSmoothing:
    """Certified robustness via input noise.
    Provides provable radius within which prediction is robust."""
    
    def __init__(self, base_classifier, sigma=0.25, n_samples=100):
        self.base = base_classifier
        self.sigma = sigma
        self.n = n_samples
    
    def predict(self, x):
        """Smooth prediction: add Gaussian noise and aggregate."""
        counts = torch.zeros(x.shape[0], self.base.num_classes)
        
        for _ in range(self.n):
            noise = torch.randn_like(x) * self.sigma
            logits = self.base(x + noise)
            preds = logits.argmax(dim=1)
            for i in range(x.shape[0]):
                counts[i, preds[i]] += 1
        
        return counts.argmax(dim=1)
    
    def certify_radius(self, x, n0=100, n=10000, alpha=0.001):
        """Compute certified L2 radius."""
        # Two-step: select top class with n0 samples, then certify with n samples
        pass
```

## Evaluation

```python
def evaluate_robustness(model, test_loader, attack_fn=pgd_attack, **attack_kwargs):
    """Measure robust accuracy against an attack."""
    clean_correct = 0
    robust_correct = 0
    total = 0
    
    for x, y in test_loader:
        x_adv = attack_fn(model, x, y, **attack_kwargs)
        
        clean_pred = model(x).argmax(dim=1)
        robust_pred = model(x_adv).argmax(dim=1)
        
        clean_correct += (clean_pred == y).sum().item()
        robust_correct += (robust_pred == y).sum().item()
        total += y.shape[0]
    
    print(f"Clean accuracy: {clean_correct/total:.2%}")
    print(f"Robust accuracy: {robust_correct/total:.2%}")
    return clean_correct/total, robust_correct/total
```

## Common Pitfalls

1. **Gradient masking** — defending against one attack doesn't mean robustness; always evaluate with adaptive attacks
2. **Evaluation on same attack type** — adversarial training against PGD doesn't generalize to C&W attacks
3. **Perceptual vs. adversarial distance** — a perturbation that's small in L2 norm can be visually obvious; use LPIPS for vision
4. **Adaptive attacks** — white-box attacks that know your defense will often break it; test with transfer attacks
5. **False sense of security** — no defense is 100% effective; report both attack success rate and clean accuracy drop

## Verification Checklist

- [ ] Attack reproduces published results on standard model
- [ ] Adversarial examples are visually similar to originals (or within specified perturbation budget)
- [ ] Defense degrades clean accuracy by acceptable amount
- [ ] Robust accuracy reported against multiple attack types (FGSM, PGD, C&W)
- [ ] Adaptive attack considered (defense-aware attacker)
- [ ] Certified robustness radius computed (if using certified defense)

## See Also

- agent-safety-alignment — broader AI safety considerations
- differential-privacy-training — privacy-preserving ML
- explainable-ai-xai-patterns — understanding model decisions
