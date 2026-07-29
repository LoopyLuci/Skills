---
name: interpretable-ml
description: "Use when explaining and interpreting ML model predictions."
category: mlops
tags: [interpretability, explainability, shap, lime, xai]
---
# Interpretable ML

Explaining and interpreting machine learning model predictions.

## When to Use Each Method

| Method | Scope | Speed | Model-Agnostic | Best For |
|--------|-------|-------|---------------|----------|
| SHAP | Local + Global | Slow | Yes | Any model, feature importance |
| LIME | Local | Medium | Yes | Single prediction explanation |
| Integrated Gradients | Local | Fast | No | Deep learning |
| Attention Weights | Local | Fast | No | Transformers |
| Partial Dependence | Global | Medium | Yes | Feature effect |
| Permutation Importance | Global | Fast | Yes | Feature ranking |

## SHAP

```python
import shap

# Tree explainer (fast for XGBoost, LightGBM, RF)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# Summary plot
shap.summary_plot(shap_values, X)

# Force plot for single prediction
shap.force_plot(explainer.expected_value, shap_values[0], X.iloc[0])

# Deep explainer (for neural networks)
explainer = shap.DeepExplainer(model, background_data)
shap_values = explainer.shap_values(X_test[:100])
```

## LIME

```python
from lime import lime_tabular
import numpy as np

explainer = lime_tabular.LimeTabularExplainer(
    X_train.values,
    feature_names=feature_names,
    class_names=['negative', 'positive'],
    mode='classification',
)

exp = explainer.explain_instance(
    X_test.iloc[0].values,
    model.predict_proba,
    num_features=10,
)

exp.show_in_notebook()
exp.as_list()  # [(feature, weight), ...]
```

## Integrated Gradients

```python
def integrated_gradients(model, input_tensor, baseline=None, steps=50):
    if baseline is None:
        baseline = torch.zeros_like(input_tensor)
    scaled_inputs = [baseline + (i/steps) * (input_tensor - baseline)
                     for i in range(steps + 1)]
    scaled_inputs = torch.stack(scaled_inputs)
    scaled_inputs.requires_grad_(True)

    outputs = model(scaled_inputs)
    pred = outputs[:, outputs.argmax(dim=-1)]
    grad = torch.autograd.grad(pred.sum(), scaled_inputs)[0]

    avg_grad = (grad[:-1] + grad[1:]).mean(dim=0) / 2
    ig = (input_tensor - baseline) * avg_grad
    return ig.sum(dim=-1)  # feature attributions per token
```

## Attention Visualization

```python
# For transformer models
def visualize_attention(tokens, attention_weights, layer=-1, head=0):
    # attention_weights: (layers, heads, seq_len, seq_len)
    attn = attention_weights[layer, head].detach().numpy()
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(attn, cmap='Blues')
    ax.set_xticks(range(len(tokens)))
    ax.set_yticks(range(len(tokens)))
    ax.set_xticklabels(tokens, rotation=90)
    ax.set_yticklabels(tokens)
```

## Pitfalls

- SHAP is computationally expensive for large models and datasets
- LIME results vary between runs due to sampling — set seed for reproducibility
- Attention ≠ explanation (different attention distributions can give same output)
- Feature importance measures correlation, not causation
- Local explanations don't generalize to global behavior
