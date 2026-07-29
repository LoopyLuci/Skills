---
name: model-interpretability-deep
description: "Use when implementing deep model interpretability methods."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [interpretability, explainability, SHAP, LIME, integrated-gradients, feature-attribution, mechanistic-interpretability]
    related_skills: [explainable-ai-xai-patterns, model-monitoring-drift, feature-engineering-automation, random-forest-advanced]
---

# Deep Model Interpretability

Implementing deep model interpretability — from feature attribution (SHAP, Integrated Gradients) through mechanistic interpretability, activation patching, and sparse autoencoders.

## When to Use

- Understanding why a model made a specific prediction
- Debugging model behavior in production
- Building trust with stakeholders through explanations
- Discovering what neural networks internally represent
- Detecting spurious correlations and shortcut learning

## Interpretability Methods

```python
INTERPRETABILITY_METHODS = {
    'shap': 'SHapley Additive exPlanations — game-theoretic feature attribution',
    'integrated_gradients': 'Path-based attribution for neural networks',
    'activation_patching': 'Intervene on specific neurons/layers, measure effect on output',
    'sparse_autoencoders': 'Learn interpretable features from hidden representations',
    'probing': 'Train simple classifiers on hidden states to detect encoded concepts',
}

def compute_shap_values(model, X, background_data):
    """Compute SHAP feature importance for a model."""
    import shap
    explainer = shap.KernelExplainer(model.predict, background_data)
    shap_values = explainer.shap_values(X, nsamples=100)
    return {
        'shap_values': shap_values,
        'feature_importance': np.abs(shap_values).mean(0),
    }
```

## Verification Checklist

- [ ] Feature attribution method chosen (SHAP, Integrated Gradients, LIME)
- [ ] Explanations are consistent across similar inputs
- [ ] Model behavior documented for key edge cases
- [ ] Mechanistic interpretability for understanding representations
- [ ] Spurious correlations identified and mitigated
- [ ] Explanations validated with domain experts
- [ ] Model card or documentation with interpretability findings
