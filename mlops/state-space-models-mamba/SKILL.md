---
name: state-space-models-mamba
description: "Use when building state space models like Mamba and S4."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ssm, state-space, mamba, s4, sequence-models, pytorch]
    related_skills: [transformer-architectures, attention-mechanisms-deep, custom-neural-architecture-design, neural-network-fundamentals]
---

# State Space Models — Mamba, S4, and Beyond

Designing and implementing state space model (SSM) architectures for sequence modeling — structured state spaces (S4), Mamba (S6), and their variants as alternatives to transformers for efficient long-range dependency modeling.

## When to Use

- Processing long sequences (10K+ tokens) where self-attention's O(n²) cost is prohibitive
- Tasks requiring linear or near-linear scaling with sequence length
- Continuous-time signals (audio, sensor data, physical simulations)
- Building efficient alternatives to transformers for edge/latency-sensitive deployment
- Researching new sequence model architectures

## SSM Fundamentals

### Continuous State Space Model

```python
# A continuous SSM maps input u(t) to output y(t) via hidden state x(t):
# x'(t) = A @ x(t) + B @ u(t)
# y(t)  = C @ x(t) + D @ u(t)
# A: state transition (N x N), B: input projection (N x 1), C: output projection (1 x N)
```

### Discretization (for digital computation)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

def discretize(A, B, delta):
    """Discretize continuous SSM parameters using zero-order hold.
    A_bar = exp(delta * A)
    B_bar = (exp(delta * A) - I) @ inv(A) @ B ≈ delta * B  (first-order approx)
    """
    A_bar = torch.matrix_exp(delta.unsqueeze(-1) * A)
    B_bar = delta.unsqueeze(-1) * B  # First-order approximation
    return A_bar, B_bar
```

## S4 (Structured State Space)

The Structured State Space (S4) uses HiPPO initialization for long-range memory:

```python
class S4Block(nn.Module):
    """S4 layer: structured state space with HiPPO initialization.
    Handles long-range dependencies (up to 16K tokens)."""
    
    def __init__(self, d_model, d_state=64, l_max=4096):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        
        # HiPPO-LegS matrix: captures long-range memory structure
        self._init_hippo()
        
        # Parametrized input/output projections
        self.B = nn.Parameter(torch.randn(d_model, d_state) / d_state**0.5)
        self.C = nn.Parameter(torch.randn(d_model, d_state) / d_state**0.5)
        self.D = nn.Parameter(torch.ones(d_model))
        self.delta = nn.Parameter(torch.log(torch.rand(d_model)))  # log-delta
        
        # Output projection
        self.out_proj = nn.Linear(d_model, d_model)
        self.act = nn.GELU()
    
    def _init_hippo(self):
        """Initialize A matrix with HiPPO-LegS (Structured State Space)."""
        N = self.d_state
        # HiPPO matrix: A[n,k] = -0.5 if n>k, 0.5 if n<k, -[0.5 if n==k]
        A = torch.zeros(N, N)
        for n in range(N):
            for k in range(N):
                if n > k:
                    A[n, k] = 1.0
                elif n == k:
                    A[n, k] = 0.5
        A = -A  # Normalized low-rank structure
        # Normal plus low-rank decomposition
        self.A_normal = nn.Parameter(torch.diag(torch.linspace(0.5, N+0.5, N)))
        self.A_low_rank = nn.Parameter(A - torch.diag(torch.diag(A)))
    
    def forward(self, u):
        """
        u: (batch, seq_len, d_model)
        Returns: (batch, seq_len, d_model)
        """
        batch, seq_len, _ = u.shape
        
        # Global convolution mode (parallel during training)
        # Uses FFT convolution for O(L log L) instead of O(L²) recurrence
        A = self.A_normal + self.A_low_rank  # Reconstruct A
        delta = F.softplus(self.delta)  # Ensure positive
        
        # Discretize
        A_bar, B_bar = discretize(A, self.B, delta)
        
        # Compute SSM kernel (convolutional representation)
        kernel = self._compute_kernel(A_bar, B_bar, seq_len)
        
        # Global convolution via FFT
        y = self._fft_convolution(u, kernel)
        
        # Residual connection + gating
        y = self.act(self.out_proj(y))
        return y + u  # Skip connection
    
    def _compute_kernel(self, A_bar, B_bar, L):
        """K = (C B, C A B, C A² B, ..., C A^L-1 B)"""
        kernel = torch.zeros(L, self.d_model, device=A_bar.device)
        power = torch.eye(self.d_state, device=A_bar.device)
        for t in range(L):
            kernel[t] = (self.C @ power @ B_bar).sum(-1)
            power = A_bar @ power
        return kernel
    
    def _fft_convolution(self, u, kernel):
        """Convolution via FFT: O(L log L)."""
        u_fft = torch.fft.fft(u.transpose(1, 2), n=2*u.shape[1])
        k_fft = torch.fft.fft(kernel.unsqueeze(0).transpose(1, 2), n=2*u.shape[1])
        y = torch.fft.ifft(u_fft * k_fft, n=2*u.shape[1]).real
        return y[:, :, :u.shape[1]].transpose(1, 2)
```

## Mamba (S6 — Selective State Space)

Mamba improves S4 with input-dependent (selective) state transitions:

```python
class MambaBlock(nn.Module):
    """Mamba: Selective state space model with input-dependent dynamics.
    O(n) inference, parallel training, matches transformer quality."""
    
    def __init__(self, d_model, d_state=16, expand_factor=2, d_conv=4):
        super().__init__()
        self.d_model = d_model
        self.d_inner = d_model * expand_factor
        self.d_state = d_state
        
        # Input projection
        self.in_proj = nn.Linear(d_model, self.d_inner * 2, bias=False)
        
        # Convolution + activation before SSM
        self.conv1d = nn.Conv1d(
            in_channels=self.d_inner,
            out_channels=self.d_inner,
            kernel_size=d_conv,
            padding=d_conv - 1,
            groups=self.d_inner,  # Depthwise
            bias=False
        )
        
        # Selective parameters (input-dependent)
        # These make Mamba "selective" — filtering based on content
        self.x_proj = nn.Linear(self.d_inner, d_state * 3, bias=False)  # delta, B, C
        self.dt_proj = nn.Linear(d_state, self.d_inner, bias=True)
        
        # Output projection
        self.out_proj = nn.Linear(self.d_inner, d_model, bias=False)
        
        # Initialize A as log-uniform
        A_log = torch.log(torch.arange(1, d_state + 1, dtype=torch.float32))
        self.A_log = nn.Parameter(A_log)
        self.D = nn.Parameter(torch.ones(self.d_inner))
    
    def forward(self, x):
        """
        x: (batch, seq_len, d_model)
        """
        batch, seq_len, _ = x.shape
        
        # Input projection + activation
        x_and_res = self.in_proj(x)
        x, res = x_and_r.chunk(2, dim=-1)
        x = F.silu(x)
        
        # 1D convolution (depthwise)
        x_conv = x.transpose(1, 2)  # (batch, d_inner, seq_len)
        x_conv = self.conv1d(x_conv)[:, :, :seq_len]
        x = F.silu(x_conv.transpose(1, 2))
        
        # Selective SSM parameters (input-dependent!)
        # This is the key innovation: A, B, C, delta depend on input
        delta_BC = self.x_proj(x)  # (batch, seq_len, d_state*3)
        delta, B, C = delta_BC.split([self.d_state, self.d_state, self.d_state], dim=-1)
        
        delta = F.softplus(self.dt_proj(delta))  # (batch, seq_len, d_inner)
        
        # Selective SSM (recurrent scan)
        y = self._selective_scan(x, delta, B, C)
        
        # Gated residual
        y = y * res
        return self.out_proj(y)
    
    def _selective_scan(self, u, delta, B, C):
        """
        Selective scan: O(n) sequential during inference.
        For training, uses parallel associative scan.
        """
        batch, seq_len, d_inner = u.shape
        d_state = B.shape[-1]
        
        # A from log-uniform init (negative ensures stability)
        A = -torch.exp(self.A_log.float())  # (d_state,)
        
        # Discretize with selective delta
        delta_A = torch.exp(delta.unsqueeze(-1) * A)  # (batch, seq_len, d_inner, d_state)
        delta_B = delta.unsqueeze(-1) * B.unsqueeze(2)  # (batch, seq_len, d_inner, d_state)
        
        # Recurrent scan
        h = torch.zeros(batch, d_inner, d_state, device=u.device)
        outputs = []
        for t in range(seq_len):
            h = delta_A[:, t] * h + delta_B[:, t] * u[:, t].unsqueeze(-1)
            y_t = (h @ C[:, t].unsqueeze(-1)).squeeze(-1)
            outputs.append(y_t + self.D * u[:, t])
        
        return torch.stack(outputs, dim=1)
    
    def step(self, x, state=None):
        """Inference mode: single step with state caching. O(1) per step."""
        # Same as forward but processes one token at a time
        # Caches state between steps for efficient autoregressive generation
        pass
```

## Mamba Architecture

```python
class MambaLanguageModel(nn.Module):
    """Full Mamba architecture for language modeling.
    Stacks Mamba blocks with RMSNorm instead of LayerNorm."""
    
    def __init__(self, vocab_size=32000, d_model=2560, n_layers=32, 
                 d_state=16, expand_factor=2):
        super().__init__()
        
        self.embedding = nn.Embedding(vocab_size, d_model)
        
        self.layers = nn.ModuleList([
            nn.ModuleDict({
                'norm': RMSNorm(d_model),
                'mamba': MambaBlock(d_model, d_state, expand_factor)
            })
            for _ in range(n_layers)
        ])
        
        self.final_norm = RMSNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)
        
        # Tie embeddings
        self.lm_head.weight = self.embedding.weight
    
    def forward(self, input_ids):
        x = self.embedding(input_ids)
        
        for layer in self.layers:
            x = x + layer['mamba'](layer['norm'](x))
        
        x = self.final_norm(x)
        return self.lm_head(x)
    
    def generate(self, input_ids, max_new_tokens=100):
        """Autoregressive generation with cached state."""
        for _ in range(max_new_tokens):
            logits = self(input_ids[:, -1:])
            next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            input_ids = torch.cat([input_ids, next_token], dim=-1)
        return input_ids


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization."""
    def __init__(self, dim, eps=1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.eps = eps
    
    def forward(self, x):
        rms = x.pow(2).mean(-1, keepdim=True).sqrt()
        return x / (rms + self.eps) * self.weight
```

## SSM Variants

| Model | State Transition | Selection | Key Innovation |
|-------|-----------------|-----------|----------------|
| S4 (2021) | HiPPO + DPLR | No | Structured initialization for long-range memory |
| S4D (2022) | Diagonal | No | Simplified diagonal parameterization |
| DSS (2022) | Diagonal | No | Explicit diagonalization |
| S5 (2022) | Multi-input Multi-output | No | Parallel scan, MIMO generalization |
| Mega (2022) | Simplified EMA | Yes | Exponential moving average + attention |
| Mamba (S6, 2023) | Selective | Yes | Input-dependent state transitions + hardware-efficient scan |
| Jamba (2024) | Hybrid Mamba-Attention | Yes | Interleaved Mamba + attention layers + MoE |

## SSM vs Transformer

| Aspect | Transformer | SSM (Mamba) |
|--------|-------------|-------------|
| Complexity | O(n²) | O(n) |
| Long-range (16K+) | Prohibitive cost | Efficient |
| Autoregressive generation | O(n²) KV-cache | O(1) state |
| Hardware efficiency | Attention compute-bound | Scan memory-bound |
| In-context learning | Strong | Weaker |
| Quality (equiparameter) | Slightly better | Competitive |
| Training stability | Well-studied | More sensitive |

## Hardware-Efficient Scan (for Training)

```python
# Mamba's training efficiency comes from the parallel associative scan
# (not sequential like inference). Key insight:
# The recurrence is a linear operation (no nonlinearities),
# so it can be parallelized with scan/prefix-sum algorithms.

def associate_scan(u, delta_A, delta_B):
    """Parallel associative scan using work-efficient algorithm.
    Complexity: O(L log L) parallel steps instead of O(L) sequential."""
    # Step 1: Up-sweep (bottom-up)
    for stride in [1, 2, 4, 8, ...]:
        for i in range(0, L, stride*2):
            u[i+stride] = delta_A[i+stride] * u[i+stride] + delta_B[i+stride] * u[i]
    
    # Step 2: Down-sweep (top-down)
    ...
```

## Common Pitfalls

1. **Numerical stability** — SSMs can amplify numerical errors over long sequences; double-check discretization
2. **Initialization sensitivity** — Mamba is more sensitive to init than transformers; use provided init recipes
3. **Hardware utilization** — SSMs are memory-bound, not compute-bound; optimize for memory bandwidth
4. **Attention-free blind spot** — pure SSMs can struggle at tasks needing content-based retrieval; hybrid Mamba-Attention helps
5. **Autoregressive mode mismatch** — training uses parallel scan, inference uses recurrent; ensure state equivalence
6. **Normalization choice** — RMSNorm works better than LayerNorm for SSMs

## Verification Checklist

- [ ] Recurrence numerically stable for sequence length up to max expected
- [ ] Parallel scan forward matches sequential forward (numerical tolerance 1e-5)
- [ ] Inference state caching works correctly across multiple steps
- [ ] Gradient flows through discretization (check grad on delta parameter)
- [ ] Training loss matches reference implementation on small task
- [ ] Memory efficient: peak memory < O(n²) baseline for long sequences
- [ ] Throughput measured: tokens/second vs equivalent transformer

## See Also

- transformer-architectures — the alternative to SSMs
- attention-mechanisms-deep — attention that SSMs can replace
- custom-neural-architecture-design — architecture design patterns
