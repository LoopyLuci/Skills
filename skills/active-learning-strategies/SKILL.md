---
name: active-learning-strategies
description: "Use when implementing active learning for data labeling."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [active-learning, data-labeling, uncertainty-sampling, query-strategies, annotation]
    related_skills: [semi-supervised-learning, data-augmentation-techniques, feature-engineering-automation, ml-pipeline-design]
---

# Active Learning Strategies

Implementing active learning to reduce labeling costs — from uncertainty sampling and diversity sampling through query strategies and human-in-the-loop workflows.

## When to Use

- Labeled data is expensive or time-consuming to obtain
- Large pool of unlabeled data with limited annotation budget
- Building models that improve with strategic labeling
- Medical imaging, legal document review, rare event detection
- Optimizing labeling ROI

## Query Strategies

```python
ACTIVE_LEARNING_STRATEGIES = {
    'uncertainty_sampling': 'Label examples model is most uncertain about (lowest confidence)',
    'margin_sampling': 'Label examples where top two class probabilities are closest',
    'entropy_sampling': 'Label examples with highest predictive entropy',
    'diversity_sampling': 'Select diverse examples covering the feature space',
    'expected_error_reduction': 'Select examples that would most reduce expected generalization error',
    'query_by_committee': 'Train multiple models, label examples they disagree on most',
}

class UncertaintySampler:
    """Select most uncertain examples for labeling."""
    
    def __init__(self, model):
        self.model = model
    
    def query(self, unlabeled_pool, n: int = 10) -> List[int]:
        """Return indices of top-N most uncertain examples."""
        probs = self.model.predict_proba(unlabeled_pool)
        # Least confidence: 1 - max probability
        uncertainty = 1 - probs.max(axis=1)
        return np.argsort(uncertainty)[-n:][::-1]


class DiversitySampler:
    """Select diverse examples covering the feature space."""
    
    def __init__(self, embedding_model):
        self.model = embedding_model
    
    def query(self, unlabeled_pool, n: int = 10) -> List[int]:
        """Use k-center clustering for diversity sampling."""
        from sklearn.cluster import KMeans
        embeddings = self.model(unlabeled_pool)
        kmeans = KMeans(n_clusters=n, random_state=42)
        kmeans.fit(embeddings)
        # Select nearest point to each cluster center
        indices = []
        for center in kmeans.cluster_centers_:
            distances = np.linalg.norm(embeddings - center, axis=1)
            indices.append(np.argmin(distances))
        return indices
```

## Common Pitfalls

1. **Sampling bias** — uncertainty sampling may never select certain classes; combine with diversity
2. **Cost of annotation** — some examples cost more to label; consider cost-sensitive acquisition
3. **Model change** — examples selected early may not be useful after model updates; use batch mode
4. **Cold start** — no initial model for uncertainty; start with random sampling
5. **Labeler inconsistency** — different labelers give different labels; measure inter-rater reliability

## Verification Checklist

- [ ] Initial labeled set exists (minimum 20-50 per class)
- [ ] Query strategy chosen (uncertainty, diversity, committee, or hybrid)
- [ ] Batch size defined (how many to label per iteration)
- [ ] Annotation budget defined (max labels per iteration, total budget)
- [ ] Model retrained and evaluated after each labeling batch
- [ ] Stopping criterion defined (no improvement plateau)
- [ ] Labeler agreement measured
