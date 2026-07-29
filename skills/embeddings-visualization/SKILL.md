---
name: embeddings-visualization
description: "Use when visualizing and analyzing embeddings."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [embeddings, visualization, t-SNE, UMAP, vector-space, clustering, similarity]
    related_skills: [dimensionality-reduction, embedding-models-patterns, data-visualization-practices, data-profiling-quality]
---

# Embeddings Visualization

Visualizing and analyzing high-dimensional embeddings — from dimensionality reduction (UMAP, t-SNE) through interactive visualization, cluster analysis, and similarity search.

## When to Use

- Understanding embedding space structure and clusters
- Debugging embedding quality and semantic relationships
- Presenting embedding analysis to stakeholders
- Finding patterns in high-dimensional vector spaces

## Visualization Pipeline

```python
import numpy as np
from typing import List, Dict

class EmbeddingVisualizer:
    """Reduce and visualize embedding spaces."""
    
    @staticmethod
    def reduce(embeddings: np.array, method: str = 'umap', 
               n_components: int = 2) -> np.array:
        if method == 'umap':
            import umap
            reducer = umap.UMAP(n_components=n_components)
        elif method == 'tsne':
            from sklearn.manifold import TSNE
            reducer = TSNE(n_components=n_components)
        elif method == 'pca':
            from sklearn.decomposition import PCA
            reducer = PCA(n_components=n_components)
        return reducer.fit_transform(embeddings)
    
    @staticmethod
    def find_clusters(reduced: np.array, 
                      min_clusters: int = 3, max_clusters: int = 10) -> Dict:
        from sklearn.cluster import HDBSCAN
        clusterer = HDBSCAN(min_cluster_size=5)
        labels = clusterer.fit_predict(reduced)
        return {
            'n_clusters': len(set(labels) - {-1}),
            'noise_points': int((labels == -1).sum()),
            'labels': labels.tolist(),
        }
```

## Verification Checklist

- [ ] Embedding dimension reduced to 2D/3D for visualization
- [ ] Labels/colors applied for semantic interpretation
- [ ] Clusters identified (HDBSCAN or similar)
- [ ] Nearest neighbor search working on reduced space
- [ ] Visualizations explainable to stakeholders
- [ ] Outlier/novelty detection from embedding space
