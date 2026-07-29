---
name: packet-processing-pipeline
title: Packet Processing Pipeline
description: Use when building parallel multi-stage packet processing.
category: networking
tags: [pipeline, packet, processing, parallel, stages, throughput]
---

# Packet Processing Pipeline

**Trigger**: Use when implementing multi-stage parallel packet processing pipeline.

**Libraries**: `rayon`, `crossbeam` (channels), `tokio`, `pnet`

**Implementation**: Pipeline stages: Capture → Parse → Classify → Filter → Log → Forward. Crossbeam channels between stages for bounded backpressure. Per-stage thread pools sized to workload: capture (pinned cores), parse (rayon parallel), classify (GPU). Batch processing: collect N packets before dispatch for amortized cost. Backpressure via bounded channels: slow stage blocks fast stage.

**Connected**: `multi-queue-capture`, `packet-capture-engine`, `protocol-identifier`, `pattern-matching-engine`, `gpu-packet-classifier`, `connection-tracker`
