---
name: hyperparameter-optimization-ml
description: "Use when optimizing hyperparameters for ML models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hyperparameter, optimization, tuning, automl, bayesian, grid-search]
    related_skills: [neural-architecture-search, custom-training-loops, model-evaluation-metrics, ml-pipeline-design]
---

# Hyperparameter Optimization for ML

Systematic approaches to tuning model hyperparameters — from grid and random search through Bayesian optimization, bandit-based methods, and multi-fidelity techniques.

## When to Use

- Your model isn't converging and you suspect suboptimal hyperparameters
- Preparing a model for production deployment (squeezing out last 5-10% performance)
- Building AutoML pipelines that need automated tuning
- Comparing algorithms requires fair (well-tuned) baselines
- Reducing manual trial-and-error in the training workflow

## Optimization Methods

| Method | Budget | Params | Best For | Parallel |
|--------|--------|--------|----------|----------|
| Grid Search | High | Low | Small spaces, exhaustive | Yes |
| Random Search | Low | High | Most problems | Yes |
| Bayesian (GP) | Medium | Medium | Medium budget, noisy | Limited |
| Bayesian (TPE) | Medium | Mixed | Heterogeneous spaces | No |
| Hyperband | Low | High | Large spaces, many configs | Yes |
| Population-based | Medium | High | Training-time tuning | Yes |

### Random Search (Baseline)

```python
import random
import itertools
from dataclasses import dataclass
from typing import Dict, Any

class RandomSearch:
    """Random search — often 80% as good as Bayesian for 20% of complexity.
    Key insight from Bergstra & Bengio (2012)."""
    
    def __init__(self, param_space: Dict[str, list], n_trials=100):
        self.param_space = param_space
        self.n_trials = n_trials
    
    def sample(self) -> Dict[str, Any]:
        """Sample one random configuration."""
        config = {}
        for name, values in self.param_space.items():
            if isinstance(values, (list, tuple)):
                config[name] = random.choice(values)
            elif isinstance(values, dict):
                # Range: {'min': 1e-5, 'max': 1.0, 'log': True}
                if values.get('log'):
                    log_min = math.log(values['min'])
                    log_max = math.log(values['max'])
                    config[name] = math.exp(random.uniform(log_min, log_max))
                else:
                    config[name] = random.uniform(values['min'], values['max'])
        return config
    
    def optimize(self, objective_fn):
        """Run random search."""
        results = []
        for i in range(self.n_trials):
            config = self.sample()
            score = objective_fn(config)
            results.append((score, config))
            print(f"Trial {i+1}/{self.n_trials}: {score:.4f}")
        
        results.sort(key=lambda x: x[0], reverse=True)
        return results[0]
```

### Bayesian Optimization (GP)

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel
import numpy as np

class BayesianOptimization:
    """Bayesian optimization with Gaussian Processes.
    
    Uses acquisition function (Expected Improvement) to balance
    exploration vs exploitation."""
    
    def __init__(self, param_bounds, n_init=10, n_iter=50):
        self.bounds = param_bounds  # {name: (min, max)}
        self.n_init = n_init
        self.n_iter = n_iter
        self.X = []
        self.y = []
        
        self.gp = GaussianProcessRegressor(
            kernel=ConstantKernel(1.0) * Matern(length_scale=1.0, nu=2.5),
            normalize_y=True,
            n_restarts_optimizer=5,
            random_state=42
        )
    
    def optimize(self, objective_fn):
        # Initial random points
        for _ in range(self.n_init):
            x = self._sample_random()
            y = objective_fn(x)
            self.X.append(x)
            self.y.append(y)
        
        # Bayesian iterations
        for i in range(self.n_iter):
            self.gp.fit(np.array(self.X), np.array(self.y))
            
            # Find next point via acquisition function maximization
            x_next = self._propose_point()
            y_next = objective_fn(x_next)
            
            self.X.append(x_next)
            self.y.append(y_next)
            print(f"Iter {i+1}/{self.n_iter}: {y_next:.4f}")
        
        best_idx = np.argmax(self.y)
        return self.y[best_idx], self.X[best_idx]
    
    def _propose_point(self):
        """Find point that maximizes Expected Improvement."""
        def negative_ei(x):
            x = x.reshape(1, -1)
            mu, sigma = self.gp.predict(x, return_std=True)
            y_best = max(self.y)
            
            with np.errstate(divide='warn'):
                imp = mu - y_best
                Z = imp / sigma
                ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
                ei[sigma == 0.0] = 0.0
            
            return -ei
        
        # Multi-start optimization
        best_x = None
        best_ei = float('inf')
        for _ in range(20):
            x0 = self._sample_random()
            result = minimize(negative_ei, x0, bounds=list(self.bounds.values()),
                            method='L-BFGS-B')
            if result.fun < best_ei:
                best_ei = result.fun
                best_x = result.x
        
        return best_x
```

### Hyperband (Multi-Fidelity)

```python
class Hyperband:
    """Hyperband: resource-efficient hyperparameter search.
    
    Allocates more resources to promising configurations via
    successive halving. Supports early stopping of bad configs."""
    
    def __init__(self, param_space, max_epochs=81, eta=3):
        self.param_space = param_space
        self.max_epochs = max_epochs
        self.eta = eta  # Elimination factor
    
    def optimize(self, train_fn):
        """Run Hyperband optimization.
        
        train_fn(config, budget) — trains for `budget` epochs and returns score.
        """
        s_max = int(math.log(self.max_epochs, self.eta))
        B = (s_max + 1) * self.max_epochs
        
        results = []
        
        for s in range(s_max, -1, -1):
            n = int(math.ceil(B / (self.max_epochs * (s + 1) * self.eta**s)))
            r = self.max_epochs * self.eta**(-s)
            
            # Generate initial candidates
            candidates = [self._sample() for _ in range(n)]
            
            for i in range(s + 1):
                ni = int(n * self.eta**(-i))
                ri = int(r * self.eta**i)
                
                # Train all candidates for ri epochs
                scores = []
                for config in candidates[:ni]:
                    score = train_fn(config, ri)
                    scores.append(score)
                
                # Keep top 1/eta
                sorted_indices = np.argsort(scores)[::-1]
                keep = int(ni / self.eta)
                candidates = [candidates[idx] for idx in sorted_indices[:keep]]
                
                results.append((max(scores), candidates[0]))
        
        return max(results, key=lambda x: x[0])
```

## Population-Based Training (PBT)

```python
class PBT:
    """Population-Based Training: evolve hyperparameters during training.
    Used by AlphaGo, DeepMind for RL hyperparameter tuning."""
    
    def __init__(self, population_size=20, exploit_quantile=0.2, explore_prob=0.2):
        self.population = []
        self.pop_size = population_size
        self.exploit_q = exploit_quantile
        self.explore_p = explore_prob
    
    def run(self, worker_fn, total_steps=1000):
        # Initialize population
        for _ in range(self.pop_size):
            self.population.append({
                'params': self._sample_params(),
                'state': None,
                'score': float('-inf'),
                'step': 0
            })
        
        for step in range(total_steps):
            # Train all members
            for member in self.population:
                member['state'], member['score'] = worker_fn(
                    member['state'], member['params'], member['score']
                )
                member['step'] += 1
            
            # PBT update
            scores = sorted([m['score'] for m in self.population])
            threshold = scores[int(self.pop_size * self.exploit_q)]
            
            for member in self.population:
                if member['score'] <= threshold:
                    # EXPLOIT: copy from a better member
                    better = random.choice([m for m in self.population 
                                          if m['score'] > threshold])
                    member['params'] = dict(better['params'])
                    member['state'] = better['state']
                    member['score'] = better['score']
                    
                    # EXPLORE: perturb hyperparameters
                    if random.random() < self.explore_p:
                        member['params'] = self._perturb(member['params'])
```

## Common Pitfalls

1. **Too few trials** — random search needs at least 10× the number of hyperparameters
2. **Over-tuning on validation set** — every HP optimization run uses the val set; track how many times it's been used
3. **Ignoring interactions** — learning rate and batch size interact; optimize jointly, not sequentially
4. **Bayesian on high-dim** — GP-based BO fails above ~20 dimensions; use random search or Hyperband
5. **Same seed across configs** — a lucky seed makes a bad config look good; run each config with multiple seeds
6. **Not tuning the optimizer** — Adam's default lr=1e-3 is rarely optimal; include optimizer params in the search

## Verification Checklist

- [ ] Search space covers all important hyperparameters (LR, batch, optimizer, regularization)
- [ ] At least 3 seeds per configuration to reduce noise
- [ ] Random search baseline established before Bayesian/Hyperband
- [ ] Validation set not used for anything else (no double-dipping)
- [ ] Optimized config beats default by meaningful margin
- [ ] Results reproducible (seed logged per trial)

## See Also

- neural-architecture-search — searching architecture (complementary to HP search)
- custom-training-loops — implementing the training loop being tuned
- model-evaluation-metrics — measuring what we're optimizing
- ml-pipeline-design — integrating HP search into pipelines
