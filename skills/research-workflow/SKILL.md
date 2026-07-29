---
name: research-workflow
description: "Use when conducting systematic AI/ML research."
category: mlops
tags: [research, methodology, experiment, literature-review]
---
# Research Workflow

Systematic approach to AI/ML research: literature review, experimentation, reporting.

## Literature Review

```python
# 1. Search
# - arXiv: https://arxiv.org/search/?query=transformer+attention
# - Google Scholar, Semantic Scholar
# - PapersWithCode (for benchmarks + implementations)

# 2. Filter (relevance, recency, venue)
def filter_papers(papers: list, max_age_days=365, min_citations=10):
    return [
        p for p in papers
        if p.age_days <= max_age_days or p.citations >= min_citations
    ]

# 3. Read system: Three-pass approach
# Pass 1: Title + abstract + figures (5 min) → keep or discard
# Pass 2: Intro + method + results (30 min) → understand approach
# Pass 3: Full paper + appendix (2 hrs) → deep understanding

# 4. Synthesize
# - Create comparison table of existing approaches
# - Identify gaps: What's missing? What can be improved?
# - Formulate hypothesis: "Can we improve X by applying Y to Z?"
```

## Experiment Design

```python
from dataclasses import dataclass
from typing import Any
import json
from datetime import datetime

@dataclass
class Experiment:
    name: str
    hypothesis: str
    config: dict
    metrics: dict = None
    results: Any = None
    conclusions: str = None

    def to_dict(self):
        return {
            "name": self.name,
            "hypothesis": self.hypothesis,
            "config": self.config,
            "metrics": self.metrics,
            "timestamp": datetime.now().isoformat(),
        }

    def save(self, path: str):
        with open(f"{path}/{self.name}.json", "w") as f:
            # Exclude large results
            save_data = self.to_dict()
            save_data["results_summary"] = str(self.results)[:500] if self.results else None
            json.dump(save_data, f, indent=2)
```

## Ablation Studies

```python
def run_ablation(model_class, dataset, config: dict) -> dict:
    """Systematically remove/modify components to measure their impact."""
    variations = {}

    # Baseline (all components)
    baseline = train_eval(model_class(**config), dataset)
    variations["baseline"] = baseline

    # Remove each component
    for component in ["attention", "feedforward", "layernorm", "residual"]:
        ablated_config = config.copy()
        ablated_config[f"disable_{component}"] = True
        try:
            result = train_eval(model_class(**ablated_config), dataset)
            variations[f"no_{component}"] = result
        except Exception as e:
            variations[f"no_{component}"] = f"FAILED: {e}"

    return variations
```

## Research Log Template

```markdown
# Experiment: {date}_{hypothesis_short}

## Hypothesis
[One sentence]

## Configuration
- Model: {architecture}
- Dataset: {name, size, splits}
- Hyperparameters: {lr, batch_size, epochs, optimizer}
- Hardware: {GPU, RAM}

## Results
| Metric | Value | vs Baseline |
|--------|-------|-------------|
| Accuracy | 0.92 | +0.03 |
| F1 | 0.89 | +0.02 |
| Training time | 4.2h | -1.1h |

## Key Findings
1. ...
2. ...

## Next Steps
- [ ] Test on different dataset
- [ ] Vary hyperparameter X
- [ ] Compare with approach Y

## Takeaways for Skills
- [ ] Should I create a skill from this?
```

## Hypothesis Testing Framework

```python
class HypothesisTest:
    def __init__(self, null_hypothesis: str, experiment_fn, significance_level=0.05):
        self.null = null_hypothesis
        self.experiment = experiment_fn
        self.alpha = significance_level

    def run(self, n_trials: int = 5) -> dict:
        results = [self.experiment() for _ in range(n_trials)]

        import numpy as np
        mean = np.mean(results)
        std = np.std(results)

        return {
            "null_hypothesis": self.null,
            "mean": mean,
            "std": std,
            "n_trials": n_trials,
            "significant": abs(mean) / (std + 1e-8) > 2,  # rough heuristic
        }
```

## Reproducibility Checklist

- [ ] Random seeds set for ALL libraries (torch, numpy, random, Python hash)
- [ ] GPU determinism enabled (torch.backends.cudnn.deterministic=True)
- [ ] All hyperparameters logged (wandb, MLflow, or JSON)
- [ ] Dataset version pinned (hash or commit)
- [ ] Code version pinned (git commit or tag)
- [ ] Hardware recorded (GPU model, driver, CUDA version)
- [ ] Results saved before any analysis
- [ ] Base image or container recorded

## Pitfalls

- Confirmation bias: design experiments to DISPROVE your hypothesis
- p-hacking: don't run 100 experiments and report only the significant ones
- Compute budget: plan experiments from cheapest to most expensive
- Negative results are valuable — report them!
- Reproducibility requires discipline — automate logging from day one
