---
name: edge-ai-tinyml
description: "Use when deploying ML models to edge devices."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [edge-ai, tinyML, TensorFlow-Lite, ONNX-Runtime, MCU, embedded-ml]
    related_skills: [tiny-ml-mcu-deployment, on-device-ml-optimization, ml-serving-optimization, ml-deployment-serving]
---

# Edge AI and TinyML

Deploying ML models to edge devices — from model optimization (quantization, pruning) through TensorFlow Lite Micro, ONNX Runtime, and deployment on MCUs and edge hardware.

## When to Use

- Running ML models on resource-constrained devices
- Reducing cloud dependency and latency
- Privacy-preserving on-device inference
- IoT sensor data processing at the edge

## Edge ML Pipeline

```python
class EdgeMLOptimizer:
    """Optimize models for edge deployment."""
    
    @staticmethod
    def quantize_to_int8(model_path: str, output_path: str, 
                          representative_dataset) -> str:
        import tensorflow as tf
        converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = representative_dataset
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        tflite_model = converter.convert()
        
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        return output_path
    
    @staticmethod
    def estimate_memory(model_path: str) -> Dict:
        import os
        size = os.path.getsize(model_path)
        return {'model_size_bytes': size, 'model_size_kb': round(size / 1024, 1)}
```

## Verification Checklist

- [ ] Quantization method chosen (INT8, FP16) for target hardware
- [ ] Model fits within edge device memory (RAM + flash)
- [ ] Inference latency acceptable for use case
- [ ] Accuracy validated post-quantization
- [ ] Hardware support verified (TFLite Micro, ONNX Runtime, or vendor SDK)
- [ ] Power consumption measured (battery-powered devices)
- [ ] OTA update mechanism for model updates
