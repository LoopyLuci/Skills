---
name: self-supervised-learning
description: "Use when implementing self-supervised learning methods."
category: mlops
tags: [self-supervised, contrastive, pre-training, ssl, simclr]
---
# Self-Supervised Learning

Pre-training methods that learn from unlabeled data.

## Contrastive Learning (SimCLR)

```python
import torch
import torch.nn.functional as F

def nt_xent_loss(z1, z2, temperature=0.5):
    """Normalized temperature-scaled cross entropy loss."""
    batch_size = z1.shape[0]
    z = torch.cat([z1, z2], dim=0)  # (2N, D)
    z = F.normalize(z, dim=-1)

    # Similarity matrix
    sim = z @ z.T  # (2N, 2N)
    sim = sim / temperature

    # Mask out self-contrast
    mask = ~torch.eye(2 * batch_size, dtype=torch.bool, device=z.device)
    sim = sim[mask].view(2 * batch_size, -1)

    # Positive pairs: i and i+batch_size
    labels = torch.arange(batch_size, device=z.device)
    labels = torch.cat([labels + batch_size, labels])

    return F.cross_entropy(sim, labels)

# Usage
# 1. Apply two different augmentations to same image → x_i, x_j
# 2. Encode both with shared encoder → z_i, z_j
# 3. Maximize agreement with NT-Xent loss
```

## Masked Autoencoders (MAE)

```python
class MAE(nn.Module):
    def __init__(self, encoder, decoder, mask_ratio=0.75):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.mask_ratio = mask_ratio

    def forward(self, x):
        # x: (B, N, D) patches
        B, N, D = x.shape
        num_masked = int(N * self.mask_ratio)

        # Random masking
        noise = torch.rand(B, N, device=x.device)
        ids_shuffle = noise.argsort(dim=1)
        ids_restore = ids_shuffle.argsort(dim=1)

        # Keep visible patches
        ids_keep = ids_shuffle[:, :N - num_masked]
        x_visible = torch.gather(x, 1, ids_keep.unsqueeze(-1).expand(-1, -1, D))

        # Encode visible only
        encoded = self.encoder(x_visible)

        # Decode with mask tokens
        decoder_input = self._add_mask_tokens(encoded, ids_restore, num_masked)
        reconstruction = self.decoder(decoder_input)

        # Loss on masked patches only
        mask = torch.ones(B, N, device=x.device)
        mask[:, :N - num_masked] = 0
        mask = torch.gather(mask, 1, ids_restore)
        loss = (reconstruction - x).pow(2).mean(dim=-1)
        loss = (loss * mask).sum() / mask.sum()

        return loss
```

## BYOL (Bootstrap Your Own Latent)

```python
# No negative pairs needed — predict one view from another

# Online network (trainable): encoder → projector → predictor
# Target network (EMA): encoder → projector (no gradients)
# Loss: MSE between normalized predictions
# Target weights = momentum * target_weights + (1 - momentum) * online_weights
```

## Pre-training Tasks

```
CV:         masked patches, rotation prediction, jigsaw, colorization
NLP:        masked language modeling, next sentence prediction, replaced token detection
Graph:      masked node features, edge prediction, graph completion
Audio:      masked spectrogram, contrastive predictive coding
```

## Pitfalls

- Large batch sizes needed for contrastive learning (4096+ for SimCLR)
- Negative-free methods (BYOL, SimSiam) need predictor and stop-gradient
- Masking ratio matters — MAE uses 75%, BERT uses 15%
- Data augmentation is critical — must be strong enough but not destructive
- SSL features are good for transfer but may need fine-tuning for specific tasks
