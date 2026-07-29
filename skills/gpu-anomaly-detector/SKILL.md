---
name: gpu-anomaly-detector
title: GPU Anomaly Detector
description: Use when running ML threat detection on GPU.
category: networking
tags: [gpu, anomaly, detection, ml, inference, candle]
---

# GPU Anomaly Detector

**Trigger**: Use when implementing GPU-accelerated ML-based anomaly detection.

**Libraries**: `candle` (Rust ML), `wgpu`, `ort` (ONNX Runtime)

**Implementation**: ONNX model inference on GPU via `candle` with CUDA/ROCm backend. Autoencoder for traffic baseline anomaly detection. Feature extraction: flow duration, packet sizes, inter-arrival times, protocol mix, port distribution. Batch inference: 1024 flows per GPU dispatch. Anomaly thresholds calibrated per network profile. Real-time alert on deviation >3sigma.

**Connected**: `gpu-packet-classifier`, `ml-threat-detection`, `traffic-analyzer`, `connection-tracker`, `pattern-matching-engine`
