---
name: dimensionality-reduction
description: "Use when implementing dimensionality reduction techniques."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [dimensionality-reduction, PCA, t-SNE, UMAP, feature-extraction, manifold-learning]
    related_skills: [feature-engineering-automation, data-visualization-practices, embeddings-visualization, anomaly-detection-ml]
---

# Dimensionality Reduction

Implementing dimensionality reduction — from PCA and t-SNE through UMAP, autoencoders, and feature selection for high-dimensional data.

## When to Use

- Visualizing high-dimensional data in 2D/3D
- Reducing feature space before ML model training
- Removing multicollinearity from feature sets
- Preprocessing for compress or speed up computation
- Exploratory data analysis on complex datasets

## Reduction Methods

```python
REDUCTION_METHODS = {
    'pca': {
        'type': 'Linear, global',
        'best_for': 'Data with linear structure, preprocessing before ML',
        'limitation': 'Assumes linear relationships',
    },
    'tsne': {
        'type': 'Non-linear, local',
        'best_for': 'Visualization (2D/3D), exploring clusters',
        'limitation': 'Non-deterministic, doesn't generalize to new points',
    },
    'umap': {
        'type': 'Non-linear, global+local',
        'best_for': 'Visualization, general-purpose reduction, faster than t-SNE',
        'limitation': 'Sensitive to hyperparameters (n_neighbors, min_dist)',
    },
}

class DimensionalityReducer:
    """Apply dimensionality reduction with automation."""
    def __init__(self, n_components: int = 2):
        self.n = n_components
    
    def reduce_pca(self, X: np.array) -> np.array:
        from sklearn.decomposition import PCA
        pca = PCA(n_components=self.n)
        X_reduced = pca.fit_transform(X)
        self.explained_variance = pca.explained_variance_ratio_
        return X_reduced
    
    def reduce_umap(self, X: np.array, n_neighbors: int = 15, 
                    min_dist: float = 0.1) -> np.array:
        import umap
        reducer = umap.UMAP(n_components=self.n, 
                           n_neighbors=n_neighbors, min_dist=min_dist)
        return reducer.fit_transform(X)
```

## Common Pitfalls

1. **Interpreting PCA components** — they are linear combinations, not real features
2. **t-SNE perplexity mismatch** — wrong perplexity creates misleading clusters; try values 5-50
3. **Losing global structure with t-SNE** — t-SNE preserves local, not global structure; use UMAP
4. **Applying PCA without scaling** — PCA is sensitive to feature scales; standardize first
5. **Reducing then interpreting** — you can't reverse-engineer which original features matter from reduced space

## Verification Checklist

- [ ] Features standardized before PCA
- [ ] Reduction method matches use case (PCA for preprocessing, UMAP for visualization)
- [ ] Explained variance checked for PCA (enough components?)
- [ ] t-SNE perplexity tuned (5-50 range)
- [ ] UMAP n_neighbors and min_dist tuned
- [ ] Results visualized (2D/3D scatter plot colored by target)
- [ ] Downstream model performance compared with/without reduction
