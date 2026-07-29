---
name: gpu-flow-visualizer
title: GPU Flow Visualizer
description: Use when rendering network flow graphs on GPU.
category: networking
tags: [gpu, visualization, flow, graph, rendering, wgpu]
---

# GPU Flow Visualizer

**Trigger**: Use when rendering network flow topology graphs using GPU compute.

**Libraries**: `wgpu` (rendering), `wgsl` (shaders), `petgraph` (graph layout)

**Implementation**: Force-directed graph layout computed on GPU via wgpu compute shaders. Flow topology: nodes = IPs, edges = connections. Edge weight = traffic volume (animated thickness). Time-animated playback of network activity. GPU renders at 60fps for smooth interaction. Zoom/pan interaction via camera matrix. Export as SVG/PNG snapshot.

**Connected**: `gpu-packet-classifier`, `connection-tracker`, `traffic-analyzer`, `realtime-dashboard`
