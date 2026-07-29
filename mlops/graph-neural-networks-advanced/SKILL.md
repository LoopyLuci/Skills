---
name: graph-neural-networks-advanced
description: "Use when implementing graph neural networks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GNN, graph-neural-networks, PyTorch-Geometric, GCN, GAT, message-passing]
    related_skills: [custom-neural-architecture-design, attention-mechanisms-deep, transformer-architectures, embedding-models-patterns]
---

# Graph Neural Networks

Implementing graph neural networks — from GCN and GAT through message passing, graph transformers, and applications in molecular, social, and knowledge graphs.

## When to Use

- Learning on graph-structured data (social networks, molecules, knowledge graphs)
- Node classification, link prediction, or graph classification
- Recommendation systems with graph structure
- Molecular property prediction or drug discovery

## GNN Implementation

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool

class GCN(nn.Module):
    """Graph Convolutional Network for node classification."""
    def __init__(self, in_channels: int, hidden: int, out_channels: int):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden)
        self.conv2 = GCNConv(hidden, hidden)
        self.conv3 = GCNConv(hidden, out_channels)
    
    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.2, training=self.training)
        x = F.relu(self.conv2(x, edge_index))
        x = self.conv3(x, edge_index)
        return F.log_softmax(x, dim=1)

class GraphTransformerLayer(nn.Module):
    """Graph Transformer with attention across nodes."""
    def __init__(self, dim: int, n_heads: int = 4):
        super().__init__()
        self.attention = nn.MultiheadAttention(dim, n_heads, batch_first=True)
        self.norm = nn.LayerNorm(dim)
        self.ffn = nn.Sequential(nn.Linear(dim, dim*4), nn.GELU(), nn.Linear(dim*4, dim))
    
    def forward(self, x, mask=None):
        attn_out, _ = self.attention(x, x, x, attn_mask=mask)
        x = self.norm(x + attn_out)
        return self.norm(x + self.ffn(x))
```

## Verification Checklist

- [ ] Graph representation defined (nodes, edges, features, adjacency)
- [ ] GNN architecture chosen (GCN, GAT, GraphSAGE, GIN, Graph Transformer)
- [ ] Message passing and aggregation functions defined
- [ ] Task type chosen (node classification, link prediction, graph classification)
- [ ] Data splits respect graph structure (no leakage)
- [ ] Scalability considered (mini-batching with NeighborLoader for large graphs)
- [ ] Over-smoothing addressed (skip connections, layer normalization)
