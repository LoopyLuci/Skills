---
name: graph-neural-networks
description: "Use when implementing GNNs for graph-structured data."
category: mlops
tags: [gnn, graph-neural-networks, message-passing, gcn, gat]
---
# Graph Neural Networks

Building and training GNNs for graph-structured data.

## Message Passing Framework

```
h_v^(l+1) = UPDATE(h_v^l, AGGREGATE({h_u^l : u ∈ N(v)}))
```

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MessagePassingLayer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.msg_fn = nn.Linear(2 * in_dim, out_dim)  # message from u→v
        self.update_fn = nn.Linear(in_dim + out_dim, out_dim)

    def forward(self, h, edge_index):
        # h: (N, F), edge_index: (2, E)
        src, dst = edge_index
        messages = self.msg_fn(torch.cat([h[src], h[dst]], dim=-1))
        # Aggregate: sum messages per node
        aggr = torch.zeros_like(h)
        aggr.index_add_(0, dst, messages)
        # Update
        return F.relu(self.update_fn(torch.cat([h, aggr], dim=-1)))
```

## GCN (Graph Convolutional Network)

```python
class GCNLayer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.weight = nn.Linear(in_dim, out_dim)

    def forward(self, h, adj_norm):
        # adj_norm: normalized adjacency D^{-1/2} A D^{-1/2}
        h = self.weight(h)
        return F.relu(adj_norm @ h)

class GCN(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.conv1 = GCNLayer(in_dim, hidden_dim)
        self.conv2 = GCNLayer(hidden_dim, out_dim)

    def forward(self, h, adj_norm):
        h = self.conv1(h, adj_norm)
        h = F.dropout(h, 0.5, training=self.training)
        h = self.conv2(h, adj_norm)
        return F.log_softmax(h, dim=-1)
```

## GAT (Graph Attention Networks)

```python
class GATLayer(nn.Module):
    def __init__(self, in_dim, out_dim, n_heads=8):
        super().__init__()
        self.w = nn.Linear(in_dim, out_dim * n_heads)
        self.a = nn.Parameter(torch.randn(1, n_heads, 2 * out_dim))
        self.n_heads = n_heads

    def forward(self, h, edge_index):
        src, dst = edge_index
        h = self.w(h).view(-1, self.n_heads, h.shape[-1])
        # Compute attention scores
        e = F.leaky_relu(
            (self.a @ torch.cat([h[src], h[dst]], dim=-1).unsqueeze(-1)).squeeze(-1),
            negative_slope=0.2
        )
        # Softmax per node
        attn = F.softmax(e, dim=0)
        # Weighted sum
        return (attn.unsqueeze(-1) * h[src]).sum(dim=0)
```

## Graph-Level Tasks

```python
# Node classification: predict label per node
# Link prediction: predict edge existence
# Graph classification: predict label per graph

# Graph readout for graph classification
def global_mean_pool(h, batch):
    # h: (N, F), batch: (N,) — which graph each node belongs to
    return torch_scatter.scatter_mean(h, batch, dim=0)
```

## Pitfalls

- Message passing is O(E) — dense graphs are expensive
- Over-smoothing: many layers → all node embeddings become similar
- GCN assumes undirected graphs — directed needs separate src/dst weights
- GAT computes attention for each edge — expensive for large graphs
- Negative sampling needed for link prediction (sample non-edges)
