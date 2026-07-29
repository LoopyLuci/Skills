---
name: model-evaluation-metrics
description: "Use when evaluating ML model performance."
category: mlops
tags: [ml, evaluation, metrics, classification, regression]
---
# Model Evaluation Metrics

Selecting and interpreting evaluation metrics for ML models.

## Classification Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, log_loss,
)

y_true = [0, 1, 1, 0, 1, 0, 1, 0, 0, 1]
y_pred = [0, 1, 0, 0, 1, 0, 1, 0, 1, 1]

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
cm = confusion_matrix(y_true, y_pred)
report = classification_report(y_true, y_pred)

print(f"Accuracy:  {accuracy:.3f}")
print(f"Precision: {precision:.3f}  (TP / (TP+FP))")
print(f"Recall:    {recall:.3f}     (TP / (TP+FN))")
print(f"F1:        {f1:.3f}  (harmonic mean of P and R)")
```

## Regression Metrics

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

y_true = [1.0, 2.0, 3.0, 4.0, 5.0]
y_pred = [1.1, 1.9, 3.2, 3.8, 5.1]

mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
mape = np.mean(np.abs((np.array(y_true) - np.array(y_pred)) / np.array(y_true))) * 100

# When to use:
# MSE: penalizes large errors (outliers distort)
# MAE: robust to outliers
# RMSE: interpretable in original units
# R2: proportion of variance explained (0-1, higher better)
# MAPE: percentage error (interpretable across scales)
```

## When to Use Which Metric

| Scenario | Primary Metric | Secondary |
|----------|---------------|-----------|
| Balanced classes | Accuracy | F1 macro |
| Imbalanced classes | F1 weighted | Precision-Recall AUC |
| Fraud detection | Recall | Precision @ threshold |
| Medical diagnosis | Recall (don't miss) | F1 |
| Regression (normal) | RMSE | R2 |
| Regression (outliers) | MAE | MAPE |
| Ranking | NDCG@k | MRR |
| LLM generation | BLEU, ROUGE | Perplexity |
| Embedding quality | Retrieval recall@k | mAP |

## LLM-Specific Evaluation

```python
# Perplexity (lower is better)
import torch
def perplexity(model, tokenizer, text: str) -> float:
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
    return torch.exp(loss).item()

# Generation quality
from evaluate import load
bleu = load("bleu")
rouge = load("rouge")
bertscore = load("bertscore")

# BLEU: precision-based, good for translation
# ROUGE: recall-based, good for summarization
# BERTScore: semantic similarity, good for open-ended generation
```

## Pitfalls

- Accuracy is misleading for imbalanced classes — use precision/recall
- RMSE in same units as target — easy to interpret but sensitive to outliers
- Cross-validation metrics are distributions, not point estimates
- Test set must match production distribution — concept drift invalidates metrics
- Multiple metrics can conflict — define a primary metric for model selection
