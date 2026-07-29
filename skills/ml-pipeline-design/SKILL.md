---
name: ml-pipeline-design
description: "Use when designing end-to-end ML training pipelines."
category: mlops
tags: [ml, pipeline, training, data, mlops]
---
# ML Pipeline Design

Designing end-to-end machine learning training pipelines.

## Pipeline Architecture

```
Raw Data → Validate → Preprocess → Feature Eng → Split → Train → Evaluate → Deploy
                                                 │          │
                                                 └→ Test ───┘
```

## Pipeline Implementation

```python
from typing import Iterator, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
from torch.utils.data import Dataset, DataLoader

class MLPipeline:
    def __init__(self, config: dict):
        self.config = config
        self.scaler = StandardScaler()
        self.model = None

    def load_data(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        assert not df.isnull().all().any(), "Columns with all nulls"
        return df

    def validate(self, df: pd.DataFrame):
        assert df.shape[0] > 0, "Empty dataset"
        assert df.shape[1] > 1, "Need at least 2 columns"
        assert df.select_dtypes(include=[np.number]).shape[1] >= 1, "Need numeric features"

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        # Handle missing values
        df = df.fillna(df.median(numeric_only=True))
        # Remove outliers (IQR)
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1
        return df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]

    def split(self, df: pd.DataFrame, target_col: str):
        X = df.drop(columns=[target_col])
        y = df[target_col]
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def create_dataloader(self, X, y, batch_size: int = 32) -> DataLoader:
        class TorchDataset(Dataset):
            def __init__(self, X, y):
                self.X = torch.FloatTensor(X.values if hasattr(X, 'values') else X)
                self.y = torch.FloatTensor(y.values if hasattr(y, 'values') else y)

            def __len__(self): return len(self.y)
            def __getitem__(self, i): return self.X[i], self.y[i]

        return DataLoader(TorchDataset(X, y), batch_size=batch_size, shuffle=True)

    def run(self, data_path: str) -> dict:
        df = self.load_data(data_path)
        self.validate(df)
        df = self.preprocess(df)
        X_train, X_test, y_train, y_test = self.split(df, self.config["target"])

        # Scale
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        train_loader = self.create_dataloader(X_train_scaled, y_train, self.config["batch_size"])
        test_loader = self.create_dataloader(X_test_scaled, y_test, self.config["batch_size"])

        return {"train": train_loader, "test": test_loader, "scaler": self.scaler}
```

## Experiment Tracking

```python
import wandb

class ExperimentTracker:
    def __init__(self, project: str, config: dict):
        wandb.init(project=project, config=config)

    def log_metrics(self, metrics: dict, step: int = None):
        wandb.log(metrics, step=step)

    def log_model(self, model, name: str):
        wandb.save(f"{name}.pt")

    def log_artifact(self, path: str, name: str, type: str):
        artifact = wandb.Artifact(name, type=type)
        artifact.add_file(path)
        wandb.log_artifact(artifact)

    def finish(self):
        wandb.finish()
```

## Pitfalls

- Data leakage: split BEFORE preprocessing (especially scaling)
- Class imbalance: use stratified splits or weighted loss
- Pipeline determinism: set random seeds everywhere
- Caching intermediate results saves time on iteration
- Feature store vs on-the-fly: pre-computed features speed up training
