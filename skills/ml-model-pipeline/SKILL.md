---
name: ml-model-pipeline
title: ML Model Pipeline
description: Use when training and deploying ML models for Sentinel.
category: networking
tags: [ml, model, pipeline, training, deployment, automation]
---

# ML Model Pipeline

**Trigger**: Use when training, validating, and deploying ML models for threat detection.

**Libraries**: Python: `scikit-learn`, `xgboost`, `pytorch`, `onnx`, `optuna`

**Implementation**: Training pipeline: feature extraction from historical flow data → train XGBoost/Autoencoder → hyperparameter tuning (Optuna) → ONNX export. Validation: precision, recall, F1 on held-out test set. A/B testing: serve old model to 10% of traffic, new model to 90%. Rollback on metric degradation. Continuous retraining via scheduled pipeline.

**Connected**: `ml-threat-detection`, `gpu-anomaly-detector`, `python-orchestrator`, `traffic-analyzer`
