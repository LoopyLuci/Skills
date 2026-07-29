---
name: neural-architecture-search
description: "Use when implementing neural architecture search for models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [nas, architecture-search, automl, neural-networks, pytorch]
    related_skills: [custom-neural-architecture-design, hyperparameter-optimization, model-compression-techniques]
---

# Neural Architecture Search (NAS)

Automated discovery of optimal neural network architectures — from search space design through search strategies to evaluation and deployment of discovered architectures.

## When to Use

- Manual architecture design is too slow or suboptimal for your problem
- You want to automate finding Pareto-optimal architectures (quality vs. efficiency)
- Building production systems where architecture matters (mobile, edge, real-time)
- Researching new search spaces or search algorithms
- You have compute budget and want the best architecture for your data

## NAS Pipeline

```
Search Space → Search Strategy → Performance Estimation → Architecture Selection → Retraining
```

### Step 1: Define Search Space

```python
# Micro search space (cell-based): discover a cell, stack it N times
# Macro search space: discover layer types at each position

class SearchSpace:
    """Define possible operations and their parameters."""
    OPERATIONS = [
        'conv3x3', 'conv5x5', 'sep_conv3x3', 'sep_conv5x5',
        'dilated_conv3x3', 'dilated_conv5x5',
        'max_pool3x3', 'avg_pool3x3',
        'skip_connection', 'none'
    ]
    
    def sample_random_architecture(self):
        """Sample a random architecture from the space."""
        return {
            'num_cells': 8,
            'num_nodes_per_cell': 4,
            'operations': np.random.choice(self.OPERATIONS, (8, 4)),
            'connectivity': self._random_dag(4)
        }
```

### Step 2: Choose Search Strategy

**Random Search (Baseline)**
```python
def random_search(search_space, num_samples=1000, evaluator=None):
    """Simple random search. Often surprisingly effective."""
    best_arch = None
    best_score = float('-inf')
    
    for i in range(num_samples):
        arch = search_space.sample_random_architecture()
        score = evaluator.evaluate(arch)
        if score > best_score:
            best_score = score
            best_arch = arch
    
    return best_arch, best_score
```

**Evolutionary Search**
```python
class EvolutionaryNAS:
    """Population-based architecture evolution."""
    def __init__(self, search_space, pop_size=50, mutation_rate=0.2):
        self.population = [search_space.sample_random_architecture() 
                          for _ in range(pop_size)]
        self.mutation_rate = mutation_rate
    
    def mutate(self, arch):
        """Randomly mutate an architecture."""
        new_arch = copy.deepcopy(arch)
        for cell in range(new_arch['num_cells']):
            for node in range(new_arch['num_nodes_per_cell']):
                if random.random() < self.mutation_rate:
                    new_arch['operations'][cell, node] = random.choice(SEARCH_SPACE_OPERATIONS)
        return new_arch
    
    def crossover(self, arch1, arch2):
        """Single-point crossover between two architectures."""
        child = copy.deepcopy(arch1)
        split = arch1['num_cells'] // 2
        for cell in range(split, arch2['num_cells']):
            child['operations'][cell] = arch2['operations'][cell]
        return child
    
    def search(self, evaluator, generations=100):
        for gen in range(generations):
            # Evaluate fitness
            scores = [evaluator.evaluate(arch) for arch in self.population]
            
            # Selection (tournament)
            parents = self._tournament_selection(self.population, scores, k=3)
            
            # Create next generation
            offspring = []
            while len(offspring) < len(self.population):
                if random.random() < 0.3:  # Crossover probability
                    p1, p2 = random.sample(parents, 2)
                    child = self.crossover(p1, p2)
                else:
                    child = self.mutate(random.choice(parents))
                offspring.append(child)
            
            self.population = offspring
            print(f"Gen {gen}: Best score = {max(scores):.4f}")
        
        # Return best architecture
        final_scores = [evaluator.evaluate(arch) for arch in self.population]
        return self.population[final_scores.index(max(final_scores))]
```

**Differentiable NAS (DARTS)**
```python
class DARTSSearchCell(nn.Module):
    """Differentiable architecture search cell.
    Each edge is a mixed operation (weighted sum of all ops).
    Architecture weights are learned via gradient descent."""
    
    def __init__(self, C_in, C_out, num_nodes=4):
        super().__init__()
        self.num_nodes = num_nodes
        self.C_in = C_in
        
        # Architecture parameters (logits for each operation)
        self.arch_weights = nn.Parameter(torch.zeros(num_nodes, num_nodes, len(OPERATIONS)))
        
        # Operations
        self.ops = nn.ModuleDict()
        for i in range(num_nodes):
            for j in range(i):
                for k, op_name in enumerate(OPERATIONS):
                    if op_name != 'none':
                        self.ops[f'{i}_{j}_{k}'] = self._get_op(op_name, C_in, C_out)
                        self.ops[f'{i}_{j}_{k}'].requires_grad_(True)
    
    def forward(self, x):
        # Softmax over operation choices for each edge
        weights = F.softmax(self.arch_weights, dim=-1)
        
        states = [x]
        for i in range(1, self.num_nodes):
            s = 0
            for j in range(i):
                for k, op_name in enumerate(OPERATIONS):
                    w = weights[i, j, k]
                    op = self.ops.get(f'{i}_{j}_{k}')
                    if op is not None and w > 1e-5:
                        s += w * op(states[j])
            states.append(s)
        
        # Concatenate intermediate states
        return torch.cat(states[1:], dim=1)
```

### Step 3: Performance Estimation

```python
# Full training (accurate but expensive)
def full_training_eval(arch, epochs=100):
    model = build_model(arch)
    train(model, epochs)
    return evaluate(model)

# Weight-sharing / One-shot (efficient but biased)
class OneShotModel(nn.Module):
    """Supernet containing all possible architectures.
    Sub-architectures are extracted by masking paths."""
    def __init__(self, search_space):
        super().__init__()
        # Contains ALL possible operations
        self.supernet = nn.ModuleList([
            build_all_ops_layer() for _ in range(search_space.max_layers)
        ])
    
    def forward(self, x, arch_mask):
        """Forward pass with mask selecting sub-architecture."""
        for i, (layer, mask) in enumerate(zip(self.supernet, arch_mask)):
            x = layer.masked_forward(x, mask)
        return x

# Zero-shot (fastest, least accurate)
def zero_shot_score(arch):
    """Predict architecture quality without any training."""
    # Measures like: gradient signal-to-noise ratio, Jacobian properties
    score = compute_zen_score(arch)  # ZenNAS or similar
    return score
```

### Step 4: Practical NAS

```python
# EfficientNet-style compound scaling pattern
# (pre-designed scaling rules, not full search)
def compound_scale(base_width, base_depth, base_resolution, phi):
    """EfficientNet compound scaling: w * alpha^phi, d * beta^phi, r * gamma^phi"""
    alpha, beta, gamma = 1.2, 1.1, 1.15
    width = int(base_width * alpha ** phi)
    depth = int(base_depth * beta ** phi)
    resolution = int(base_resolution * gamma ** phi)
    return {'width': width, 'depth': depth, 'resolution': resolution}

# OFA (Once-For-All) progressive shrinking
class OFATrainer:
    """Train a supernet, then extract subnets at inference."""
    def __init__(self, supernet):
        self.supernet = supernet
    
    def progressive_shrinking(self, epochs):
        """Phase 1: Train full network. Phase 2-4: progressively shrink."""
        # Phase 1: Train full kernel size (7x7)
        self._train_phase(self.supernet, epochs, kernel_size=7)
        # Phase 2: Support 5x5 and 7x7
        self._train_phase(self.supernet, epochs, kernel_sizes=[5, 7])
        # Phase 3: Support 3x3, 5x5, 7x7
        self._train_phase(self.supernet, epochs, kernel_sizes=[3, 5, 7])
```

## NAS Performance Predictors

```python
class PerformancePredictor:
    """Predict architecture performance without training."""
    
    @staticmethod
    def compute_zen_score(model, dummy_input):
        """Zen-NAS score: gradient kernel alignment."""
        output = model(dummy_input)
        loss = output.norm()
        grads = torch.autograd.grad(loss, model.parameters(), create_graph=True)
        # Compute alignment score
        alignment = sum((g * g.detach()).sum() for g in grads if g is not None)
        return alignment.item()
    
    @staticmethod
    def compute_grad_norm(arch):
        """Gradient norm as proxy for trainability."""
        model = build_mini_model(arch)
        params = torch.cat([p.view(-1) for p in model.parameters()])
        return params.norm().item()
```

## Resource-Constrained NAS

```python
# Multi-objective: maximize accuracy, minimize latency
def pareto_search(search_space, latency_constraint_ms=50, memory_mb=256):
    best = []
    for _ in range(1000):
        arch = search_space.sample()
        accuracy = estimate_accuracy(arch)
        latency = measure_latency(arch)
        params = count_parameters(arch)
        
        if latency <= latency_constraint_ms and params*4 <= memory_mb:
            best.append((accuracy, latency, params, arch))
    
    # Return architectures on Pareto frontier
    return compute_pareto_frontier(best)
```

## Common Pitfalls

1. **Search-dataset mismatch** — architectures found on CIFAR-10 don't transfer to ImageNet; search on target domain
2. **Ranking correlation collapse** — one-shot weight sharing gives poor ranking of sub-architectures; use progressive shrinking
3. **Overfitting to search space** — if the search space is too small, best architecture is just the least-bad option
4. **Compute cost explosion** — full NAS on ImageNet costs 1000+ GPU-days; use proxies (zero-shot, reduced epochs)
5. **Retraining gap** — architecture found with weight sharing may underperform when retrained from scratch
6. **Operation bias** — differentiable NAS tends to favor skip connections; apply regularization

## Verification Checklist

- [ ] Search space includes reasonable baselines (manual architectures as candidates)
- [ ] Search strategy reproducible (seed set, random samples logged)
- [ ] Performance estimation method documented (full/one-shot/zero-shot)
- [ ] Found architecture beats manual baseline under same training budget
- [ ] Transfer verified (search on proxy → retrain on target)
- [ ] Pareto frontier computed if resource-constrained
- [ ] Search cost (GPU-hours) documented

## See Also

- custom-neural-architecture-design — manual architecture design patterns
- hyperparameter-optimization — tuning companion to architecture search
- model-compression-techniques — compressing found architectures
