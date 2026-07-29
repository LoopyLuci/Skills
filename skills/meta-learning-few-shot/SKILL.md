---
name: meta-learning-few-shot
description: "Use when implementing meta-learning and few-shot learning."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta-learning, few-shot, MAML, prototypical, pytorch]
    related_skills: [self-supervised-learning, transfer-learning, custom-training-loops, llm-fine-tuning-lora]
---

# Meta-Learning and Few-Shot Learning

Implementing meta-learning (learning to learn) and few-shot learning systems that rapidly adapt to new tasks from very few examples — including optimization-based (MAML), metric-based (Prototypical Networks), and model-based approaches.

## When to Use

- Training models that must adapt to new tasks with 1–20 examples
- Building systems that learn from few demonstrations (robotics, personalization)
- Fast fine-tuning where full retraining is too expensive
- Cross-task generalization where you have many similar tasks
- Agentic systems that must quickly adapt to new environments

## Algorithm Families

### Metric-Based (Learning a Similarity Space)

Compare query examples to support set in embedding space.

**Prototypical Networks**

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class PrototypicalNet(nn.Module):
    """Prototypical Networks: classify by distance to class prototypes.
    Support set: K examples per class × N classes (N-way K-shot)."""
    
    def __init__(self, encoder):
        super().__init__()
        self.encoder = encoder  # Pre-trained or meta-trained encoder
    
    def forward(self, support_x, support_y, query_x):
        """
        support_x: (N_way * K_shot, C, H, W) — support images
        support_y: (N_way * K_shot,) — support labels
        query_x: (N_query, C, H, W) — query images
        """
        # Embed all images
        support_embeddings = self.encoder(support_x)
        query_embeddings = self.encoder(query_x)
        
        # Compute class prototypes (mean embedding per class)
        n_way = len(support_y.unique())
        prototypes = []
        for c in range(n_way):
            mask = support_y == c
            prototypes.append(support_embeddings[mask].mean(0))
        prototypes = torch.stack(prototypes)
        
        # Compute distances from queries to prototypes
        distances = torch.cdist(query_embeddings, prototypes)  # (N_query, N_way)
        
        # Convert to probabilities
        logits = -distances
        return F.log_softmax(logits, dim=-1)
    
    def loss(self, support_x, support_y, query_x, query_y):
        log_probs = self.forward(support_x, support_y, query_x)
        return F.nll_loss(log_probs, query_y)
```

### Optimization-Based (Learning to Fine-Tune)

**MAML (Model-Agnostic Meta-Learning)**

```python
class MAML:
    """Model-Agnostic Meta-Learning: learn initialization that
    adapts quickly via a few gradient steps on new tasks."""
    
    def __init__(self, model, inner_lr=0.01, meta_lr=0.001, inner_steps=5):
        self.model = model
        self.inner_lr = inner_lr
        self.meta_lr = meta_lr
        self.inner_steps = inner_steps
        self.meta_optimizer = torch.optim.Adam(model.parameters(), lr=meta_lr)
    
    def meta_train_step(self, task_batch):
        """
        task_batch: list of tasks, each with (support_x, support_y, query_x, query_y)
        """
        meta_loss = 0
        
        for support_x, support_y, query_x, query_y in task_batch:
            # Clone model for inner loop
            fast_weights = {name: param.clone() for name, param in self.model.named_parameters()}
            
            # Inner loop: adapt to task with a few gradient steps
            for _ in range(self.inner_steps):
                logits = self.model.functional_forward(support_x, fast_weights)
                loss = F.cross_entropy(logits, support_y)
                grads = torch.autograd.grad(loss, fast_weights.values(), create_graph=True)
                fast_weights = {name: w - self.inner_lr * g 
                              for (name, w), g in zip(fast_weights.items(), grads)}
            
            # Query loss on adapted model
            logits = self.model.functional_forward(query_x, fast_weights)
            meta_loss += F.cross_entropy(logits, query_y)
        
        # Meta-update (second-order gradient through inner loop)
        meta_loss /= len(task_batch)
        self.meta_optimizer.zero_grad()
        meta_loss.backward()
        self.meta_optimizer.step()
        
        return meta_loss.item()
    
    def adapt(self, support_x, support_y, steps=None):
        """Adapt to new task (no meta-gradient, just inner loop)."""
        steps = steps or self.inner_steps
        
        # Create a copy for adaptation
        adapted_model = copy.deepcopy(self.model)
        optimizer = torch.optim.SGD(adapted_model.parameters(), lr=self.inner_lr)
        
        for _ in range(steps):
            logits = adapted_model(support_x)
            loss = F.cross_entropy(logits, support_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        return adapted_model
```

**Reptile (First-Order MAML)**

```python
class Reptile:
    """First-order meta-learning. Simpler than MAML.
    Just move initialization towards task-specific weights."""
    
    def __init__(self, model, inner_lr=0.01, meta_lr=0.1, inner_steps=5):
        self.model = model
        self.inner_lr = inner_lr
        self.meta_lr = meta_lr
        self.inner_steps = inner_steps
    
    def meta_train_step(self, task_batch):
        """Reptile update: W = W + meta_lr * (W_task - W)"""
        for support_x, support_y, _, _ in task_batch:
            # Save initial weights
            init_weights = {name: p.clone().detach() for name, p in self.model.named_parameters()}
            
            # SGD on task
            adapted_model = copy.deepcopy(self.model)
            optimizer = torch.optim.SGD(adapted_model.parameters(), lr=self.inner_lr)
            
            for _ in range(self.inner_steps):
                logits = adapted_model(support_x)
                loss = F.cross_entropy(logits, support_y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            
            # Move initialization towards task-specific weights
            with torch.no_grad():
                for name, param in self.model.named_parameters():
                    param += self.meta_lr * (adapted_model.state_dict()[name] - param)
```

### Model-Based (Learning to Learn via Internal State)

```python
class MetaNetwork(nn.Module):
    """A network that learns to learn by updating its own weights
    via a learned optimizer (learned gradient descent)."""
    
    def __init__(self, input_dim, hidden_dim=128):
        super().__init__()
        self.core_network = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.output_layer = nn.Linear(hidden_dim, input_dim)
        # Learned learning rate
        self.lr_net = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()  # Output [0, 1] learning rate
        )
```

## Few-Shot Dataset Patterns

```python
class EpisodeSampler:
    """Sample N-way K-shot episodes from a dataset."""
    def __init__(self, dataset, n_way=5, k_shot=1, n_query=15):
        self.dataset = dataset
        self.n_way = n_way
        self.k_shot = k_shot
        self.n_query = n_query
        
        # Group by class
        self.class_to_indices = {}
        for idx, (_, label) in enumerate(dataset):
            self.class_to_indices.setdefault(label, []).append(idx)
    
    def sample_episode(self):
        """Sample one episode: support set + query set."""
        classes = random.sample(list(self.class_to_indices.keys()), self.n_way)
        
        support_x, support_y = [], []
        query_x, query_y = [], []
        
        for i, cls in enumerate(classes):
            indices = self.class_to_indices[cls]
            sampled = random.sample(indices, self.k_shot + self.n_query)
            
            for j, idx in enumerate(sampled):
                x, _ = self.dataset[idx]
                if j < self.k_shot:
                    support_x.append(x)
                    support_y.append(i)
                else:
                    query_x.append(x)
                    query_y.append(i)
        
        return (torch.stack(support_x), torch.tensor(support_y),
                torch.stack(query_x), torch.tensor(query_y))
```

## Training Loop

```python
def train_prototypical(encoder, dataset, n_way=5, k_shot=1, n_query=15,
                       episodes=10000, lr=1e-3):
    model = PrototypicalNet(encoder)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    sampler = EpisodeSampler(dataset, n_way, k_shot, n_query)
    
    for episode in range(episodes):
        support_x, support_y, query_x, query_y = sampler.sample_episode()
        loss = model.loss(support_x, support_y, query_x, query_y)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if episode % 100 == 0:
            print(f"Episode {episode}, Loss: {loss.item():.4f}")
    
    return model
```

## Cross-Domain and Cross-Task

```python
class CrossDomainMetaLearner:
    """Meta-learn across different domains (images, text, audio)."""
    def meta_train(self, domain_tasks):
        """domain_tasks: dict of {domain_name: [task1, task2, ...]}"""
        for domain, tasks in domain_tasks.items():
            # Option 1: Shared encoder with domain-specific heads
            # Option 2: Domain-agnostic embedding + task-specific adaptation
            pass
```

## Common Pitfalls

1. **Task distribution mismatch** — meta-test tasks must come from same distribution as meta-training
2. **Second-order optimization cost** — MAML's gradient-through-gradient is expensive (2x memory); use FOMAML or Reptile
3. **Overfitting to support set** — K-shot is very few examples; use data augmentation and strong regularization
4. **Catastrophic forgetting** — meta-training on too many tasks can overwrite earlier knowledge; use episodic replay
5. **Network capacity** — too few parameters can't represent the meta-knowledge; too many overfit to specific tasks
6. **Evaluation protocol** — always test on unseen tasks (unseen class combinations), not just unseen examples of seen classes

## Verification Checklist

- [ ] Meta-training converges (episode loss decreases over tasks)
- [ ] Meta-test on unseen tasks beats random initialization after same number of gradient steps
- [ ] Ablation: more inner steps improves adaptation (shows learning is happening)
- [ ] Ablation: more K-shot examples improves performance (shows data efficiency)
- [ ] Evaluation uses strict class separation (no overlapping classes between meta-train and meta-test)
- [ ] Results reported with confidence intervals (few-shot is high variance)

## See Also

- self-supervised-learning — pre-training without labels
- transfer-learning — transferring across tasks
- llm-fine-tuning-lora — efficient fine-tuning for LLMs
- custom-training-loops — customizing meta-training loops
