---
name: data-synthesis-generation
description: "Use when generating synthetic data for ML training."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [synthetic-data, data-generation, GAN, diffusion, augmentation, privacy]
    related_skills: [data-augmentation-techniques, data-labeling-strategies, privacy-training, active-learning-strategies]
---

# Data Synthesis and Generation

Generating synthetic data for ML training — from tabular data synthesis through image generation with GANs/diffusion models and privacy-preserving synthetic data.

## When to Use

- Insufficient real data for ML training
- Privacy concerns with real data (HIPAA, GDPR)
- Balancing class distributions (rare events, edge cases)
- Testing systems with controlled data properties

## Synthesis Methods

```python
SYNTHESIS_METHODS = {
    'tabular': 'CTGAN, TVAE, SDV — preserve statistical properties of real data',
    'image': 'Stable Diffusion, StyleGAN, DALL-E — photorealistic or domain-specific',
    'text': 'LLM-based generation — prompts to generate labeled text data',
    'time_series': 'DoppelGANger, TimeGAN — temporal pattern preservation',
    'privacy': 'Differentially private synthetic data — mathematical privacy guarantee',
}

def generate_tabular_synthetic(real_data: pd.DataFrame, n_rows: int = 1000) -> pd.DataFrame:
    """Generate synthetic tabular data using SDV."""
    from sdv.tabular import CTGAN
    model = CTGAN(epochs=50)
    model.fit(real_data)
    return model.sample(n_rows)
```

## Verification Checklist

- [ ] Synthetic data preserves key statistical properties (means, correlations, distributions)
- [ ] No identity leakage from training data (privacy audit)
- [ ] Downstream model performance matches real-data training
- [ ] Edge cases and rare events adequately represented
- [ ] Synthetic data quality metrics measured (statistical similarity, utility)
- [ ] Privacy guarantees documented (differential privacy epsilon if applicable)
