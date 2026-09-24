---
name: packet-processing-pipeline
description: Use when building parallel multi-stage packet processing.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [pipeline, packet, processing, parallel, stages, throughput]
---

# Packet Processing Pipeline

**Trigger**: Use when implementing multi-stage parallel packet processing pipeline.

**Libraries**: `rayon`, `crossbeam` (channels), `tokio`, `pnet`

**Implementation**: Pipeline stages: Capture → Parse → Classify → Filter → Log → Forward. Crossbeam channels between stages for bounded backpressure. Per-stage thread pools sized to workload: capture (pinned cores), parse (rayon parallel), classify (GPU). Batch processing: collect N packets before dispatch for amortized cost. Backpressure via bounded channels: slow stage blocks fast stage.

**Connected**: `multi-queue-capture`, `packet-capture-engine`, `protocol-identifier`, `pattern-matching-engine`, `gpu-packet-classifier`, `connection-tracker`
