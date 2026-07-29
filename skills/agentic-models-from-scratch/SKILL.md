---
name: agentic-models-from-scratch
description: "Use when building custom agentic AI models from scratch."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, agentic, foundation-model, architecture, training]
    related_skills: [custom-neural-architecture-design, agent-framework-design, tool-augmented-models-training, rlhf-implementation-guide, agent-reasoning-patterns]
---

# Building Agentic Models from Scratch

Designing and training neural network architectures specifically for agentic behavior — models that can reason, use tools, maintain state, and interact with environments autonomously.

## When to Use

- Building a foundation model architecture optimized for agentic tasks (tool use, planning, multi-turn)
- Researching new architectures for agentic AI
- Designing models where agent capability (reasoning, tool-calling, state-tracking) is the primary goal
- Creating models that natively support function calling without fine-tuning
- Building small, efficient agentic models for edge deployment

## Agentic Model Requirements

A model designed for agentic behavior needs distinct capabilities beyond standard language modeling:

```
1. State tracking — maintain conversation and environment state
2. Tool awareness — understand available tools and their schemas
3. Action generation — produce structured tool calls
4. Observation integration — incorporate tool outputs
5. Planning — decompose tasks and track sub-task progress
6. Self-reflection — evaluate own outputs and correct errors
```

## Architecture Blueprints

### Blueprint 1: Tool-Augmented Transformer

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ToolAugmentedTransformer(nn.Module):
    """Transformer with native tool-calling capabilities.
    
    Key architectural differences from standard LLMs:
    1. Tool registry embeddings — tools embedded as tokens/virtual tokens
    2. Action head — separate head for structured tool call generation
    3. Observation integration — special tokens for interleaving I/O
    4. State cache — persistent state across turns
    """
    
    def __init__(self, vocab_size=32000, d_model=2048, n_layers=24,
                 n_heads=16, max_tools=128, tool_embed_dim=128):
        super().__init__()
        self.d_model = d_model
        
        # Standard transformer components
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.pos_embedding = nn.Embedding(4096, d_model)
        
        # Tool-aware components
        self.tool_embedding = nn.Embedding(max_tools, tool_embed_dim)
        self.tool_projection = nn.Linear(tool_embed_dim, d_model)
        
        # Special tokens for tool interaction
        self.special_tokens = {
            'tool_call': 32000,     # <tool_call>
            'tool_output': 32001,   # <tool_output>
            'observation': 32002,   # <observation>
            'think_start': 32003,   # <think>
            'think_end': 32004,     # </think>
        }
        
        # Transformer layers
        self.layers = nn.ModuleList([
            TransformerLayer(d_model, n_heads) for _ in range(n_layers)
        ])
        
        # Agent-specific heads
        self.action_head = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.Linear(d_model, d_model)  # Projects to tool-call space
        )
        
        self.state_head = nn.Linear(d_model, d_model)  # For state tracking
        
        self.lm_head = nn.Linear(d_model, vocab_size)
    
    def forward(self, input_ids, tool_ids=None, attention_mask=None):
        """
        input_ids: (batch, seq) with interleaved text, tool calls, observations
        tool_ids: (batch, seq) tool index for tool-call positions, 0 elsewhere
        """
        # Token embeddings
        x = self.token_embedding(input_ids)
        
        # Add positional info
        positions = torch.arange(input_ids.shape[1], device=input_ids.device)
        x = x + self.pos_embedding(positions)
        
        # Add tool embeddings where applicable
        if tool_ids is not None:
            tool_emb = self.tool_embedding(tool_ids)
            tool_emb = self.tool_projection(tool_emb)
            x = x + tool_emb * (tool_ids > 0).unsqueeze(-1).float()
        
        # Pass through transformer layers
        for layer in self.layers:
            x = layer(x, attention_mask)
        
        # Agentic outputs
        logits = self.lm_head(x)
        action_features = self.action_head(x)  # For tool call generation
        
        return logits, action_features


class TransformerLayer(nn.Module):
    """Standard pre-norm transformer layer with GQA and RoPE."""
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Linear(d_model * 4, d_model)
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
    
    def forward(self, x, mask=None):
        x = x + self.attn(self.norm1(x), self.norm1(x), x, 
                          attn_mask=mask, need_weights=False)[0]
        x = x + self.ffn(self.norm2(x))
        return x
```

### Blueprint 2: Recurrent State-Space Agent Model

```python
class RecurrentAgentModel(nn.Module):
    """Agentic model with recurrent state for persistent memory.
    Combines Mamba-style SSM with tool-awareness.
    
    Key advantage: O(1) state per turn, no quadratic attention over history.
    """
    
    def __init__(self, vocab_size, d_model=1024, d_state=64, n_layers=16):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        
        # Mamba blocks for efficient sequence processing
        self.backbone = nn.ModuleList([
            MambaBlock(d_model, d_state) for _ in range(n_layers)
        ])
        
        # Agent state (updated at each turn end)
        self.state_projection = nn.Linear(d_model, d_state)
        self.state_norm = nn.LayerNorm(d_state)
        
        # Memory cross-attention (attends to compressed state)
        self.memory_attn = nn.MultiheadAttention(d_model, 8, batch_first=True)
        self.memory_proj = nn.Linear(d_state, d_model)
        
        self.lm_head = nn.Linear(d_model, vocab_size)
    
    def forward(self, input_ids, agent_state=None, return_state=False):
        x = self.embed(input_ids)
        
        # Inject memory into sequence
        if agent_state is not None:
            memory = self.memory_proj(agent_state).unsqueeze(1)
            x = x + self.memory_attn(x, memory, memory)[0]
        
        for block in self.backbone:
            x = block(x)
        
        logits = self.lm_head(x)
        
        if return_state:
            # Compress last hidden state into agent state
            new_state = self.state_norm(self.state_projection(x[:, -1]))
            return logits, new_state
        
        return logits
```

### Blueprint 3: Multi-Head Agent Architecture

```python
class MultiHeadAgent(nn.Module):
    """Agent with specialized heads for different agentic functions.
    
    Each head handles a different aspect of agentic behavior:
    - Reasoning head: chain-of-thought generation
    - Action head: tool call generation
    - Reflection head: self-evaluation
    - Memory head: state compression
    """
    
    def __init__(self, base_model, d_model=2048, num_tools=64):
        super().__init__()
        self.base_model = base_model  # Shared transformer backbone
        
        # Specialized heads (trained with different objectives)
        self.reasoning_head = nn.Linear(d_model, d_model)
        self.action_head = ActionHead(d_model, num_tools)
        self.reflection_head = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Linear(d_model // 2, 1)  # Confidence score
        )
        self.memory_head = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.Tanh()
        )
    
    def forward(self, input_ids, mode='generate', **kwargs):
        hidden = self.base_model(input_ids)
        
        if mode == 'reason':
            return self.reasoning_head(hidden)
        elif mode == 'act':
            return self.action_head(hidden)
        elif mode == 'reflect':
            return self.reflection_head(hidden[:, -1])
        elif mode == 'memorize':
            return self.memory_head(hidden[:, -1])


class ActionHead(nn.Module):
    """Generates structured tool calls.
    Outputs: (tool_id, parameters_start, parameters_end) tokens."""
    def __init__(self, d_model, num_tools):
        super().__init__()
        self.tool_selector = nn.Linear(d_model, num_tools)
        self.param_generator = nn.Linear(d_model, d_model)
    
    def forward(self, hidden):
        # Select tool
        tool_logits = self.tool_selector(hidden[:, -1])
        # Generate parameters (would be decoded as token sequence)
        param_features = self.param_generator(hidden)
        return tool_logits, param_features
```

## Training Agentic Models

```python
class AgenticModelTrainer:
    """Multi-objective training for agentic capabilities."""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def train_step(self, batch, objective='all'):
        losses = {}
        
        # 1. Language modeling loss (standard next-token prediction)
        if objective in ('lm', 'all'):
            logits = self.model(batch['input_ids'])
            losses['lm'] = F.cross_entropy(
                logits.view(-1, logits.size(-1)),
                batch['labels'].view(-1)
            )
        
        # 2. Tool call loss (predict tool call tokens)
        if objective in ('tool', 'all'):
            tool_logits = self.model(batch['input_ids'], mode='act')
            losses['tool'] = self.tool_call_loss(
                tool_logits, batch['tool_labels']
            )
        
        # 3. Reflection loss (predict whether tool call succeeded)
        if objective in ('reflect', 'all'):
            confidence = self.model(batch['input_ids'], mode='reflect')
            losses['reflect'] = F.binary_cross_entropy_with_logits(
                confidence, batch['tool_success']
            )
        
        # 4. State consistency loss (contrastive between turns)
        if objective in ('state', 'all'):
            _, state1 = self.model(batch['turn1'], return_state=True)
            _, state2 = self.model(batch['turn2'], return_state=True)
            # Contrastive: same context = close, different = far
            losses['state'] = self.contrastive_loss(state1, state2, batch['same_context'])
        
        # Weighted combination
        total_loss = sum(losses.values())
        return total_loss, losses
```

## Common Pitfalls

1. **Overfitting to tool patterns** — model memorizes tool calls without understanding; use diverse tool schemas
2. **Action vs. reasoning imbalance** — one head dominates; balance loss weights carefully
3. **State collapse** — recurrent state loses information; use gating mechanisms (like LSTM forget gates)
4. **Catastrophic forgetting of language** — adding agentic heads degrades core LM performance; mix SFT data
5. **Tool embedding saturation** — too few tool embeddings limit scaling; use dynamic tool representations
6. **Multi-head interference** — heads interfere during shared backbone training; use adversarial or orthogonal regularization

## Verification Checklist

- [ ] Model generates valid tool calls (parsable JSON/structured format)
- [ ] Model correctly integrates tool outputs into subsequent reasoning
- [ ] State maintained correctly across turns (test with 5+ turn conversations)
- [ ] Reflection head prediction correlates with actual tool success
- [ ] Language modeling loss doesn't regress compared to base model
- [ ] Model can learn new tools (not just memorized ones)
- [ ] Inference latency acceptable for interactive use

## See Also

- agent-framework-design — wrapping models in agent frameworks
- tool-augmented-models-training — training models to use tools
- rlhf-implementation-guide — aligning agentic models
- agent-reasoning-patterns — reasoning patterns for agents
- custom-neural-architecture-design — custom architecture patterns
