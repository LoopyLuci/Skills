---
name: on-device-ml-optimization
description: "Use when optimizing ML for on-device deployment."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [on-device-ML, mobile-ML, TFLite, CoreML, MLKit, NNAPI, GPU-delegate]
    related_skills: [edge-ai-tinyml, tiny-ml-mcu-deployment, ml-serving-optimization, model-compression-techniques]
---

# On-Device ML Optimization

Optimizing ML models for on-device deployment (mobile, browser, edge) — from TFLite and CoreML through hardware acceleration, model conversion, and battery-efficient inference.

## When to Use

- Running ML on mobile devices (iOS/Android)
- Browser-based ML with TensorFlow.js or ONNX Runtime Web
- Deploying models that work offline
- Privacy-preserving on-device inference

## On-Device ML Pipeline

```python
class OnDeviceOptimizer:
    """Optimize models for mobile/edge deployment."""
    
    @staticmethod
    def convert_to_tflite(model_path: str, output_path: str,
                           optimizations: List[str] = ['default']) -> str:
        import tensorflow as tf
        converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
        
        if 'default' in optimizations:
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
        if 'fp16' in optimizations:
            converter.target_spec.supported_types = [tf.float16]
        if 'edgetpu' in optimizations:
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        
        tflite_model = converter.convert()
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        return output_path
    
    @staticmethod
    def benchmark(model_path: str, n_runs: int = 50) -> Dict:
        import time, numpy as np
        import tflite_runtime.interpreter as tflite
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        
        input_details = interpreter.get_input_details()
        latencies = []
        for _ in range(n_runs):
            start = time.time()
            interpreter.set_tensor(input_details[0]['index'], np.random.rand(*input_details[0]['shape']).astype(np.float32))
            interpreter.invoke()
            latencies.append((time.time() - start) * 1000)
        
        return {'avg_ms': round(np.mean(latencies), 2), 'p95_ms': round(np.percentile(latencies, 95), 2)}
```

## Verification Checklist

- [ ] Model converted to target format (TFLite, CoreML, ONNX)
- [ ] Hardware acceleration enabled (GPU, NPU, DSP delegates)
- [ ] Model size optimized (< 10MB for mobile download)
- [ ] Inference latency < 30ms for real-time use cases
- [ ] Battery impact measured (mAh per 1000 inferences)
- [ ] Offline capability verified (no network required)
- [ ] Model updates via app store or on-device download
