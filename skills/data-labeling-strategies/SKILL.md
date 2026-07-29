---
name: data-labeling-strategies
description: "Use when implementing data labeling workflows and tools."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-labeling, annotation, labeling-tools, quality, consensus, active-learning]
    related_skills: [active-learning-strategies, data-augmentation-techniques, semi-supervised-learning, data-profiling-quality]
---

# Data Labeling Strategies

Implementing data labeling workflows — from tool selection and annotation guidelines through quality control, inter-annotator agreement, and labeling cost optimization.

## When to Use

- Setting up data labeling for ML projects
- Choosing labeling tools (Label Studio, Supervisely, Scale)
- Defining annotation guidelines for consistency
- Measuring and improving label quality
- Optimizing labeling budget with active learning

## Labeling Process

```python
LABELING_APPROACHES = {
    'in_house': 'Domain experts label data — highest quality, highest cost',
    'outsourced': 'Labeling services (Scale, Labelbox) — moderate quality/cost',
    'crowd': 'Mechanical Turk, Appen — variable quality, lowest cost',
    'synthetic': 'Programmatically generated labels — no human cost, quality depends on generator',
    'weak_supervision': 'Snorkel, labeling functions — noisy labels, heuristic rules',
}

def inter_annotator_agreement(labels1: List[str], labels2: List[str]) -> float:
    """Cohen's Kappa for two annotators."""
    from sklearn.metrics import cohen_kappa_score
    return round(cohen_kappa_score(labels1, labels2), 3)
```

## Verification Checklist

- [ ] Annotation guidelines documented with examples
- [ ] Labeling tool chosen and configured
- [ ] Pilot labeling round (50-100 items) before full scale
- [ ] Inter-annotator agreement measured (target: 0.8+ Cohen's Kappa)
- [ ] Quality assurance process (10% re-label, consensus review)
- [ ] Active learning reduces labeling volume
- [ ] Labeled data versioned and stored with provenance
- [ ] Labeling cost per item tracked
