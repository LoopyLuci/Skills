---
name: knowledge-distillation
description: "Use when compressing models via knowledge distillation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [knowledge-distillation, model-compression, student-teacher, quantization]
    related_skills: [model-compression-techniques, custom-training-loops, transformer-architectures, ml-model-serving-optimization]
---

# Knowledge Distillation

Compressing large teacher models into smaller student models via knowledge distillation — from logit-based and feature-based distillation through self-distillation and distillation for LLMs.

## When to Use

- Deploying large models where latency/cost matter
- Compressing an ensemble into a single model
- Transferring knowledge from a large teacher to a deployable student
- Improving a small model's performance beyond its capacity
- Building production-ready models from research-scale models

## Distillation Methods

```python
DISTILLATION_TYPES = {
    'logit_based': 'Student learns from teacher soft labels (temperature-scaled)',
    'feature_based': 'Student matches teacher intermediate representations',
    'relation_based': 'Student learns relationships between samples from teacher',
    'self_distillation': 'Model distills knowledge into itself (no separate teacher)',
    'online_distillation': 'Teacher and student trained simultaneously',
}
```

## Logit-Based Distillation

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DistillationLoss:
    """Knowledge distillation loss combining hard and soft targets.
    
    Loss = α * CE(student_logits, hard_label) 
         + (1-α) * KL(student_soft, teacher_soft) * T²
    """
    
    def __init__(self, temperature: float = 4.0, alpha: float = 0.3):
        self.T = temperature
        self.alpha = alpha
    
    def __call__(self, student_logits, teacher_logits, targets):
        # Hard loss (standard cross-entropy)
        hard_loss = F.cross_entropy(student_logits, targets)
        
        # Soft loss (KL divergence between temperature-scaled distributions)
        soft_student = F.log_softmax(student_logits / self.T, dim=1)
        soft_teacher = F.softmax(teacher_logits.detach() / self.T, dim=1)
        soft_loss = F.kl_div(soft_student, soft_teacher, reduction='batchmean') * (self.T ** 2)
        
        return self.alpha * hard_loss + (1 - self.alpha) * soft_loss


def distill_model(teacher, student, train_loader, epochs=10, T=4.0, alpha=0.3, lr=1e-4):
    """Train a student model using knowledge distillation."""
    criterion = DistillationLoss(T, alpha)
    optimizer = torch.optim.Adam(student.parameters(), lr=lr)
    
    teacher.eval()
    student.train()
    
    for epoch in range(epochs):
        total_loss = 0
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            
            with torch.no_grad():
                teacher_logits = teacher(inputs)
            
            student_logits = student(inputs)
            loss = criterion(student_logits, teacher_logits, targets)
            
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        print(f"Epoch {epoch}: Distillation Loss = {total_loss/len(train_loader):.4f}")
    
    return student
```

## Feature-Based Distillation

```python
class FeatureDistillation(nn.Module):
    """Match intermediate features between teacher and student.
    
    Student regresses to match teacher's intermediate representations,
    not just final outputs."""
    
    def __init__(self, student, teacher, student_feature_dims, teacher_feature_dims):
        super().__init__()
        self.student = student
        self.teacher = teacher
        
        # Projection layers to align feature dimensions
        self.projections = nn.ModuleList([
            nn.Linear(s_dim, t_dim) if s_dim != t_dim else nn.Identity()
            for s_dim, t_dim in zip(student_feature_dims, teacher_feature_dims)
        ])
    
    def forward(self, x):
        """Compute feature matching loss."""
        s_features = self.student.get_intermediate_features(x)
        t_features = self.teacher.get_intermediate_features(x)
        
        total_loss = 0
        for s_feat, t_feat, proj in zip(s_features, t_features, self.projections):
            s_proj = proj(s_feat)
            loss = F.mse_loss(s_proj, t_feat.detach())
            total_loss += loss
        
        return total_loss
```

## Common Pitfalls

1. **Temperature too high or low** — T ~4 is a good starting point; tune for your task
2. **Student too small** — extremely small students can't capture teacher knowledge; find minimum viable size
3. **Overfitting to teacher** — student memorizes teacher mistakes; use hard labels too (α ≥ 0.3)
4. **Feature mismatch** — student and teacher have different architecture shapes; projection layers needed
5. **Not using teacher's strengths** — logit distillation works best; feature distillation adds marginal benefit

## Verification Checklist

- [ ] Teacher model achieves target accuracy before distillation
- [ ] Student model trains with distillation loss converging
- [ ] Student accuracy approaches teacher's (within 1-3%)
- [ ] Student parameter count < 30% of teacher
- [ ] Student inference speed benchmarked (vs teacher)
- [ ] Temperature and alpha hyperparameters tuned
- [ ] Ablation: student trained with/without distillation compared

## See Also

- model-compression-techniques — broader compression beyond distillation
- custom-training-loops — implementing distillation in training
- transformer-architectures — distilling transformers
- ml-model-serving-optimization — deploying distilled models
