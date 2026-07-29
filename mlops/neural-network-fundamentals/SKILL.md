---
name: neural-network-fundamentals
description: "Use when designing neural network architectures."
category: mlops
tags: [neural-networks, deep-learning, architecture, layers]
---
# Neural Network Fundamentals

Core neural network concepts: layers, backpropagation, architectures.

## Core Components

```python
import torch
import torch.nn as nn

# Perceptron: y = σ(Wx + b)
linear = nn.Linear(768, 10)  # W.shape=(10,768), b.shape=(10,)

# Forward pass
x = torch.randn(32, 768)     # batch_size=32
output = linear(x)            # (32, 10)
```

## Layer Types

```python
# Dense / Linear
nn.Linear(in_features=768, out_features=1024)

# Convolutional (2D for images)
nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, stride=1, padding=1)

# Recurrent
nn.RNN(input_size=512, hidden_size=256, num_layers=2, batch_first=True)
nn.LSTM(input_size=512, hidden_size=256, num_layers=2, batch_first=True)
nn.GRU(input_size=512, hidden_size=256, num_layers=2, batch_first=True)

# Attention
nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)

# Normalization
nn.BatchNorm1d(256)
nn.LayerNorm(768)

# Pooling
nn.MaxPool2d(kernel_size=2)
nn.AvgPool2d(kernel_size=2)
nn.AdaptiveAvgPool2d((1, 1))

# Dropout
nn.Dropout(p=0.1)
nn.Dropout2d(p=0.2)
```

## Forward & Backward

```python
class SimpleMLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.GELU(),
            nn.Linear(hidden_dim // 2, output_dim),
        )

    def forward(self, x):
        return self.net(x)

model = SimpleMLP(768, 1024, 10)
x = torch.randn(32, 768)
y = model(x)                 # forward: (32, 10)
loss = y.sum()
loss.backward()              # backward: computes gradients
```

## Common Activation Functions

```python
nn.ReLU()          # max(0, x) — default, dead neurons possible
nn.GELU()          # x * Φ(x) — smooth, used in transformers
nn.SiLU() / nn.Swish()  # x * σ(x) — self-gated
nn.Tanh()          # [-1, 1] — RNNs
nn.Sigmoid()       # [0, 1] — binary classification output
nn.Softmax(dim=-1) # probability distribution — classification
```

## Loss Functions

```python
nn.CrossEntropyLoss()         # classification
nn.BCEWithLogitsLoss()        # binary classification
nn.MSELoss()                  # regression
nn.L1Loss()                   # MAE regression
nn.KLDivLoss()                # distribution divergence
nn.CosineEmbeddingLoss()      # similarity learning
```

## Pitfalls

- Gradient vanishing: ReLU + residual connections + proper init
- Gradient exploding: gradient clipping (`nn.utils.clip_grad_norm_`)
- Dead ReLU: use LeakyReLU or GELU for negative region
- BatchNorm behavior differs between train and eval mode
- Softmax + CrossEntropy numerically unstable — use `CrossEntropyLoss` (combines both)
