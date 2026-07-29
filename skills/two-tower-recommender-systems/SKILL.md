---
name: two-tower-recommender-systems
description: "Use when building two-tower recommendation models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [recommender-systems, two-tower, retrieval, candidate-generation, softmax, YouTube-DNN]
    related_skills: [recommender-systems-building, embedding-models-patterns, vector-search-indexing, custom-training-loops]
---

# Two-Tower Recommender Systems

Building two-tower (dual-encoder) recommendation models — from candidate generation through approximate nearest neighbor retrieval, training optimization, and serving.

## When to Use

- Large-scale candidate retrieval (millions of items)
- YouTube-style recommendation architecture
- Building embedding-based retrieval systems
- Scaling recommendations to large item catalogs

## Two-Tower Architecture

```python
import torch, torch.nn as nn

class TwoTowerRecommender(nn.Module):
    """Dual-encoder for retrieval: user tower + item tower."""
    def __init__(self, n_users: int, n_items: int, dim: int = 64):
        super().__init__()
        self.user_embed = nn.Embedding(n_users, dim, padding_idx=0)
        self.item_embed = nn.Embedding(n_items, dim, padding_idx=0)
        
        self.user_tower = nn.Sequential(
            nn.Linear(dim, dim*2), nn.ReLU(), nn.Linear(dim*2, dim))
        self.item_tower = nn.Sequential(
            nn.Linear(dim, dim*2), nn.ReLU(), nn.Linear(dim*2, dim))
    
    def forward(self, user_ids, item_ids):
        user_vecs = self.user_tower(self.user_embed(user_ids))
        item_vecs = self.item_tower(self.item_embed(item_ids))
        return (user_vecs @ item_vecs.T)  # similarity matrix
    
    def encode_users(self, user_ids):
        return self.user_tower(self.user_embed(user_ids))
    
    def encode_items(self, item_ids):
        return self.item_tower(self.item_embed(item_ids))


# Sampled softmax loss for efficient training
def sampled_softmax_loss(user_logits, item_logits, labels, n_negatives=100):
    # In-batch negatives
    logits = user_logits @ item_logits.T  # (batch, batch)
    labels = torch.arange(len(user_logits))
    return F.cross_entropy(logits / 0.05, labels)
```

## Verification Checklist

- [ ] User and item towers defined with feature embeddings
- [ ] Training with in-batch negatives or sampled softmax
- [ ] Item embeddings indexed for ANN retrieval (FAISS)
- [ ] Candidate retrieval recall benchmarked (recall@k)
- [ ] Serving pipeline (user query → ANN → ranker → top-k)
- [ ] Freshness: new items indexed regularly
- [ ] A/B test framework for recommendation quality
