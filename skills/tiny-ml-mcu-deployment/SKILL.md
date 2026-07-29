---
name: tiny-ml-mcu-deployment
description: "Use when deploying ML on microcontrollers (MCUs)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [TinyML, MCU, microcontroller, TFLite-Micro, Arduino, ESP32, CMSIS-NN]
    related_skills: [edge-ai-tinyml, on-device-ml-optimization, iot-security-framework, model-compression-techniques]
---

# TinyML — ML on Microcontrollers

Deploying ML models on microcontrollers — from TFLite Micro and Arduino through model quantization (INT8), memory optimization, and sensor integration.

## When to Use

- Running ML on battery-powered microcontrollers
- Always-on keyword spotting, gesture recognition
- Sensor data processing (IMU, temperature, vibration)
- Ultra-low-power ML inference (mW range)

## TinyML Pipeline

```python
class TinyMLPipeline:
    """Optimize ML for MCU deployment."""
    
    @staticmethod
    def convert_for_mcu(model_path: str, output_path: str,
                         arena_size_kb: int = 100) -> str:
        import tensorflow as tf
        converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8
        tflite_model = converter.convert()
        
        # Convert to C array for MCU
        c_array = f"const unsigned char model_data[] = {{\n"
        for i, byte in enumerate(tflite_model):
            c_array += f"0x{byte:02x}, "
            if (i + 1) % 16 == 0: c_array += "\n"
        c_array += "};\n"
        c_array += f"const int model_data_len = {len(tflite_model)};\n"
        
        with open(output_path, 'w') as f:
            f.write(c_array)
        return output_path
    
    @staticmethod
    def estimate_mcu_requirements(model_path: str) -> Dict:
        import os
        size = os.path.getsize(model_path)
        return {
            'flash_kb': round(size / 1024, 1),
            'ram_arena_kb': round(size / 1024 * 1.5, 1),  # Rule of thumb
            'recommended_mcu': 'Cortex-M4/M7' if size < 100*1024 else 'Cortex-M7/M85',
        }
```

## Verification Checklist

- [ ] Model quantized to INT8 (required for most MCUs)
- [ ] Model size fits MCU flash (< 512KB typical)
- [ ] Arena memory fits MCU RAM (< 256KB typical)
- [ ] Inference latency within power budget
- [ ] TFLite Micro interpreter configured for target MCU
- [ ] CMSIS-NN or equivalent optimized kernels used
- [ ] Sensor integration tested (read → inference → output)
- [ ] Power consumption measured (μA per inference)
