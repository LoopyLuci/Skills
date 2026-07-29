---
name: semi-supervised-learning
description: "Use when applying semi-supervised learning techniques."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [semi-supervised, pseudo-labeling, consistency-regularization, self-training, label-propagation]
    related_skills: [self-supervised-learning, active-learning-strategies, data-augmentation-techniques, transfer-learning-patterns]
---

# Semi-Supervised Learning

Applying semi-supervised learning techniques to leverage unlabeled data — from self-training and pseudo-labeling through consistency regularization and hybrid approaches.

## When to Use

- Labeled data is scarce but unlabeled data is abundant
- Reducing labeling costs while maintaining model quality
- Improving model robustness with unlabeled examples
- Cold-start scenarios with limited initial labels
- Building models where labeling requires expert time

## Key Methods

```python
SEMI_SUPERVISED_METHODS = {
    'self_training': 'Train on labeled, predict unlabeled, add high-confidence predictions as pseudo-labels, retrain',
    'consistency_regularization': 'Apply different augmentations to same input, penalize prediction differences',
    'mixmatch': 'Mix labeled and unlabeled data, apply MixUp between them',
    'fixmatch': 'Generate pseudo-labels from weakly-augmented data, enforce on strongly-augmented version',
    'label_propagation': 'Propagate labels through similarity graph of labeled to unlabeled examples',
}

class FixMatch:
    """FixMatch: simplified consistency regularization."""
    def __init__(self, model, threshold=0.95, weight_ul=1.0):
        self.model = model
        self.threshold = threshold
        self.weight_ul = weight_ul
    
    def train_step(self, labeled_x, labeled_y, unlabeled_x, weak_aug, strong_aug):
        # Supervised loss on labeled
        logits_labeled = self.model(labeled_x)
        loss_s = F.cross_entropy(logits_labeled, labeled_y)
        
        # Pseudo-label unlabeled data using weakly-augmented version
        with torch.no_grad():
            weak_out = self.model(weak_aug(unlabeled_x))
            probs = F.softmax(weak_out, dim=1)
            max_probs, pseudo_labels = probs.max(dim=1)
            mask = max_probs >= self.threshold
        
        # Apply on strongly-augmented version
        strong_out = self.model(strong_aug(unlabeled_x))
        loss_u = F.cross_entropy(strong_out, pseudo_labels, reduction='none') * mask
        loss_u = loss_u.mean()
        
        return loss_s + self.weight_ul * loss_u
```

## Common Pitfalls

1. **Noisy pseudo-labels** — low-quality pseudo-labels hurt more than help; use confidence threshold
2. **Distribution mismatch** — unlabeled data from different distribution than labeled; filter OOD
3. **Confirmation bias** — model reinforces its own mistakes in pseudo-labels; use augmentations
4. **Class imbalance** — pseudo-labels skew toward majority class; use class-balanced sampling
5. **Too little labeled data** — with <5 labeled examples per class, even SSL struggles

## Verification Checklist

- [ ] Labeled and unlabeled data from same distribution
- [ ] Pseudo-label confidence threshold tuned (eg 0.95)
- [ ] Strong vs weak augmentation strategies defined
- [ ] SSL method matches data size (FixMatch for <100 labels, MixMatch for more)
- [ ] Ablation: labeled-only baseline vs SSL improvement measured
