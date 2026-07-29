---
name: ml-serving-optimization
description: "Use when optimizing ML model serving and inference."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [model-serving, inference-optimization, quantization, batching, ONNX, TensorRT, Triton]
    related_skills: [ml-deployment-serving, model-compression-techniques, knowledge-distillation, ml-pipeline-design]
---

# ML Serving Optimization

Optimizing ML model serving for production — from latency reduction through throughput optimization, model compilation, and hardware-specific acceleration.

## When to Use

- Reducing inference latency for real-time applications
- Increasing throughput for batch inference
- Deploying models on resource-constrained devices
- Reducing serving infrastructure costs
- Compiling models for specific hardware (GPU, CPU, mobile, edge)

## Optimization Techniques

```python
from typing import Dict, List
import time
import numpy as np

class InferenceOptimizer:
    """Profile and optimize model inference."""
    
    OPTIMIZATION_TECHNIQUES = {
        'quantization': 'INT8/FP16 quantization reduces model size 2-4x',
        'pruning': 'Remove unimportant weights, reduces compute',
        'batching': 'Process multiple inputs simultaneously for throughput',
        'compilation': 'XLA/ONNX Runtime/TensorRT compile for target hardware',
        'caching': 'Cache frequent inference results (when deterministic)',
        'distillation': 'Smaller student model approximates larger teacher',
    }
    
    @staticmethod
    def benchmark(model, input_data, n_runs: int = 100) -> Dict:
        """Benchmark inference performance."""
        latencies = []
        for _ in range(n_runs):
            start = time.time()
            _ = model(input_data)
            latencies.append((time.time() - start) * 1000)
        
        return {
            'avg_latency_ms': round(np.mean(latencies), 2),
            'p50_ms': round(np.percentile(latencies, 50), 2),
            'p95_ms': round(np.percentile(latencies, 95), 2),
            'p99_ms': round(np.percentile(latencies, 99), 2),
            'throughput_per_sec': round(1000 / np.mean(latencies), 1),
        }
```

## Common Pitfalls

1. **Premature optimization** — optimize after profiling, not before; measure first
2. **Hardware mismatch** — optimizing for CPU but deploying on GPU; match target hardware
3. **Numerical degradation** — INT8 quantization can hurt accuracy; validate after optimization
4. **Batching side effects** — larger batches improve throughput but increase latency
5. **No load testing** — benchmark under production-like load, not just single requests

## Verification Checklist

- [ ] Baseline inference latency measured before optimization
- [ ] Optimization technique matches deployment hardware
- [ ] Accuracy validated after quantization/pruning
- [ ] Load testing with production-like traffic patterns
- [ ] Batching strategy tuned (dynamic vs static batch)
- [ ] Model compilation tested (ONNX, TensorRT)
- [ ] Cost per inference tracked (before and after optimization)
