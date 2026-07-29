---
name: traffic-historical
title: Traffic Historical Analysis
description: Use when storing and querying historical traffic data.
category: networking
tags: [traffic, historical, storage, timeseries, query, analytics]
---

# Traffic Historical Analysis

**Trigger**: Use when implementing long-term traffic data storage and querying.

**Libraries**: InfluxDB/TimescaleDB (storage), `sqlx` (query), `arrow`/`parquet` (columnar)

**Implementation**: Time-series database for flow records with retention policies. Downsampling: raw 1s → 1m → 1h → 1d aggregates. SQL queries for historical trends, capacity planning, forensics. Parquet export for long-term cold storage. Grafana dashboard integration. Data retention: configurable per granularity (30d raw, 1yr hourly, forever daily). Query API: date range, filter by IP/protocol/port.

**Connected**: `traffic-analyzer`, `bandwidth-monitor`, `connection-monitor`, `realtime-dashboard`, `ml-model-pipeline`
