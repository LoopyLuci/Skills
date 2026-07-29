---
name: continual-lifelong-learning
description: "Use when implementing continual and lifelong learning."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [continual-learning, lifelong-learning, catastrophic-forgetting, elastic-weight-consolidation]
    related_skills: [transfer-learning-patterns, self-supervised-learning, meta-learning-few-shot, model-compression-techniques]
---

# Continual and Lifelong Learning

Training models that learn sequentially across tasks without catastrophic forgetting — regularization, replay, architectural, and meta-learning approaches.

## When to Use

- A model must learn new tasks over time without forgetting old ones
- Training data arrives in streams (online learning, incremental learning)
- Retraining from scratch on all data is too expensive
- Building models that continuously adapt to distribution shifts
- Personalizing models without losing general knowledge

## Catastrophic Forgetting

```python
# The problem: learning task B overwrites weights useful for task A
# Task A accuracy drops from 90% → 30% after training on Task B
```

## Approaches

### EWC (Elastic Weight Consolidation)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ElasticWeightConsolidation:
    """EWC: Regularize weight changes, penalizing changes to
    weights that were important for previous tasks."""
    
    def __init__(self, model):
        self.model = model
        self.fisher_information = {}  # Importance of each weight
        self.optimal_params = {}      # Optimal value after previous tasks
    
    def compute_fisher(self, dataloader):
        """Compute diagonal Fisher Information Matrix.
        
        Measures how much each parameter contributes to the loss.
        High Fisher = important for the task."""
        
        self.model.eval()
        fisher = {name: torch.zeros_like(param) 
                 for name, param in self.model.named_parameters() 
                 if param.requires_grad}
        
        for inputs, targets in dataloader:
            self.model.zero_grad()
            outputs = self.model(inputs)
            loss = F.cross_entropy(outputs, targets)
            loss.backward()
            
            # Accumulate squared gradients (Fisher diagonal)
            for name, param in self.model.named_parameters():
                if param.grad is not None:
                    fisher[name] += param.grad ** 2 / len(dataloader)
        
        self.fisher_information = fisher
        self.optimal_params = {
            name: param.clone().detach()
            for name, param in self.model.named_parameters()
            if param.requires_grad
        }
    
    def ewc_loss(self, model, lambda_ewc=1000):
        """EWC regularization term.
        
        Penalty: λ/2 * Σ_i Fisher_i * (θ_i - θ*_i)²
        Where Fisher_i is importance of weight i,
        θ_i is current weight, θ*_i is optimal weight."""
        
        loss = 0
        for name, param in model.named_parameters():
            if name in self.fisher_information:
                fisher = self.fisher_information[name]
                optimal = self.optimal_params[name]
                loss += (fisher * (param - optimal) ** 2).sum()
        
        return (lambda_ewc / 2) * loss
    
    def training_step(self, current_task_loss, model):
        """Total loss = current task loss + EWC penalty."""
        return current_task_loss + self.ewc_loss(model)
```

### Experience Replay

```python
import random
from collections import deque

class ExperienceReplay:
    """Store samples from previous tasks and replay them during new tasks."""
    
    def __init__(self, capacity=1000):
        self.memory = deque(maxlen=capacity)
    
    def add_samples(self, inputs, targets):
        """Store examples from a task."""
        for x, y in zip(inputs, targets):
            self.memory.append((x.clone(), y.clone()))
    
    def sample(self, batch_size):
        """Mix replay samples with current batch."""
        if len(self.memory) < batch_size:
            return None, None
        
        batch = random.sample(self.memory, batch_size)
        inputs = torch.stack([x for x, _ in batch])
        targets = torch.tensor([y for _, y in batch])
        return inputs, targets
    
    def replay_loss(self, model, batch_size, criterion):
        """Compute loss on replayed samples."""
        inputs, targets = self.sample(batch_size)
        if inputs is None:
            return 0
        
        outputs = model(inputs)
        return criterion(outputs, targets)
```

### Progressive Neural Networks

```python
class ProgressiveNetwork(nn.Module):
    """Add new columns for new tasks, freeze old columns.
    
    Each task gets its own network column, with lateral
    connections to previous columns for feature reuse."""
    
    def __init__(self, input_dim, hidden_dim, output_dims):
        super().__init__()
        self.columns = nn.ModuleList()
        self.output_dims = output_dims
    
    def add_task(self, output_dim):
        """Add a new column for a new task."""
        new_column = nn.ModuleDict({
            'fc1': nn.Linear(self.input_dim + len(self.columns) * self.hidden_dim, self.hidden_dim),
            'fc2': nn.Linear(self.hidden_dim, output_dim)
        })
        
        # Freeze all previous columns
        for col in self.columns:
            for param in col.parameters():
                param.requires_grad = False
        
        self.columns.append(new_column)
    
    def forward(self, x, task_id):
        """Forward through columns up to task_id.
        
        Each column receives input from the original input
        plus all previous columns' hidden representations."""
        features = [x]
        
        for i in range(task_id + 1):
            col_input = torch.cat(features, dim=1)
            h = torch.relu(self.columns[i]['fc1'](col_input))
            features.append(h)
        
        return self.columns[task_id]['fc2'](features[-1])
```

### Memory-Aware Synapses (MAS)

```python
class MemoryAwareSynapses:
    """MAS: estimate parameter importance by sensitivity of
    output to parameter changes (no labels needed)."""
    
    def compute_importance(self, model, dataloader):
        """Compute importance based on gradient of L2 norm of output."""
        model.eval()
        importance = {name: torch.zeros_like(param)
                     for name, param in model.named_parameters()
                     if param.requires_grad}
        
        for inputs, _ in dataloader:
            outputs = model(inputs)
            # L2 norm of output
            output_norm = outputs.norm()
            output_norm.backward()
            
            for name, param in model.named_parameters():
                if param.grad is not None:
                    importance[name] += param.grad.abs() / len(dataloader)
        
        return importance
```

## Evaluation Metrics for Continual Learning

```python
class ContinualLearningMetrics:
    """Track forgetting and forward transfer."""
    
    def __init__(self, num_tasks):
        self.accuracy_matrix = [[None] * num_tasks for _ in range(num_tasks)]
        # accuracy_matrix[i][j] = accuracy on task j after learning task i
    
    def record_accuracy(self, task_i, task_j, accuracy):
        self.accuracy_matrix[task_i][task_j] = accuracy
    
    def forgetting_measure(self, task_j, num_tasks_learned):
        """How much did task j accuracy drop after learning later tasks."""
        best = max(self.accuracy_matrix[i][task_j] 
                  for i in range(task_j, num_tasks_learned))
        final = self.accuracy_matrix[num_tasks_learned - 1][task_j]
        return best - final
    
    def average_forgetting(self, num_tasks_learned):
        if num_tasks_learned <= 1:
            return 0.0
        forget = [self.forgetting_measure(j, num_tasks_learned) 
                 for j in range(num_tasks_learned - 1)]
        return sum(forget) / len(forget) if forget else 0.0
    
    def forward_transfer(self, task_j):
        """How much did learning previous tasks help task j?"""
        # Compare accuracy with random init vs after previous tasks
        pass
```

## Common Pitfalls

1. **Task boundary ambiguity** — in streaming scenarios, tasks aren't clearly separated; use change point detection
2. **Replay memory poisoning** — mislabeled replay samples corrupt knowledge; verify replay quality
3. **Fisher approximation quality** — EWC's diagonal Fisher is a crude approximation; full Fisher is expensive
4. **Network capacity saturation** — after many tasks, model has no capacity left; expand architecture
5. **Evaluation protocol confusion** — task-incremental vs class-incremental vs domain-incremental need different metrics
6. **Rehearsal overhead** — storing all previous data defeats the purpose; use generative replay

## Verification Checklist

- [ ] Baseline: model without CL forgets catastrophically (accuracy drops >20%)
- [ ] CL method reduces forgetting to <5% average forgetting
- [ ] No unreasonable data storage (replay buffer bounded)
- [ ] Forward transfer positive (learning earlier tasks helps later ones)
- [ ] Compute/memory overhead of CL method is acceptable
- [ ] Scales to at least 10 sequential tasks

## See Also

- transfer-learning-patterns — single-step transfer (vs continual)
- self-supervised-learning — pre-training without forgetting
- meta-learning-few-shot — learning to learn across tasks
- model-compression-techniques — reducing model size for CL
