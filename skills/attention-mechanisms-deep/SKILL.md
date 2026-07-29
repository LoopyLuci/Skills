---
name: attention-mechanisms-deep
description: "Use when implementing advanced attention mechanisms."
category: mlops
tags: [attention, transformers, multi-head, flash-attention, sparse]
---
# Advanced Attention Mechanisms

Deep dive into attention variants beyond the original Transformer.

## Attention Variants

```python
# Linear Attention (O(n) instead of O(n²))
# Replace softmax(QK^T) with φ(Q)φ(K)^T where φ is a feature map
# Uses associative property: φ(Q)(φ(K)^T V)

# Flash Attention (memory-efficient, fused kernel)
# Uses tiling to avoid materializing the full attention matrix
# Supported via: F.scaled_dot_product_attention(q, k, v)

# Sparse Attention (attend to subset of positions)
# Patterns: sliding window, dilated, global, random

# Multi-Query Attention (MQA)
# Single K,V head, multiple Q heads
# Reduces memory, speeds up decoding

# Grouped Query Attention (GQA)
# Compromise between MHA and MQA
# Group heads, each group shares KV

# Sliding Window Attention
# Each token attends to w neighbors on each side
# Used in Mistral, Gemma: window_size=4096
```

## Flash Attention Usage

```python
import torch.nn.functional as F

# PyTorch 2.0+ built-in flash attention
out = F.scaled_dot_product_attention(
    query, key, value,
    attn_mask=mask,
    dropout_p=0.0,
    is_causal=True,  # causal mask for decoder
    scale=None,       # default: 1/sqrt(d_k)
)
```

## Positional Encodings

```python
# Absolute (original Transformer)
# RoPE (Rotary Position Embedding) — applies rotation to Q and K
# ALiBi — adds bias based on distance, no learned position
# Relative Position Bias — used in T5, Swin
# No Positional Encoding — used in some modern architectures

# RoPE implementation sketch
def apply_rotary(x, cos, sin):
    # x: (batch, n_heads, seq_len, d_k)
    # Interleave: x1, x2 → (-x2, x1) rotation
    half = x.shape[-1] // 2
    x_rot = torch.cat([-x[..., half:], x[..., :half]], dim=-1)
    return x * cos + x_rot * sin
```

## Efficient Attention for Long Sequences

```python
# Longformer: sliding window + global attention
# BigBird: sliding window + global + random
# Reformer: LSH (locality-sensitive hashing) attention
# Performer: FAVOR+ kernel approximation
# Routing Transformer: k-means clustering of keys

# Sparse attention mask
def create_sliding_window_mask(seq_len, window_size, device):
    mask = torch.zeros(seq_len, seq_len, device=device)
    for i in range(seq_len):
        start = max(0, i - window_size // 2)
        end = min(seq_len, i + window_size // 2 + 1)
        mask[i, start:end] = 1
    return mask
```

## Pitfalls

- Flash Attention requires CUDA compute capability 8.0+ (Ampere) for full speed
- MQA reduces quality slightly but is much faster for inference
- RoPE doesn't work well with ALiBi — choose one
- Linear attention often underperforms softmax on difficult tasks
- KV cache for long contexts uses significant GPU memory — use PagedAttention
