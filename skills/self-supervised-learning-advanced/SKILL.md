---
name: self-supervised-learning-advanced
description: "Use when implementing advanced self-supervised learning."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [self-supervised, SSL, contrastive-learning, masked-modeling, SimCLR, MAE]
    related_skills: [semi-supervised-learning, data-augmentation-techniques, custom-training-loops, embeddings-visualization]
---

# Advanced Self-Supervised Learning

Implementing advanced self-supervised learning — from contrastive methods (SimCLR, MoCo, BYOL) through masked modeling (MAE, BERT-style) and joint embedding architectures.

## When to Use

- Pre-training models without labeled data
- Learning representations from unlabeled data
- Improving downstream task performance with SSL pre-training
- Reducing labeled data requirements for fine-tuning

## SSL Methods

```python
SSL_METHODS = {
    'contrastive': 'SimCLR, MoCo — pull positive pairs together, push negatives apart',
    'masked': 'MAE, BERT — mask input patches/tokens, reconstruct missing content',
    'clustering': 'SwAV, DeepCluster — cluster representations, enforce cluster consistency',
    'distillation': 'BYOL, DINO — student-teacher with no negatives, momentum encoder',
    'whitening': 'W-MSE, Barlow Twins — decorrelate feature dimensions, redundancy reduction',
}

class SimCLR:
    """Simplified SimCLR contrastive learning."""
    def __init__(self, encoder, projection_dim=128, temperature=0.5):
        self.encoder = encoder
        self.projection = nn.Linear(encoder.output_dim, projection_dim)
        self.temperature = temperature
    
    def contrastive_loss(self, z_i, z_j):
        """NT-Xent loss — InfoNCE with temperature."""
        z_i = F.normalize(z_i, dim=1)
        z_j = F.normalize(z_j, dim=1)
        representations = torch.cat([z_i, z_j], dim=0)
        similarity = representations @ representations.T / self.temperature
        # Labels: diagonal = positive pairs
        batch_size = z_i.shape[0]
        labels = torch.arange(batch_size, device=z_i.device)
        labels = torch.cat([labels + batch_size, labels])
        mask = ~torch.eye(2 * batch_size, dtype=bool)
        return F.cross_entropy(similarity[mask].view(2 * batch_size, -1), labels)
```

## Verification Checklist

- [ ] SSL method matched to data type (contrastive for vision, masked for text)
- [ ] Strong augmentation pipeline for positive pair generation
- [ ] Projection head used for representation learning
- [ ] Training stabilizes without collapse (monitor uniformity + alignment)
- [ ] Downstream task improvement measured (with vs without SSL pre-training)
- [ ] Batch size sufficient for contrastive methods (256+ recommended)
