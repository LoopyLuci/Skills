---
name: multi-queue-capture
title: Multi-Queue Capture
description: Use when distributing packet capture across CPU cores.
category: networking
tags: [packet, capture, multi-queue, rss, parallel, performance]
---

# Multi-Queue Capture

**Trigger**: Use when distributing packet capture across multiple CPU cores for 24-thread utilization.

**Libraries**: `pcap`, `pnet`, `rayon`, `crossbeam`

**Implementation**: RSS (Receive Side Scaling) affinity: one capture thread per NIC queue pinned to dedicated core. Ring buffer per queue with lock-free SPSC channel. Flow hashing for consistent queue assignment (RSS Toeplitz hash). NUMA-aware memory allocation. Batch processing: process N packets per dispatch for amortized overhead. Zero-copy between queue and processor.

**Connected**: `packet-capture-engine`, `packet-processing-pipeline`, `gpu-packet-classifier`, `connection-tracker`, `parallel`
