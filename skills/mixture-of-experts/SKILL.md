---
name: mixture-of-experts
description: "Use when implementing MoE architectures for sparse models."
category: mlops
tags: [mixture-of-experts, moe, sparse, routing, scaling]
---
# Mixture of Experts (MoE)

Implementing sparse MoE architectures for scaling models efficiently.

## Architecture

```
Input → Router → Softmax → Top-k Selection
              ↘                ↓
         [Expert 1] [Expert 2] ... [Expert N]
              ↓                ↓
         Weighted sum → Output
```

## MoE Layer Implementation

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MoELayer(nn.Module):
    def __init__(self, d_model, d_ff, num_experts=8, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(d_model, num_experts, bias=False)

        # Expert FFNs
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.GELU(),
                nn.Linear(d_ff, d_model),
            ) for _ in range(num_experts)
        ])

    def forward(self, x):
        # x: (batch, seq, d_model)
        B, S, D = x.shape

        # Routing weights
        routing_logits = self.router(x)  # (B, S, E)
        routing_weights = F.softmax(routing_logits, dim=-1)

        # Top-k routing
        top_k_weights, top_k_indices = torch.topk(routing_weights, self.top_k, dim=-1)
        top_k_weights = top_k_weights / top_k_weights.sum(dim=-1, keepdim=True)

        # Sparse computation
        output = torch.zeros_like(x)
        for i, expert in enumerate(self.experts):
            # Create mask for tokens routed to this expert
            mask = (top_k_indices == i).any(dim=-1)  # (B, S)
            if mask.any():
                batch_indices, seq_indices = mask.nonzero(as_tuple=True)
                expert_input = x[batch_indices, seq_indices]
                expert_output = expert(expert_input)

                # Weight by routing probability
                weight_mask = top_k_weights[batch_indices, seq_indices, (top_k_indices[batch_indices, seq_indices] == i)]
                expert_output = expert_output * weight_mask.unsqueeze(-1)

                output[batch_indices, seq_indices] += expert_output

        return output
```

## Auxiliary Load Balancing Loss

```python
def load_balancing_loss(routing_logits, num_experts, top_k):
    """Encourage uniform expert utilization."""
    routing_probs = F.softmax(routing_logits, dim=-1)

    # Fraction of tokens routed to each expert
    tokens_per_expert = routing_probs.mean(dim=(0, 1))  # (E,)

    # Average routing probability per expert
    avg_prob = routing_probs.mean(dim=(0, 1))  # (E,)

    # Load balancing loss (CV = 0 for uniform)
    loss = num_experts * (tokens_per_expert * avg_prob).sum()
    return loss
```

## Expert Parallelism

```python
# For distributed training: each GPU hosts a subset of experts
# Tokens with expert i → GPU i (all-to-all communication)

# DeepSpeed MoE: automatic expert parallelism
# from deepspeed.moe.layer import MoE
# model = MoE(hidden_size, expert):
#     name="deepspeed",
#     ...expert=nn.Module,
#     num_experts=config.num_experts,
#     top_k=config.top_k,
# )
```

## Pitfalls

- Load imbalance: some experts get most tokens — add load balancing loss
- All-to-all communication is expensive for expert parallelism
- Larger expert count improves capacity but adds communication overhead
- Top-k=2 is common (Mistral 8x7B, Mixtral) — higher k increases compute
- Auxiliary loss weight should be small (0.01) to not interfere with main loss
- Capacity factor limits tokens per expert — tokens exceeding capacity are dropped
