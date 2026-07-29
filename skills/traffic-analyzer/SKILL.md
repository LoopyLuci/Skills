---
name: traffic-analyzer
title: Traffic Analyzer
description: Use when analyzing traffic patterns and protocol mix.
category: networking
tags: [traffic, analysis, protocol, patterns, stats, rust]
---

# Traffic Analyzer

**Trigger**: Use when analyzing traffic patterns, protocol distribution, and trends.

**Libraries**: `protocol-identifier`, `connection-tracker`, `bandwidth-monitor`

**Implementation**: Protocol distribution pie chart data: % of traffic per protocol. Top talkers: IPs with highest bandwidth usage. Traffic growth trends: daily/weekly comparisons. Anomaly detection: traffic spikes outside normal patterns. Protocol transition tracking (HTTP→HTTPS migration). Export: JSON, Prometheus metrics, Grafana dashboard.

**Connected**: `connection-tracker`, `bandwidth-monitor`, `protocol-identifier`, `realtime-dashboard`, `traffic-historical`, `ml-threat-detection`
