---
name: gpu-packet-classifier
title: GPU Packet Classifier
description: Use when offloading packet classification to GPU compute.
category: networking
tags: [gpu, packet, classify, compute, wgpu, rocm]
---

# GPU Packet Classifier

**Trigger**: Use when implementing GPU-accelerated packet classification.

**Libraries**: `wgpu` (WebGPU), `candle` (ML inference), `wgsl` (shaders)

**Implementation**: wgpu compute shaders for parallel packet header analysis. Vulkan compute on RX 7900 XTX via RADV/AMDVLK. Batch packet processing: upload buffer, dispatch compute, read results. ROCm 6.x for ML model inference. iGPU for lightweight preprocessing (Intel QuickAssist). Fallback to CPU when GPU unavailable. Shader compilation at startup.

**Connected**: `gpu-anomaly-detector`, `gpu-flow-visualizer`, `pattern-matching-engine`, `protocol-identifier`, `packet-processing-pipeline`
