---
name: transformer-architectures
description: "Use when implementing transformer-based models."
category: mlops
tags: [transformer, attention, bert, gpt, pytorch]
---
# Transformer Architectures

Implementing transformer-based models: attention, self-attention, encoder-decoder.

## Scaled Dot-Product Attention

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ScaledDotProductAttention(nn.Module):
    def __init__(self, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

    def forward(self, query, key, value, mask=None):
        d_k = query.size(-1)
        scores = torch.matmul(query, key.transpose(-2, -1)) / d_k ** 0.5
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = self.dropout(F.softmax(scores, dim=-1))
        return torch.matmul(attn, value), attn
```

## Multi-Head Attention

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_k = d_model // n_heads
        self.n_heads = n_heads
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w_o = nn.Linear(d_model, d_model)
        self.attention = ScaledDotProductAttention(dropout)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        Q = self.w_q(query).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        K = self.w_k(key).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        V = self.w_v(value).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        attn_out, _ = self.attention(Q, K, V, mask)
        attn_out = attn_out.transpose(1, 2).contiguous().view(batch_size, -1, self.n_heads * self.d_k)
        return self.w_o(attn_out)
```

## Transformer Block

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, n_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x, mask=None):
        x = x + self.attention(self.norm1(x), self.norm1(x), self.norm1(x), mask)
        x = x + self.ffn(self.norm2(x))
        return x
```

## GPT-Style Decoder

```python
class GPTDecoder(nn.Module):
    def __init__(self, vocab_size: int, d_model: int, n_heads: int,
                 n_layers: int, d_ff: int, max_seq_len: int = 2048):
        super().__init__()
        self.token_embed = nn.Embedding(vocab_size, d_model)
        self.pos_embed = nn.Embedding(max_seq_len, d_model)
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, n_heads, d_ff) for _ in range(n_layers)
        ])
        self.norm = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size)

    def forward(self, tokens):
        seq_len = tokens.size(1)
        pos = torch.arange(seq_len, device=tokens.device).unsqueeze(0)
        x = self.token_embed(tokens) + self.pos_embed(pos)
        causal_mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool().to(tokens.device)
        for block in self.blocks:
            x = block(x, mask=causal_mask)
        return self.lm_head(self.norm(x))
```

## Pitfalls

- Attention is O(n²) — memory grows quadratically with sequence length
- Causal masking prevents attending to future tokens (decoder only)
- LayerNorm BEFORE or AFTER residual — both work, Pre-LN is more stable
- Rotary Position Embeddings (RoPE) — better than learned for extrapolation
- Flash Attention — use `F.scaled_dot_product_attention` for optimized GPU attention
