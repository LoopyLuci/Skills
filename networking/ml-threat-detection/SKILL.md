---
name: ml-threat-detection
title: ML Threat Detection
description: Use when running ML models for network threat detection.
category: networking
tags: [ml, threat, detection, model, inference, candle, rust]
---

# ML Threat Detection

**Trigger**: Use when implementing ML-based threat detection on network flows.

**Libraries**: `candle` (Rust ML inference), `ort` (ONNX Runtime), `xgboost` (decision trees)

**Implementation**: Feature extraction: 50+ flow features (duration, packet sizes, TTL, TCP flags, inter-arrival times, entropy, protocol distribution). Models: XGBoost for fast classification, Autoencoder for anomaly detection, Random Forest for domain reputation. ONNX export for cross-runtime compatibility. Continuous learning: human feedback loop retrains model. Threat scoring 0-100.

**Connected**: `gpu-anomaly-detector`, `gpu-packet-classifier`, `pattern-matching-engine`, `traffic-analyzer`, `dns-adblock-engine`
