---
name: explainable-ai-xai-patterns
description: "Use when implementing explainable AI techniques and tools."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [explainability, XAI, interpretability, SHAP, LIME, attention]
    related_skills: [interpretable-ml, adversarial-ml-robustness, ai-fairness-mitigation, agent-safety-alignment]
---

# Explainable AI (XAI) — Implementation Patterns

Implementing explainable AI techniques for understanding, debugging, and trusting model predictions — covering feature attribution, concept-based explanations, counterfactuals, and mechanistic interpretability.

## When to Use

- Debugging why a model made a specific prediction
- Building trust with stakeholders (regulators, users, domain experts)
- Detecting shortcut learning or spurious correlations
- Improving model design through understanding internal mechanisms
- Regulatory compliance requiring explanations (EU AI Act, etc.)
- Red-teaming and safety evaluation of AI systems

## Explanation Types

| Type | What it answers | Methods |
|------|----------------|---------|
| Feature Attribution | Which inputs mattered most? | SHAP, LIME, Integrated Gradients |
| Concept Explanation | What concepts does the model use? | TCAV, Concept Bottleneck |
| Counterfactual | What would change the prediction? | Counterfactual search |
| Mechanistic | How does the model internally compute? | Activation patching, SAEs |
| Example-based | Which training examples drive this prediction? | Influence functions |

## Feature Attribution Methods

### SHAP (SHapley Additive exPlanations)

```python
import shap
import numpy as np

def shap_explain(model, background_data, instance_to_explain):
    """SHAP explanations using KernelSHAP (model-agnostic) or DeepSHAP.
    
    SHAP values show each feature's contribution to the prediction,
    based on cooperative game theory (Shapley values).
    """
    # KernelSHAP: model-agnostic, works with any black-box model
    explainer = shap.KernelExplainer(model.predict, background_data)
    shap_values = explainer.shap_values(instance_to_explain)
    
    # DeepSHAP: efficient for deep learning models
    # explainer = shap.DeepExplainer(model, background_data)
    # shap_values = explainer.shap_values(instance_to_explain)
    
    return shap_values


def visualize_shap(shap_values, features, feature_names):
    """Visualize SHAP values as waterfall or force plot."""
    shap.summary_plot(shap_values, features, feature_names=feature_names)
    shap.waterfall_plot(shap_values[0], features[0], feature_names=feature_names)
```

### LIME (Local Interpretable Model-agnostic Explanations)

```python
import lime
import lime.lime_tabular
import lime.lime_image
import lime.lime_text

def lime_explain_tabular(model, training_data, instance, feature_names):
    """LIME: fit a simple surrogate model locally around the prediction."""
    explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data,
        feature_names=feature_names,
        mode='classification'
    )
    
    exp = explainer.explain_instance(
        instance,
        model.predict_proba,
        num_features=10
    )
    
    exp.show_in_notebook(show_table=True)
    return exp.as_list()


def lime_explain_text(model, text, class_names):
    """LIME explanation for text classification."""
    explainer = lime.lime_text.LimeTextExplainer(class_names=class_names)
    
    exp = explainer.explain_instance(
        text,
        model.predict_proba,
        num_features=6
    )
    
    return exp.as_list()
```

### Integrated Gradients

```python
import torch
import torch.nn.functional as F

def integrated_gradients(model, x, target_class=None, steps=50):
    """Integrated Gradients: path integral of gradients from baseline to input.
    
    Provides feature attributions satisfying:
    - Sensitivity: if changing one feature changes output, it gets non-zero attribution
    - Implementation invariance: identical models get identical attributions
    """
    if target_class is None:
        target_class = model(x).argmax(dim=1)
    
    # Baseline: zero tensor (or mean image for vision)
    baseline = torch.zeros_like(x)
    
    # Riemann approximation of path integral
    scaled_inputs = [baseline + (i / steps) * (x - baseline) for i in range(steps + 1)]
    scaled_inputs = torch.cat(scaled_inputs, dim=0)
    
    # Compute gradients
    scaled_inputs.requires_grad_(True)
    logits = model(scaled_inputs)
    preds = logits[:, target_class]
    
    grads = torch.autograd.grad(preds.sum(), scaled_inputs)[0]
    
    # Average gradients and multiply by (x - baseline)
    avg_grads = grads.mean(dim=0, keepdim=True)
    attributions = (x - baseline) * avg_grads
    
    return attributions


class GradCAM:
    """Gradient-weighted Class Activation Mapping for CNNs.
    Highlights important regions in images for a prediction."""
    
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        target_layer.register_forward_hook(self._forward_hook)
        target_layer.register_full_backward_hook(self._backward_hook)
    
    def _forward_hook(self, module, input, output):
        self.activations = output.detach()
    
    def _backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()
    
    def generate(self, x, class_idx=None):
        """Generate Grad-CAM heatmap."""
        logits = self.model(x)
        
        if class_idx is None:
            class_idx = logits.argmax(dim=1).item()
        
        self.model.zero_grad()
        logits[:, class_idx].backward()
        
        # Global average pool gradients
        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        
        # Weighted combination of activation maps
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = F.relu(cam)  # Only positive contributions
        
        # Normalize
        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)
        
        return cam
```

## Concept-Based Explanations

### TCAV (Testing with Concept Activation Vectors)

```python
class TCAV:
    """Testing with Concept Activation Vectors.
    Quantifies how sensitive a model's predictions are to human-defined concepts
    (e.g., "stripedness" for zebra classification)."""
    
    def __init__(self, model, concept_dataset, random_dataset, layer_name):
        self.model = model
        self.concept_acts = self._get_activations(concept_dataset, layer_name)
        self.random_acts = self._get_activations(random_dataset, layer_name)
    
    def _get_activations(self, dataset, layer_name):
        """Extract activations at a given layer for all examples."""
        activations = []
        hook = self._register_hook(layer_name, activations)
        
        for x in dataset:
            self.model(x)
        
        hook.remove()
        return torch.cat(activations)
    
    def compute_cav(self):
        """Compute Concept Activation Vector (linear classifier)."""
        # Train linear SVM to distinguish concept vs random
        from sklearn.svm import SVC
        
        X = torch.cat([self.concept_acts, self.random_acts]).numpy()
        y = np.array([1]*len(self.concept_acts) + [0]*len(self.random_acts))
        
        cav_model = SVC(kernel='linear', C=1.0)
        cav_model.fit(X, y)
        self.cav = torch.tensor(cav_model.coef_[0])
        
        return self.cav
    
    def tcav_score(self, class_examples):
        """Compute TCAV score: fraction of examples where
        model output increases along the concept direction."""
        class_acts = self._get_activations(class_examples, self.target_layer)
        
        # Directional derivative along CAV
        directional_derivatives = (class_acts @ self.cav)
        return (directional_derivatives > 0).float().mean().item()
```

## Counterfactual Explanations

```python
def generate_counterfactual(model, x, target_class, num_steps=500, lr=0.1):
    """Find the minimal change to x that changes prediction to target_class."""
    x_cf = x.clone().detach().requires_grad_(True)
    optimizer = torch.optim.Adam([x_cf], lr=lr)
    
    for step in range(num_steps):
        logits = model(x_cf)
        # Loss: cross-entropy to target + L1 distance for sparsity
        class_loss = F.cross_entropy(logits, torch.tensor([target_class]))
        dist_loss = torch.abs(x_cf - x).sum()  # L1 for sparsity
        
        loss = class_loss + 0.01 * dist_loss
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if class_loss < 0.01:
            print(f"Counterfactual found at step {step}")
            break
    
    return x_cf.detach()
```

## Mechanistic Interpretability

### Activation Patching

```python
def activation_patching(model, original_input, patched_input, layer_name, neuron_idx=None):
    """Replace activations at a specific layer/neuron from patched_input
    into original_input. Measures causal effect on output."""
    
    stored_activation = None
    
    def hook_fn(module, input, output):
        nonlocal stored_activation
        if neuron_idx is not None:
            stored_activation = output[:, :, neuron_idx].clone()
        else:
            stored_activation = output.clone()
        return output
    
    hook = getattr(model, layer_name).register_forward_hook(hook_fn)
    
    # Run patched input to get its activations
    _ = model(patched_input)
    hook.remove()
    
    # Now patch into original input
    def patch_hook(module, input, output):
        if neuron_idx is not None:
            output[:, :, neuron_idx] = stored_activation
        else:
            output = stored_activation
        return output
    
    patch_hook_handle = getattr(model, layer_name).register_forward_hook(patch_hook)
    patched_logits = model(original_input)
    patch_hook_handle.remove()
    
    return patched_logits
```

### Sparse Autoencoders (Feature Extraction)

```python
class SparseAutoencoder(nn.Module):
    """Train sparse autoencoders on model activations to find interpretable features.
    Key technique in mechanistic interpretability (Anthropic's SAE work)."""
    
    def __init__(self, activation_dim, hidden_dim_mult=8, l1_coef=0.001):
        super().__init__()
        hidden_dim = activation_dim * hidden_dim_mult  # Overcomplete
        self.encoder = nn.Linear(activation_dim, hidden_dim, bias=False)
        self.decoder = nn.Linear(hidden_dim, activation_dim, bias=False)
        self.l1_coef = l1_coef
    
    def forward(self, x):
        encoded = torch.relu(self.encoder(x))  # Sparse!
        reconstructed = self.decoder(encoded)
        
        # L1 regularization for sparsity
        sparsity_loss = self.l1_coef * encoded.abs().sum()
        recon_loss = F.mse_loss(reconstructed, x)
        
        return reconstructed, encoded, recon_loss + sparsity_loss
```

## Common Pitfalls

1. **Explanation ≠ cause** — feature attributions show correlation, not causation; use causal methods for causal questions
2. **Model complexity tradeoff** — simpler models are more interpretable but less accurate; use XAI on complex models
3. **Over-relying on saliency maps** — saliency maps can be misleading (sensitivity to preprocessing); validate with multiple methods
4. **Feature attribution instability** — SHAP values can vary between runs; stabilize with multiple background sets
5. **User misinterpretation** — non-technical users may misinterpret explanations; design explanations for the audience
6. **Explanation quality metrics** — there's no single "correct" explanation; use faithfulness + comprehensiveness metrics

## Verification Checklist

- [ ] Explanation method chosen matches the task type (tabular/image/text) and audience
- [ ] Faithfulness verified: features with high attribution actually affect the prediction
- [ ] Robustness verified: small input changes don't drastically change explanations
- [ ] Multiple explanation methods compared for consistency
- [ ] Explanations tested with end users (do they trust appropriately?)
- [ ] Limitation of method documented (e.g., LIME assumes local linearity)

## See Also

- interpretable-ml — deeper coverage of ML interpretability
- adversarial-ml-robustness — robustness vs. explanations
- ai-fairness-mitigation — fairness detection via explanations
- agent-safety-alignment — using XAI for safety evaluation
