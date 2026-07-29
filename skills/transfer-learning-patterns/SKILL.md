---
name: transfer-learning-patterns
description: "Use when applying transfer learning and domain adaptation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [transfer-learning, domain-adaptation, fine-tuning, pre-training]
    related_skills: [self-supervised-learning, llm-fine-tuning-lora, meta-learning-few-shot, ml-pipeline-design]
---

# Transfer Learning and Domain Adaptation

Transferring knowledge from pre-trained models to new tasks and domains — fine-tuning strategies, feature extraction, domain adaptation, and multi-task learning patterns.

## When to Use

- You have a small dataset but access to a large pre-trained model
- Your target domain differs from the source domain (distribution shift)
- Training from scratch is too expensive (compute, data, or time)
- You need to adapt a general model to a specific use case
- Building multi-task systems that share representations

## Transfer Learning Strategies

| Strategy | Data Labeled | Compute | Performance | When to Use |
|----------|-------------|---------|-------------|-------------|
| Feature Extraction | Few | Low | Good | Source/target similar |
| Full Fine-Tuning | Moderate | High | Best | Source/target somewhat different |
| Adapters/LoRA | Few | Medium | Near-best | Resource-constrained |
| Progressive Unfreezing | Few | Medium | Good | Uncertain similarity |
| Distillation | Moderate | Medium | Good | Model compression + transfer |

## Feature Extraction

```python
import torch
import torch.nn as nn
import torchvision.models as models

class FeatureExtractor:
    """Use pre-trained model as fixed feature extractor."""
    
    def __init__(self, model_name='resnet50', device='cuda'):
        # Load pre-trained model without classification head
        weights = 'IMAGENET1K_V2'
        model = getattr(models, model_name)(weights=weights)
        self.model = nn.Sequential(*list(model.children())[:-1])
        self.model.eval()
        self.model.to(device)
        self.device = device
    
    @torch.no_grad()
    def extract(self, images):
        """Extract features (no gradients)."""
        features = self.model(images)
        return features.squeeze(-1).squeeze(-1)  # Remove spatial dims


# Train a simple classifier on extracted features
def train_on_features(model, train_loader, num_classes, feature_dim=2048):
    classifier = nn.Linear(feature_dim, num_classes)
    optimizer = torch.optim.Adam(classifier.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()
    
    # Pre-compute all features (fast epoch training)
    all_features, all_labels = [], []
    with torch.no_grad():
        for images, labels in train_loader:
            features = model.extract(images.to(model.device))
            all_features.append(features.cpu())
            all_labels.append(labels)
    
    all_features = torch.cat(all_features)
    all_labels = torch.cat(all_labels)
    
    for epoch in range(100):
        preds = classifier(all_features)
        loss = criterion(preds, all_labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    return classifier
```

## Fine-Tuning

### Full Fine-Tuning

```python
def full_finetune(model, train_loader, val_loader, num_classes, epochs=10):
    """Fine-tune the entire model."""
    # Replace classification head
    in_features = model.classifier[0].in_features
    model.classifier = nn.Linear(in_features, num_classes)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)  # Lower LR
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, epochs)
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(epochs):
        model.train()
        for images, labels in train_loader:
            preds = model(images)
            loss = criterion(preds, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        scheduler.step()
        
        # Validation
        model.eval()
        val_acc = compute_accuracy(model, val_loader)
        print(f"Epoch {epoch}: val_acc={val_acc:.4f}")
    
    return model
```

### Progressive Unfreezing

```python
class ProgressiveUnfreeze:
    """Gradually unfreeze layers from top to bottom.
    
    Phase 1: Train new head only (epochs 1-2)
    Phase 2: Unfreeze last block (epochs 3-4)
    Phase 3: Unfreeze more blocks (epochs 5-10)
    """
    
    def __init__(self, model, num_stages=4):
        self.model = model
        self.stages = num_stages
        
        # Freeze all
        for param in model.parameters():
            param.requires_grad = False
    
    def stage(self, stage_num, lr=1e-4):
        """Configure model for training stage."""
        if stage_num == 0:
            # Only train the new head
            for param in self.model.head.parameters():
                param.requires_grad = True
        
        elif stage_num == 1:
            # Unfreeze last block
            for param in self.model.blocks[-1].parameters():
                param.requires_grad = True
        
        elif stage_num >= self.stages - 1:
            # Unfreeze everything
            for param in self.model.parameters():
                param.requires_grad = True
    
    def train(self, train_loader, val_loader, epochs_per_stage=3, base_lr=1e-4):
        for stage in range(self.stages):
            self.stage(stage, base_lr)
            lr = base_lr * (10 ** (-stage))  # Lower LR for early layers
            optimizer = torch.optim.Adam(
                [p for p in self.model.parameters() if p.requires_grad], lr=lr
            )
            
            for epoch in range(epochs_per_stage):
                self._train_epoch(optimizer, train_loader)
                acc = self._evaluate(val_loader)
                print(f"Stage {stage}, Epoch {epoch}: val_acc={acc:.4f}")
```

## Domain Adaptation

### Adversarial Domain Adaptation

```python
class DomainAdversarialNetwork(nn.Module):
    """Domain-adversarial training (Ganin et al., 2016).
    
    Feature extractor trained to fool domain classifier,
    so features become domain-invariant."""
    
    def __init__(self, feature_extractor, num_classes):
        super().__init__()
        self.feature_extractor = feature_extractor
        self.class_classifier = nn.Linear(512, num_classes)
        self.domain_classifier = nn.Sequential(
            nn.Linear(512, 256), nn.ReLU(), nn.Linear(256, 2)  # Source vs target
        )
    
    def forward(self, x, alpha=0.1):
        features = self.feature_extractor(x)
        
        # Gradient reversal layer (implemented via gradient scaling)
        # In forward pass: identity
        # In backward pass: multiply gradients by -alpha
        
        class_output = self.class_classifier(features)
        domain_output = self.domain_classifier(
            GradientReversal.apply(features, alpha)
        )
        
        return class_output, domain_output
```

## Common Pitfalls

1. **Catastrophic forgetting** — fine-tuning on new task destroys pre-trained knowledge; use low LR, shorter training
2. **Domain shift** — pre-trained on ImageNet, deployed on medical images; may need domain adaptation
3. **Head vs body LR** — new head needs higher LR than pre-trained body; use different LR groups
4. **Overly aggressive fine-tuning** — full fine-tuning on tiny dataset overfits; freeze more or use LoRA
5. **Batch norm adaptation** — batchnorm statistics need updating on new domain; use small batches or freeze BN
6. **Task mismatch** — pre-trained on classification, fine-tuned on detection; low-level features still transfer

## Verification Checklist

- [ ] Pre-trained model's input format matches target data (size, normalization, channels)
- [ ] Feature extractor approach evaluated before full fine-tuning
- [ ] Learning rate for fine-tuning lower than from-scratch (1/10th)
- [ ] Catastrophic forgetting checked (pre-training task accuracy preserved)
- [ ] Domain adaptation considered if source/target distributions differ significantly
- [ ] Progressive unfreezing beats one-shot fine-tuning
- [ ] No overfitting on small target dataset (check val vs train gap)

## See Also

- self-supervised-learning — pre-training without labels
- llm-fine-tuning-lora — efficient LLM fine-tuning
- meta-learning-few-shot — learning from very few examples
- ml-pipeline-design — integrating transfer in pipelines
