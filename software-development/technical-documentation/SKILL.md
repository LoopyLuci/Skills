---
name: technical-documentation
description: "Use when writing technical documentation for projects."
category: software-development
tags: [documentation, writing, technical, api-docs, readme]
---
# Technical Documentation

Writing clear, comprehensive technical documentation.

## Documentation Types

| Type | Audience | Purpose |
|------|----------|---------|
| README | New users | What is this? How to start? |
| Getting Started | New developers | Setup, first tutorial |
| API Reference | Integrators | Function signatures, parameters |
| Architecture | Maintainers | Design decisions, data flow |
| Operations | DevOps | Deploy, monitor, troubleshoot |
| Contributing | Contributors | How to build, test, submit PRs |

## README Template

```markdown
# Project Name

[Short description — one paragraph]

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

```bash
git clone https://github.com/user/project
cd project
docker compose up -d
```

## Usage

```python
from myproject import Client
client = Client()
result = client.process(data)
```

## Documentation

Full documentation at [docs.example.com](https://docs.example.com)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

## API Documentation (OpenAPI/Swagger)

```python
# FastAPI auto-generates OpenAPI docs
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Model API",
    description="API for training and serving ML models",
    version="1.0.0",
)

class TrainingRequest(BaseModel):
    model_name: str
    config: dict
    dataset_path: str

@app.post("/train", summary="Train a model", tags=["Training"])
async def train_model(request: TrainingRequest):
    """Train a model with the specified configuration.

    - **model_name**: Must be one of the registered architectures
    - **config**: Hyperparameters including learning_rate, batch_size
    - **dataset_path**: Path to training data in the data lake
    """
    ...
```

## Architecture Documentation

```markdown
# Architecture: Model Training Pipeline

## Overview
[Diagram: Data → Preprocess → Train → Evaluate → Deploy]

## Components
### 1. Data Ingestion
- Source: S3 bucket `s3://data-raw/`
- Format: Parquet (partitioned by date)
- Schema: [link to schema registry]

### 2. Preprocessing
- Missing value imputation
- Outlier removal (IQR)
- Feature encoding (target encoding + OHE)
- Normalization (StandardScaler)

### 3. Training
- Framework: PyTorch 2.1
- Architecture: Transformer (12 layers, 8 heads)
- Hardware: 4x A100 80GB
- Distributed: DDP (torchrun)

### 4. Evaluation
- Holdout validation (20% stratified)
- Metrics: F1 weighted, MCC, log loss
- Minimum threshold: F1 > 0.85

### 5. Deployment
- Format: TorchScript
- Serving: Triton Inference Server
- Monitoring: Prometheus + Grafana

## Data Flow
1. Raw data → S3 Event → Lambda → Preprocessing Job
2. Preprocessed → S3 (processed/) → Training Job
3. Model → S3 (models/) → Model Registry
4. Production → Triton → Inference API

## Failure Modes
- Data quality issues → alerts in validation step
- Training job OOM → reduce batch size or increase instance
- Model drift → retrain trigger based on performance threshold
```

## Code Documentation

```python
def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    config: TrainingConfig,
) -> float:
    """Train a PyTorch model for one epoch.

    Args:
        model: The PyTorch model to train. Must support
            forward() and backward().
        train_loader: DataLoader yielding (inputs, labels) tuples.
        val_loader: DataLoader for validation metrics.
        config: TrainingConfig with lr, weight_decay, clip_grad.

    Returns:
        The average validation loss for this epoch.

    Raises:
        ValueError: If model is not in training mode.
        RuntimeError: If GPU out of memory, automatically
            reduces batch size.
    """
```

## Pitfalls

- README is the first impression — invest time here
- Outdated docs are worse than no docs — keep them fresh
- Assume reader is competent but unfamiliar — explain WHY, not just HOW
- Examples must work — test every code block in your docs
- Version your docs — major version changes should have migration guides
