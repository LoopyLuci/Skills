---
name: recommender-systems-building
description: "Use when building recommendation engine architectures."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [recommender-systems, collaborative-filtering, matrix-factorization, neural-recsys]
    related_skills: [embedding-models-patterns, nlp-techniques, data-augmentation-techniques, ml-pipeline-design]
---

# Building Recommendation Systems

Designing and implementing recommendation engines — from collaborative filtering through matrix factorization to neural recommenders with candidate generation and ranking.

## When to Use

- Building product, content, or media recommendations
- Implementing personalized user experiences
- Designing two-stage (retrieval + ranking) recommendation pipelines
- Cold-start scenarios where user/item have no history
- Building real-time recommendation serving systems

## System Architecture

```
Users → Candidate Generation → Ranking → Re-ranking → Recommendations
                ↓                  ↓
           Multiple Sources    Deep Model
```

## Collaborative Filtering

### User-User and Item-Item

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFiltering:
    """User-based and item-based collaborative filtering."""
    
    def fit(self, user_item_matrix):
        """
        user_item_matrix: shape (n_users, n_items), sparse
        """
        self.user_item = user_item_matrix
        self.user_similarity = cosine_similarity(user_item_matrix)
        self.item_similarity = cosine_similarity(user_item_matrix.T)
    
    def predict_user_based(self, user_id, item_id, k=20):
        """Predict rating using k most similar users who rated the item."""
        # Users who rated this item
        users_who_rated = np.where(self.user_item[:, item_id] > 0)[0]
        if len(users_who_rated) == 0:
            return self.user_item[user_id].mean()
        
        # Similarities between target user and those who rated
        sims = self.user_similarity[user_id, users_who_rated]
        
        # Top-k most similar
        top_k = np.argsort(sims)[-k:]
        top_k_users = users_who_rated[top_k]
        top_k_sims = sims[top_k]
        
        # Weighted average
        ratings = self.user_item[top_k_users, item_id]
        if top_k_sims.sum() == 0:
            return ratings.mean()
        return np.dot(ratings, top_k_sims) / top_k_sims.sum()
```

### Matrix Factorization (SVD)

```python
class SVDRecommender:
    """Matrix factorization via SVD or ALS."""
    
    def __init__(self, n_factors=100, n_epochs=20, lr=0.01, reg=0.02):
        self.n_factors = n_factors
        self.n_epochs = n_epochs
        self.lr = lr
        self.reg = reg
        self.user_factors = None
        self.item_factors = None
    
    def fit(self, ratings):
        """
        ratings: list of (user_id, item_id, rating) or DataFrame
        """
        users = set(r[0] for r in ratings)
        items = set(r[1] for r in ratings)
        self.user_map = {u: i for i, u in enumerate(users)}
        self.item_map = {it: i for i, it in enumerate(items)}
        self.n_users = len(users)
        self.n_items = len(items)
        
        # Initialize factors
        self.user_factors = np.random.normal(0, 0.1, (self.n_users, self.n_factors))
        self.item_factors = np.random.normal(0, 0.1, (self.n_items, self.n_factors))
        self.user_bias = np.zeros(self.n_users)
        self.item_bias = np.zeros(self.n_items)
        self.global_mean = np.mean([r[2] for r in ratings])
        
        # SGD training
        for epoch in range(self.n_epochs):
            np.random.shuffle(ratings)
            total_loss = 0
            
            for user, item, rating in ratings:
                u, i = self.user_map[user], self.item_map[item]
                
                # Predict
                pred = (self.global_mean + self.user_bias[u] + self.item_bias[i] + 
                       np.dot(self.user_factors[u], self.item_factors[i]))
                error = rating - pred
                
                # Update
                self.user_bias[u] += self.lr * (error - self.reg * self.user_bias[u])
                self.item_bias[i] += self.lr * (error - self.reg * self.item_bias[i])
                
                uf = self.user_factors[u].copy()
                self.user_factors[u] += self.lr * (error * self.item_factors[i] - self.reg * self.user_factors[u])
                self.item_factors[i] += self.lr * (error * uf - self.reg * self.item_factors[i])
                
                total_loss += error ** 2
            
            print(f"Epoch {epoch}: RMSE={np.sqrt(total_loss/len(ratings)):.4f}")
    
    def predict(self, user, item):
        u = self.user_map.get(user)
        i = self.item_map.get(item)
        if u is None or i is None:
            return self.global_mean
        return (self.global_mean + self.user_bias[u] + self.item_bias[i] + 
                np.dot(self.user_factors[u], self.item_factors[i]))
```

## Neural Recommenders

### Two-Tower Model (Retrieval)

```python
import torch
import torch.nn as nn

class TwoTowerModel(nn.Module):
    """Two-tower neural network for candidate retrieval.
    User tower + Item tower → dot product → relevance score."""
    
    def __init__(self, num_users, num_items, n_factors=64):
        super().__init__()
        self.user_embedding = nn.Embedding(num_users, n_factors)
        self.item_embedding = nn.Embedding(num_items, n_factors)
        
        # Optional: add user/item features here
        
        self.user_tower = nn.Sequential(
            nn.Linear(n_factors, 128), nn.ReLU(),
            nn.Linear(128, n_factors)
        )
        self.item_tower = nn.Sequential(
            nn.Linear(n_factors, 128), nn.ReLU(),
            nn.Linear(128, n_factors)
        )
    
    def forward(self, user_ids, item_ids):
        user_emb = self.user_embedding(user_ids)
        item_emb = self.item_embedding(item_ids)
        
        user_vec = self.user_tower(user_emb)
        item_vec = self.item_tower(item_emb)
        
        # Normalize for cosine similarity
        user_vec = nn.functional.normalize(user_vec, dim=1)
        item_vec = nn.functional.normalize(item_vec, dim=1)
        
        return (user_vec * item_vec).sum(dim=1)  # Dot product
    
    def get_all_item_vectors(self):
        """Pre-compute item vectors for fast ANN search."""
        all_items = torch.arange(self.item_embedding.num_embeddings)
        return self.item_tower(self.item_embedding(all_items)).detach()
```

### Ranking Model (Deep Neural Network)

```python
class RankingModel(nn.Module):
    """Deep neural ranking model with cross features."""
    
    def __init__(self, n_users, n_items, n_categ_features, n_numerical_features):
        super().__init__()
        self.user_emb = nn.Embedding(n_users, 32)
        self.item_emb = nn.Embedding(n_items, 32)
        
        # Categorical feature embeddings
        self.categ_embeddings = nn.ModuleList([
            nn.Embedding(n, 16) for n in n_categ_features
        ])
        
        total_features = 32 + 32 + len(n_categ_features) * 16 + n_numerical_features
        
        self.deep_layers = nn.Sequential(
            nn.Linear(total_features, 256), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(256, 128), nn.ReLU(), nn.Dropout(0.1),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 1)
        )
    
    def forward(self, user_ids, item_ids, categ_features, numerical_features):
        u_emb = self.user_emb(user_ids)
        i_emb = self.item_emb(item_ids)
        
        c_embs = [emb(categ_features[:, i]) for i, emb in enumerate(self.categ_embeddings)]
        
        features = torch.cat([u_emb, i_emb] + c_embs + [numerical_features], dim=1)
        return self.deep_layers(features)
```

## Two-Stage Pipeline

```python
class RecommendationPipeline:
    """Candidate generation + ranking + re-ranking."""
    
    def __init__(self, retriever, ranker):
        self.retriever = retriever  # TwoTowerModel
        self.ranker = ranker        # RankingModel
    
    def recommend(self, user_id, n_candidates=500, n_final=10):
        # Stage 1: Retrieve candidates
        user_vector = self.retriever.user_tower(
            self.retriever.user_embedding(torch.tensor([user_id]))
        )
        item_vectors = self.retriever.get_all_item_vectors()
        
        # ANN search (simplified — use faiss in production)
        scores = user_vector @ item_vectors.T
        top_candidates = scores.topk(n_candidates).indices[0]
        
        # Stage 2: Rank candidates
        with torch.no_grad():
            ranking_scores = self.ranker(
                torch.full((n_candidates,), user_id),
                top_candidates,
                self._get_features(user_id, top_candidates),
                self._get_numerical(user_id, top_candidates),
            )
        
        # Stage 3: Re-rank (diversity, business rules)
        final_items = self._diversity_rerank(top_candidates, ranking_scores, n_final)
        
        return final_items
```

## Common Pitfalls

1. **Cold start** — new users/items with no history; use content-based features as fallback
2. **Popularity bias** — model recommends popular items that everyone already knows about; use debiasing
3. **Filter bubble** — narrowing recommendations too much; add exploration via bandits
4. **Real-time serving latency** — two-tower retrieval + ANN search is fast; avoid full-ranking every candidate
5. **Evaluation offline ≠ online** — offline metrics don't always predict online A/B test results
6. **Feedback loop** — recommending based on past recommendations can amplify bias; use random exploration

## Verification Checklist

- [ ] Baseline model (popularity) established for comparison
- [ ] Matrix factorization beats collaborative filtering baseline
- [ ] Neural model beats matrix factorization on held-out data
- [ ] Two-stage pipeline (retrieval + ranking) tested for latency
- [ ] Cold-start strategy implemented for new users/items
- [ ] Diversity metric tracked alongside accuracy
- [ ] Online A/B test shows improvement over baseline

## See Also

- embedding-models-patterns — training embeddings for retrieval
- nlp-techniques — content-based features for cold start
- data-augmentation-techniques — augmenting sparse interaction data
- ml-pipeline-design — serving pipeline architecture
