---
name: vector-search-indexing
description: "Use when implementing vector search indexing algorithms."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vector-search, ANN, HNSW, IVF, PQ, similarity-search, indexing]
    related_skills: [embedding-models-patterns, embeddings-visualization,rag-system-design, large-language-model-optimization]
---

# Vector Search and Indexing

Implementing vector search indexing algorithms — from HNSW and IVF through product quantization, filtering, hybrid search, and distributed vector databases.

## When to Use

- Building semantic search with embedding vectors
- Implementing approximate nearest neighbor (ANN) search
- Scaling vector search to millions/billions of vectors
- Hybrid search combining vector + keyword (BM25)

## Indexing Algorithms

```python
INDEXING_ALGORITHMS = {
    'flat': 'Brute force — exact, O(n*d), good for <10K vectors',
    'ivf': 'Inverted File Index — k-means clustering, coarse quantizer, O(log n)',
    'hnsw': 'Hierarchical Navigable Small World — graph-based, best recall/speed tradeoff',
    'pq': 'Product Quantization — compresses vectors, reduces memory 4-8x',
    'ivf_pq': 'IVF + PQ — combination for billion-scale search',
}

class VectorIndexBuilder:
    """Build and query vector indexes."""
    def __init__(self, dimension: int, index_type: str = 'hnsw'):
        import faiss
        self.dim = dimension
        
        if index_type == 'flat': self.index = faiss.IndexFlatL2(dimension)
        elif index_type == 'hnsw':
            self.index = faiss.IndexHNSWFlat(dimension, 32)  # 32 neighbors
        elif index_type == 'ivf':
            self.index = faiss.IndexIVFFlat(faiss.IndexFlatL2(dimension), dimension, 100)
            self.index.train = lambda x: None
    
    def add(self, vectors): self.index.add(vectors)
    def search(self, query, k: int = 10): return self.index.search(query, k)
```

## Verification Checklist

- [ ] Index type matches dataset size (Flat <10K, IVF <1M, HNSW <100M, IVF+PQ >100M)
- [ ] Recall benchmarked against brute force (target: >95% recall@10)
- [ ] Index build time and memory usage measured
- [ ] Filtering support (metadata pre-filter or post-filter)
- [ ] Hybrid search: vector + keyword (BM25) fusion
- [ ] Distributed indexing (sharding) for billion-scale
- [ ] Index update strategy (incremental add, delete)
