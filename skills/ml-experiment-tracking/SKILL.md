---
name: ml-experiment-tracking
description: "Use when tracking ML experiments and managing runs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ml-experiments, tracking, reproducibility, MLflow, W&B, metadata, versioning]
    related_skills: [weights-and-biases, ml-pipeline-design, hyperparameter-optimization-ml, model-registry-management]
---

# ML Experiment Tracking

Tracking, organizing, and managing machine learning experiments — from local run logging through full experiment management with MLflow, Weights & Biases, and custom solutions.

## When to Use

- Tracking hundreds of ML training runs
- Comparing model versions and hyperparameters
- Reproducing past experiments
- Collaborating on ML experiments with a team
- Building a central experiment registry

## Core Tracking Architecture

```python
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
import uuid

class ExperimentTracker:
    """Lightweight experiment tracking (MLflow-compatible pattern)."""
    
    def __init__(self, experiment_name: str, tracking_uri: str = './mlruns'):
        self.experiment_name = experiment_name
        self.tracking_uri = tracking_uri
        self.run_id = None
        self.run_name = None
        self.params = {}
        self.metrics = {}
        self.artifacts = []
        self.tags = {}
    
    def start_run(self, run_name: str = None, tags: Dict = None):
        self.run_id = str(uuid.uuid4())
        self.run_name = run_name or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.tags = tags or {}
        self.params = {}
        self.metrics = {}
        self.artifacts = []
        print(f"🏃 Started run: {self.run_name} ({self.run_id[:8]})")
    
    def log_param(self, key: str, value: Any):
        self.params[key] = str(value)
    
    def log_params(self, params: Dict):
        for k, v in params.items():
            self.params[k] = str(v)
    
    def log_metric(self, key: str, value: float, step: int = None):
        if key not in self.metrics:
            self.metrics[key] = []
        self.metrics[key].append({'value': value, 'step': step or len(self.metrics[key])})
    
    def log_metrics(self, metrics: Dict, step: int = None):
        for k, v in metrics.items():
            self.log_metric(k, v, step)
    
    def log_artifact(self, path: str, description: str = ''):
        self.artifacts.append({'path': path, 'description': description, 'time': datetime.now().isoformat()})
    
    def end_run(self, status: str = 'completed'):
        """Save and close run."""
        run_data = {
            'run_id': self.run_id, 'run_name': self.run_name,
            'experiment': self.experiment_name, 'status': status,
            'params': self.params, 'metrics': self.metrics,
            'artifacts': self.artifacts, 'tags': self.tags,
            'start_time': self.start_time if hasattr(self, 'start_time') else None,
            'end_time': datetime.now().isoformat(),
        }
        
        os.makedirs(f"{self.tracking_uri}/{self.experiment_name}", exist_ok=True)
        with open(f"{self.tracking_uri}/{self.experiment_name}/{self.run_id}.json", 'w') as f:
            json.dump(run_data, f, indent=2)
        
        print(f"✅ Run {self.run_name} saved — {self.run_id[:8]}")
        return run_data


# Experiment tracking decorator
def track_experiment(func):
    """Decorator that wraps a training function with experiment tracking."""
    from functools import wraps
    
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.tracker.start_run(run_name=func.__name__)
        try:
            result = func(self, *args, **kwargs)
            self.tracker.end_run('completed')
            return result
        except Exception as e:
            self.tracker.end_run('failed')
            raise e
    return wrapper
```

## Experiment Comparator

```python
class ExperimentComparator:
    """Compare multiple experiment runs."""
    
    @staticmethod
    def load_runs(experiment_dir: str) -> List[Dict]:
        runs = []
        for f in os.listdir(experiment_dir):
            if f.endswith('.json'):
                with open(os.path.join(experiment_dir, f)) as fh:
                    runs.append(json.load(fh))
        return runs
    
    @staticmethod
    def compare(runs: List[Dict], metric: str = 'val_accuracy') -> str:
        report = "📊 Experiment Comparison\n" + "=" * 50 + "\n"
        
        for run in sorted(runs, key=lambda r: r.get('metrics', {}).get(metric, [{}])[-1].get('value', 0), reverse=True):
            name = run.get('run_name', 'unknown')
            final_metric = run.get('metrics', {}).get(metric, [{}])[-1].get('value', 'N/A')
            params = run.get('params', {})
            
            report += f"\n**{name}** — {metric}: {final_metric}\n"
            if params:
                report += f"  Params: {', '.join(f'{k}={v}' for k, v in list(params.items())[:5])}\n"
        
        return report
```

## Common Pitfalls

1. **Not tracking everything** — forgetting to log seed, data version, or environment causes irreproducibility
2. **Metric logging too sparse** — logging only final accuracy misses training dynamics
3. **No consistent naming** — "final_model_v3_final_actual_final.pth" becomes unmanageable
4. **Not comparing to baseline** — every experiment should be comparable to a fixed baseline
5. **Artifacts not versioned** — models saved without code version can't be reproduced

## Verification Checklist

- [ ] Experiment tracker logs params, metrics, artifacts, and tags
- [ ] Runs are searchable and comparable
- [ ] Code version (git commit) logged automatically
- [ ] Data version tracked (hash or dataset version)
- [ ] Environment/requirements logged
- [ ] All random seeds logged
- [ ] Training and validation metrics logged per epoch
- [ ] Best model artifacts saved with run metadata

## See Also

- weights-and-biases — W&B-specific tracking
- ml-pipeline-design — integrating tracking in pipelines
- hyperparameter-optimization-ml — tracking HPO runs
- model-registry-management — managing tracked models
