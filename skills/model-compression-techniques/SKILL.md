---
name: model-compression-techniques
description: "Use when compressing models: pruning, quantization, distillation."
category: mlops
tags: [model-compression, pruning, quantization, distillation]
---
# Model Compression Techniques

Reducing model size and inference cost through compression.

## Pruning

```python
import torch
import torch.nn.utils.prune as prune

# Magnitude pruning (remove smallest weights)
model = YourModel()
prune.l1_unstructured(model.layer, name='weight', amount=0.5)
# 50% of weights with smallest magnitude → 0

# Structured pruning (remove entire neurons/channels)
prune.ln_structured(model.conv, name='weight', amount=0.3, n=2, dim=0)

# Remove pruning reparameterization for deployment
prune.remove(model.layer, 'weight')

# Iterative pruning (prune → retrain → prune → ...)
for sparsity in [0.1, 0.2, 0.3, 0.4, 0.5]:
    prune.l1_unstructured(model.layer, 'weight', sparsity - current_sparsity)
    train(model, epochs=5)  # fine-tune
```

## Quantization

```python
# Post-Training Quantization (PTQ)
import torch.quantization as quant

# Static quantization (weights + activations, needs calibration)
model.eval()
model.qconfig = quant.default_qconfig  # 8-bit symmetric
quant.prepare(model, inplace=True)
# Calibrate with representative data
quant.convert(model, inplace=True)

# Dynamic quantization (weights only, no calibration)
quantized_model = quant.quantize_dynamic(
    model, {nn.Linear, nn.LSTM}, dtype=torch.qint8
)

# Quantization-Aware Training (QAT) — higher accuracy
model.train()
model.qconfig = quant.get_default_qat_qconfig('fbgemm')
quant.prepare_qat(model, inplace=True)
train(model, dataloader)
quant.convert(model, inplace=True)
```

## Knowledge Distillation

```python
class DistillationLoss:
    def __init__(self, teacher, student, T=4.0, alpha=0.7):
        self.teacher = teacher
        self.student = student
        self.T = T  # temperature
        self.alpha = alpha  # weight for distillation loss

    def __call__(self, x, labels):
        with torch.no_grad():
            teacher_logits = self.teacher(x)

        student_logits = self.student(x)

        # Hard loss (standard cross-entropy)
        hard_loss = F.cross_entropy(student_logits, labels)

        # Soft loss (match teacher distributions)
        soft_student = F.log_softmax(student_logits / self.T, dim=-1)
        soft_teacher = F.softmax(teacher_logits / self.T, dim=-1)
        soft_loss = F.kl_div(soft_student, soft_teacher, reduction='batchmean')
        soft_loss = soft_loss * (self.T ** 2)

        return self.alpha * soft_loss + (1 - self.alpha) * hard_loss
```

## Practical Compression Guide

```
1. Start with dynamic quantization (easiest, no data needed)
2. Add pruning (iterative, 50-80% sparsity)
3. Add PTQ if accuracy still acceptable
4. Try distillation if compression hurts quality
5. QAT as last resort (most effort, best accuracy)
```

## Pitfalls

- Pruning with high sparsity (>90%) needs sparse hardware support
- INT8 quantization has ±2% accuracy loss typically
- Structured pruning is more hardware-friendly than unstructured
- Distillation is sensitive to temperature — optimal T is task-dependent
- Mixed precision (FP16) is always safe and gives ~2x speedup
