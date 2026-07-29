---
name: mlops-pipeline-ci-cd
description: "Use when building CI/CD pipelines for ML systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mlops, CI-CD, ML-pipeline, automation, model-deployment, CI, testing]
    related_skills: [ml-pipeline-design, ml-deployment-serving, ml-experiment-tracking, model-registry-management]
---

# MLOps CI/CD Pipelines

Building CI/CD pipelines for machine learning systems — from data validation through model training, evaluation, deployment, and monitoring automation.

## When to Use

- Automating ML model training and deployment
- Building CI/CD for ML systems (not just application code)
- Ensuring reproducibility across ML pipeline runs
- Implementing staging → production model promotion
- Automating model retraining on schedule or trigger

## MLOps CI/CD Pipeline

```python
MLOPS_PIPELINE_STAGES = {
    'data_validation': 'Great Expectations checks, schema validation, data drift detection',
    'training': 'Triggered by: schedule (weekly), new data, code change, or manual',
    'evaluation': 'Compare against champion model, statistical tests, holdout set',
    'staging': 'Deploy to staging, run integration tests, shadow traffic',
    'production': 'Promote to production, monitor drift and performance',
    'monitoring': 'Continuous data and concept drift detection, performance alerts',
}

class MLPipeline:
    """Define an MLOps CI/CD pipeline."""
    def __init__(self, name: str, repo: str):
        self.name = name
        self.stages = []
    
    def add_stage(self, name: str, script: str, 
                  requirements: List[str] = None):
        self.stages.append({
            'name': name, 'script': script, 'reqs': requirements or [],
            'dependencies': self.stages[-1] if self.stages else None,
        })
    
    def to_ci_config(self, platform: str = 'github') -> str:
        if platform == 'github':
            return f"""name: MLOps - {self.name}
on: [push, workflow_dispatch, schedule(cron: '0 6 * * 0')]
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Train Model
        run: python train.py
      - name: Evaluate
        run: python evaluate.py
      - name: Deploy to Staging
        run: python deploy.py --stage staging"""
```

## Verification Checklist

- [ ] Pipeline defined with stages (data validation, train, eval, deploy, monitor)
- [ ] Triggers configured (code push, schedule, data arrival)
- [ ] Model evaluation gates before production deployment
- [ ] Automated rollback on performance degradation
- [ ] Experiment tracking integrated with each pipeline run
- [ ] Model registry updated after successful deployment
- [ ] Monitoring and alerting for pipeline failures
