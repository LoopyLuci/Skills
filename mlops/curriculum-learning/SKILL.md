---
name: curriculum-learning
description: "Use when implementing curriculum learning strategies."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [curriculum-learning, training-strategy, easy-to-hard, progressive-learning]
    related_skills: [continual-lifelong-learning, deep-reinforcement-learning, active-learning-strategies, custom-training-loops]
---

# Curriculum Learning

Implementing curriculum learning strategies — from easy-to-hard training through pacing functions, self-paced learning, and anti-curriculum approaches.

## When to Use

- Training models that benefit from gradual complexity
- Improving convergence speed and final performance
- Reducing overfitting by starting with easier examples
- Training on noisy data by filtering as curriculum progresses
- RL environments with increasing difficulty levels

## Curriculum Strategies

```python
CURRICULUM_STRATEGIES = {
    'easy_to_hard': 'Start with easy examples, gradually increase difficulty',
    'self_paced': 'Model selects examples with lowest loss first, expands threshold',
    'pacing_function': 'Control difficulty exposure rate (linear, exponential, step)',
    'anti_curriculum': 'Hardest examples first (sometimes works better)',
    'automatic': 'Use auxiliary model to score difficulty automatically',
}

class CurriculumLearner:
    """Train models with curriculum learning."""
    def __init__(self, model, difficulty_scores: np.array):
        self.model = model
        self.scores = difficulty_scores  # higher = more difficult
        self.indices = np.argsort(self.scores)  # easiest first
    
    def train_epoch(self, epoch: int, total_epochs: int, 
                    pacing: str = 'linear'):
        """Train on increasing fraction of data based on pacing."""
        if pacing == 'linear':
            fraction = min(1.0, (epoch + 1) / total_epochs)
        elif pacing == 'exponential':
            fraction = min(1.0, 0.1 * (1.5 ** epoch))
        elif pacing == 'step':
            fraction = min(1.0, (epoch // 5 + 1) * 0.25)
        else:
            fraction = 1.0
        
        n_samples = max(10, int(len(self.indices) * fraction))
        current_indices = self.indices[:n_samples]
        
        # Train on selected subset
        loss = self.model.partial_fit(current_indices)
        return {'fraction': fraction, 'n_samples': n_samples, 'loss': loss}
```

## Common Pitfalls

1. **Easy definition is hard** — defining what makes an example "easier" is non-trivial
2. **No benefit for simple tasks** — curriculum helps most for complex tasks; baseline tests first
3. **Curriculum too fast** — moving to hard examples too quickly loses benefits; tune pacing
4. **Anti-curriculum surprise** — sometimes hard examples first works better for certain architectures
5. **Domain-specific** — what works for vision may not work for NLP; experiment

## Verification Checklist

- [ ] Difficulty scoring method defined (loss, length, noise, confidence)
- [ ] Pacing function chosen (linear, exponential, step, adaptive)
- [ ] Training epochs planned for curriculum schedule
- [ ] Baseline: standard training (no curriculum) for comparison
- [ ] Curriculum benefit measured (convergence speed, final accuracy)
- [ ] Ablation: test anti-curriculum (hardest first)
- [ ] Curriculum schedule tuned (not too fast, not too slow)
