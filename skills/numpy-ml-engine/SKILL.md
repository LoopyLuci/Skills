---
name: numpy-ml-engine
description: "Build ML models from scratch in NumPy for apps."
version: 1.0.0
author: Hermes Agent
tags: [numpy, ml, neural-networks, from-scratch, models]
related_skills: [pyqt5-desktop-dev]
---

# NumPy ML Engine — Build Models From Scratch

## When to Use

Use when the user wants ML models built WITHOUT external frameworks (TensorFlow, PyTorch, scikit-learn, JAX). All models are implemented purely in NumPy for full independence from external ML dependencies.

## Core Architecture

### Layer Stack (`ml_engine/__init__.py`)

```python
from webbuilder.ml_engine import (
    Dense, Dropout, BatchNorm, Conv2D, MaxPool2D, LSTM,
    ModelTrainer, ModelRegistry
)
```

| Layer | Purpose | Activation |
|-------|---------|------------|
| `Dense(in, out, activation)` | Fully connected | relu, sigmoid, tanh, softmax, linear |
| `Dropout(p)` | Regularization | — |
| `BatchNorm(dim)` | Stabilize training | — |
| `Conv2D(in_ch, out_ch, k, stride, padding)` | Image features | relu |
| `MaxPool2D(pool_size)` | Downsampling | — |
| `LSTM(input_dim, hidden_dim)` | Sequence modeling | — |

### Training Pipeline

```python
trainer = ModelTrainer(layers, learning_rate=0.001)
trainer.train(X_train, y_train, epochs=50, batch_size=32,
             val_data=(X_val, y_val), loss_type='mse')
```

**Loss types:** `mse` (regression), `crossentropy` (classification)

### Model Registry & Persistence

```python
from webbuilder.ml_engine.persistence import save_model, load_model, model_exists

save_model('color_harmony', layers)
load_model('color_harmony', layers)
model_exists('color_harmony')  # bool
```

Weights saved to `~/.webbuilder/ml_models/<name>.npz`

## Gradient Clipping — Critical Fix

**Problem:** Training with synthetic data causes gradient explosion → NaN weights.

**Fix:** Clip gradients to [-1, 0, 1.0] before SGD update:

```python
np.clip(layer.grads['W'], -1.0, 1.0, out=layer.grads['W'])
np.clip(layer.grads['b'], -1.0, 1.0, out=layer.grads['b'])
layer.params['W'] -= self.lr * layer.grads['W']
```

## Specialized Models for Web Builders

| Model | Input Dims | Output Dims | Use Case |
|-------|-----------|-------------|----------|
| ColorHarmonyModel | 33 | 15 (5 colors RGB) | WCAG-compliant palettes |
| LayoutGenerationModel | 33 | 130 (positions/spacing/alignment) | Optimal section layout |
| TypographyPairingModel | 45 | 100 (2 fonts) | Font pairing suggestions |
| PageSpeedModel | 5 | 2 (load time, score) | Performance prediction |
| AccessibilityComplianceModel | 280 | 30 (violations) | WCAG 2.1 detection |
| CodeCompletionModel | 50 tokens | vocab_size | HTML/CSS/JS completion |
| UserIntentPredictionModel | 324 | 50 (actions) | Next-action prediction |

## Synthetic Data Generation

When real training data is unavailable, generate synthetic data for initial validation:

```python
from webbuilder.ml_engine.data import DataGenerator
X, y = DataGenerator.generate_color_data(5000)
X, y = DataGenerator.generate_speed_data(5000)
```

**Pattern:** Generate data with correct input/output dimensions matching the model architecture. Use `np.random.seed(42)` for reproducibility.

## GUI Integration Pattern

```python
# In GUI method
def _generate_color_palette(self):
    from webbuilder.ml_engine.models import MLModelFactory
    factory = MLModelFactory()
    model = factory.get('color_harmony')
    palette = model.generate('#3b82f6', 'professional', 'tech')
    # Display results in QMessageBox or custom dialog
```

**Factory pattern:** `MLModelFactory.get(name)` returns cached instance. Call `MLModelFactory.load_all()` at startup to load trained weights.

## Self-Learning Pipeline

`webbuilder/ml_engine/self_learning.py` — online learning from user interactions:
- `SelfLearningPipeline` wraps any MLModel with experience replay
- Records `(state, action, reward, next_state)` tuples during user interactions
- Periodically retrains with replay buffer via `retrain()`
- Persists replay buffer to disk; loads on startup
- Integrates with TrainingDashboard — training records interaction data automatically

```python
from webbuilder.ml_engine.self_learning import SelfLearningPipeline

pipeline = SelfLearningPipeline(model, buffer_size=10000)
pipeline.record_interaction(state, action, reward, next_state)
pipeline.retrain(batch_size=64, epochs=5)
pipeline.save()  # Persists buffer + model weights
```

## Common Pitfalls

1. **Dimension mismatch** — Input layer dim must match feature vector size exactly. Use `np.concatenate` carefully.
2. **Gradient explosion** — Always clip gradients when training with synthetic data.
3. **NaN weights** — Check for overflow in sigmoid/tanh. Use `np.clip` on inputs.
4. **Softmax overflow** — Subtract max before exponent: `exp(x - max(x))`.
5. **LSTM backward pass** — Complex; verify gradients numerically if loss diverges.
6. **Persistence** — Weights are NumPy arrays. Use `np.savez` / `np.load` for storage.
7. **Model not saved** — Call `save_model(name, layers)` AFTER training. Weights are lost otherwise.

## Verification

```python
# Test each model produces valid output
factory = MLModelFactory()
palette = factory.get('color_harmony').generate('#3b82f6')
assert 'primary' in palette
assert 'secondary' in palette

speed = factory.get('page_speed').analyze(1500, 250000, 25, 800, 5)
assert 'load_time_ms' in speed
assert 'lighthouse_score' in speed
```

## References

- [layer-implementations.md](references/layer-implementations.md) — Dense, Conv2D, LSTM forward/backward math
- [model-architectures.md](references/model-architectures.md) — Full specs for all 7 models
- [training-recipes.md](references/training-recipes.md) — Epochs, batch sizes, learning rates per model
- [gui-integration.md](references/gui-integration.md) — Connecting models to PyQt5 actions