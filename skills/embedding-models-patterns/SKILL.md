---
name: embedding-models-patterns
description: "Use when training embeddings and vector search indexes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [embeddings, vector-search, similarity, ANN, faiss, sentence-transformers]
    related_skills: [rag-system-design, recommender-systems-building, nlp-techniques, knowledge-management-systems]
---

# Embedding Models and Vector Search

Training, evaluating, and deploying embedding models with vector search for similarity, retrieval, and semantic search applications.

## When to Use

- Building semantic search or RAG (retrieval augmented generation) systems
- Implementing similarity-based recommendations (item2vec)
- Clustering or categorizing text/images by semantic similarity
- Building deduplication or near-duplicate detection systems
- Reducing dimensionality while preserving semantic relationships

## Embedding Model Training

### Contrastive Learning (SimCSE)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimCSETrainer:
    """Unsupervised SimCSE: uses dropout as data augmentation.
    Same sentence through model twice = positive pair."""
    
    def __init__(self, model, temperature=0.05):
        self.model = model
        self.temp = temperature
    
    def train_step(self, batch):
        (input_ids1, mask1), (input_ids2, mask2) = batch
        
        z1 = self.model(input_ids1, mask1)
        z2 = self.model(input_ids2, mask2)
        
        batch_size = z1.shape[0]
        reps = torch.cat([z1, z2], dim=0)
        sim = reps @ reps.T / self.temp
        
        labels = torch.arange(batch_size, device=z1.device)
        labels = torch.cat([labels + batch_size, labels])
        
        mask = ~torch.eye(2 * batch_size, dtype=torch.bool, device=z1.device)
        sim = sim[mask].view(2 * batch_size, -1)
        
        return F.cross_entropy(sim, labels)
```

### Mean Pooling for Embeddings

```python
class MeanPoolingEmbedding(nn.Module):
    """Transformer encoder with mean pooling over token embeddings."""
    
    def __init__(self, encoder):
        super().__init__()
        self.encoder = encoder
    
    def forward(self, input_ids, attention_mask=None):
        outputs = self.encoder(input_ids, attention_mask=attention_mask)
        token_embeddings = outputs.last_hidden_state
        if attention_mask is None:
            return token_embeddings.mean(dim=1)
        mask = attention_mask.unsqueeze(-1).float()
        return (token_embeddings * mask).sum(dim=1) / mask.sum(dim=1)
```

## Vector Search with FAISS

```python
import faiss
import numpy as np

def build_index(embeddings, index_type='IVF'):
    """Build a FAISS vector search index."""
    dim = embeddings.shape[1]
    n = embeddings.shape[0]
    
    if n < 1000:
        return faiss.IndexFlatIP(dim)  # Exact search
    
    elif index_type == 'IVF':
        nlist = int(4 * np.sqrt(n))
        quantizer = faiss.IndexFlatIP(dim)
        index = faiss.IndexIVFFlat(quantizer, dim, nlist, faiss.METRIC_INNER_PRODUCT)
        index.train(embeddings)
    
    elif index_type == 'HNSW':
        index = faiss.IndexHNSWFlat(dim, 32)
        index.hnsw.efConstruction = 200
    
    index.add(embeddings)
    return index

def search(index, query_emb, k=10):
    if query_emb.ndim == 1:
        query_emb = query_emb.reshape(1, -1)
    scores, indices = index.search(query_emb, k)
    return scores[0], indices[0]
```

## Evaluation

```python
def evaluate_retrieval(embeddings, queries, relevant_docs, k=10):
    """Mean Reciprocal Rank @ k."""
    index = build_index(embeddings)
    mrr = 0
    for q_emb, relevant in zip(queries, relevant_docs):
        _, indices = search(index, q_emb, k)
        for rank, idx in enumerate(indices, 1):
            if idx in relevant:
                mrr += 1.0 / rank; break
    return mrr / len(queries)
```

## Common Pitfalls

1. **Embedding drift** — model updates change vectors; version embeddings
2. **Normalization** — most metrics assume normalized vectors; always normalize
3. **Index staleness** — new items not indexed; incremental indexing needed
4. **Dimensionality** — above ~1000 dims distances concentrate; use 128-768
5. **Cold start** — new items without embeddings; use content-based init
6. **Memory** — >10M vectors need significant RAM; use PQ compression

## Verification Checklist

- [ ] Cosine similarity works on known similar/dissimilar pairs
- [ ] FAISS returns relevant results (manual top-5 check)
- [ ] Dimension appropriate for dataset size
- [ ] Vectors normalized before indexing
- [ ] Search latency <50ms for interactive use
- [ ] Index updated regularly

## See Also

- rag-system-design — using embeddings for RAG
- recommender-systems-building — embedding-based recommendations
- nlp-techniques — text embedding models
- knowledge-management-systems — organizing embedded knowledge
