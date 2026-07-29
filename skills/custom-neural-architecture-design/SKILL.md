---
name: custom-neural-architecture-design
description: "Use when designing custom neural network architectures."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [neural-networks, architecture, design, deep-learning, pytorch]
    related_skills: [neural-network-fundamentals, transformer-architectures, attention-mechanisms-deep, state-space-models-mamba, custom-training-loops]
---

# Custom Neural Architecture Design

Systematic process for designing novel neural network architectures from scratch — from conceptual design to implementation, with reusable patterns and building blocks.

## When to Use

- Existing architectures (transformer, CNN, RNN) don't fit your problem's constraints
- You need to design a novel combination of existing building blocks
- You want to optimize architecture for specific efficiency/quality tradeoffs
- Building models for non-standard data types or modalities
- Researching new architectural innovations

## Architecture Design Process

### Phase 1: Problem Analysis

```python
# Answer these questions before designing:
constraints = {
    "data_type": "time-series | images | text | graph | multi-modal",
    "input_shape": (batch, channels, height, width) or (batch, seq_len, dim),
    "output_type": "classification | regression | generation | embedding",
    "latency_budget_ms": 50,
    "memory_budget_mb": 1024,
    "param_budget": int(1e7),  # 10M parameters
    "training_data_size": 100000,
    "deployment": "mobile | server | edge | browser"
}
```

### Phase 2: Building Block Selection

Choose from these composable blocks:

```python
# Core building blocks for any architecture
BLOCKS = {
    "linear":          nn.Linear,          # Fully connected
    "conv1d":          nn.Conv1d,          # 1D convolution
    "conv2d":          nn.Conv2d,          # 2D convolution
    "depthwise_conv":  nn.Conv2d(groups=in_channels),  # Depthwise
    "separable_conv":  SeparableConv2d,     # Depthwise + pointwise
    "transformer_enc": TransformerEncoder,  # Self-attention + FFN
    "transformer_dec": TransformerDecoder,  # Cross-attention + self-attention
    "lstm":            nn.LSTM,             # LSTM cell
    "gru":             nn.GRU,             # GRU cell
    "mamba_block":     MambaBlock,          # State space model block
    "mlp_mixer":       MLPMixerBlock,       # Channel + spatial mixing
    "convnext_block":  ConvNeXtBlock,       # Modern conv block
    "resnet_block":    ResNetBlock,         # Residual connection
    "dense_block":     DenseBlock,          # Dense connectivity
    "attention_pool":  AttentionPooling,    # Attention-based pooling
    "cross_attention": CrossAttention,       # Cross-modal attention
}
```

### Phase 3: Architecture Template

Use pre-built patterns for common architecture families:

**CNN Backbone + Transformer Head (Hybrid Vision)**

```python
class HybridVisionModel(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_chans=3,
                 embed_dim=768, depth=12, num_heads=12):
        super().__init__()
        # Stage 1: CNN stem for efficient early processing
        self.stem = nn.Sequential(
            nn.Conv2d(in_chans, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.GELU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.GELU(),
        )
        
        # Stage 2: Patch embed + positional encoding
        self.patch_embed = nn.Conv2d(128, embed_dim, kernel_size=patch_size//4, stride=patch_size//4)
        num_patches = (img_size // patch_size) ** 2
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches, embed_dim))
        
        # Stage 3: Transformer blocks
        self.blocks = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads) for _ in range(depth)
        ])
        
        # Stage 4: Head
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, num_classes)
    
    def forward(self, x):
        x = self.stem(x)
        x = self.patch_embed(x)
        x = x.flatten(2).transpose(1, 2)
        x = x + self.pos_embed
        for block in self.blocks:
            x = block(x)
        x = self.norm(x).mean(dim=1)  # Global average pooling
        return self.head(x)
```

**Multi-Scale Feature Pyramid (Dense Prediction)**

```python
class FeaturePyramidNet(nn.Module):
    """Uses multiple scales with top-down pathway."""
    def __init__(self, encoder_channels=[256, 512, 1024, 2048],
                 fpn_dim=256):
        super().__init__()
        # Lateral connections (1x1 convs)
        self.laterals = nn.ModuleList([
            nn.Conv2d(c, fpn_dim, 1) for c in encoder_channels
        ])
        # Top-down pathway (upsample + sum)
        self.topdowns = nn.ModuleList([
            nn.Conv2d(fpn_dim, fpn_dim, 3, padding=1) for _ in range(len(encoder_channels)-1)
        ])
    
    def forward(self, features):
        # features: list of multi-scale feature maps [P2, P3, P4, P5]
        laterals = [l(f) for l, f in zip(self.laterals, features)]
        
        # Top-down pathway
        outs = [laterals[-1]]
        for i in range(len(laterals)-2, -1, -1):
            up = F.interpolate(outs[0], size=laterals[i].shape[-2:], mode='nearest')
            merged = laterals[i] + up
            outs.insert(0, self.topdowns[i](merged))
        return outs
```

**Mixture of Experts (Sparse MoE Layer)**

```python
class SparseMoELayer(nn.Module):
    """Sparse mixture of experts with top-k routing."""
    def __init__(self, dim, num_experts=8, top_k=2, hidden_dim=512):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.gate = nn.Linear(dim, num_experts)
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(dim, hidden_dim),
                nn.GELU(),
                nn.Linear(hidden_dim, dim)
            ) for _ in range(num_experts)
        ]
    
    def forward(self, x):
        # x shape: (batch, seq, dim)
        gate_logits = self.gate(x)  # (batch, seq, num_experts)
        weights, indices = torch.topk(gate_logits, self.top_k, dim=-1)
        weights = F.softmax(weights, dim=-1)
        
        # Dispatch to experts
        output = torch.zeros_like(x)
        for b in range(x.shape[0]):
            for s in range(x.shape[1]):
                for k in range(self.top_k):
                    expert_idx = indices[b, s, k]
                    output[b, s] += weights[b, s, k] * self.experts[expert_idx](x[b, s].unsqueeze(0)).squeeze(0)
        return output
```

## Design Patterns by Use Case

| Use Case | Recommended Pattern | Key Advantage |
|----------|-------------------|---------------|
| Image classification | ConvNeXt + global pooling | Simple, well-understood |
| Object detection | FPN backbone + DETR head | End-to-end, no NMS |
| Language modeling | Transformer + MoE | Scales parameters without compute |
| Time series forecasting | Mamba + temporal convolution | Efficient long-range dependencies |
| Multi-modal (V+L) | Cross-attention encoder | Flexible modality fusion |
| Graph data | GNN + attention pooling | Relational reasoning |
| Protein structure | Equivariant transformer | Physics-aware |
| Audio generation | Diffusion + U-Net | High quality, iterative refinement |
| Video | 3D Conv + temporal transformer | Spatiotemporal modeling |

## Efficiency Optimization Patterns

**Pattern 1: Efficient Attention**
```python
def linear_attention(Q, K, V):
    """O(n) attention via kernel trick instead of O(n²)."""
    Q = F.elu(Q) + 1
    K = F.elu(K) + 1
    KV = torch.einsum("bnd,bne->bde", K, V)
    K_sum = K.sum(dim=1)
    attn = (torch.einsum("bnd,bde->bne", Q, KV)) / (torch.einsum("bnd,bd->bn", Q, K_sum).unsqueeze(-1) + 1e-6)
    return attn
```

**Pattern 2: Depthwise Separable Convolution**
```python
class SeparableConv2d(nn.Module):
    """Reduces params vs regular conv by ~groups factor."""
    def __init__(self, in_c, out_c, kernel_size, padding=0):
        super().__init__()
        self.depthwise = nn.Conv2d(in_c, in_c, kernel_size, 
                                     padding=padding, groups=in_c)
        self.pointwise = nn.Conv2d(in_c, out_c, 1)
```

**Pattern 3: Weight Tying**
```python
def weight_tying(layers):
    """Share weights across all layers. Saves memory, smooths gradients."""
    shared_block = TransformerBlock(dim=512, heads=8)
    return nn.ModuleList([shared_block for _ in range(12)])
```

## Common Pitfalls

1. **No ablation studies** — adding multiple innovations at once makes it impossible to know what worked
2. **Gradient path issues** — vanishing/exploding gradients from poor skip-connection design
3. **Normalization placement** — Pre-norm vs post-norm matters; pre-norm is more stable for deep nets
4. **Initialization sensitivity** — novel blocks need custom init; use `kaiming_uniform` or `xavier` as baseline
5. **Memory blind spots** — activation memory grows linearly with depth; use checkpointing or gradient accumulation
6. **Over-engineering** — start simple, add complexity only when baseline shows room for improvement

## Verification Checklist

- [ ] Architecture designed from problem constraints, not copied
- [ ] Each building block justified by ablation or prior work
- [ ] Parameter count within budget
- [ ] Computational cost (FLOPs) profiled
- [ ] Memory usage (activations + weights) within budget
- [ ] Gradient flow verified (gradient norm histogram)
- [ ] Forward pass runs without shape errors
- [ ] Backward pass completes without NaNs
- [ ] Training dynamics stable (loss decreases reliably)
- [ ] Baseline comparison shows architecture improvement

## See Also

- neural-network-fundamentals — core neural network concepts
- transformer-architectures — transformer design patterns
- attention-mechanisms-deep — advanced attention variants
- state-space-models-mamba — SSM alternatives to attention
- custom-training-loops — training custom architectures
