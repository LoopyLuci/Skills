---
name: data-pipeline-streaming
description: "Use when building streaming and batch data pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-pipeline, ETL, streaming, Kafka, Spark, Flink, batch]
    related_skills: [message-queue-patterns, event-driven-architecture, etl-pipeline-design, feature-engineering-automation]
---

# Data Pipeline and Streaming

Building batch and streaming data pipelines — from ETL/ELT design through stream processing, real-time analytics, and pipeline observability.

## When to Use

- Processing large volumes of data on schedule (batch)
- Processing data in real-time as it arrives (streaming)
- Building data lakes, data warehouses, or lakehouses
- Implementing change data capture (CDC) from databases
- Powering real-time dashboards and analytics

## Pipeline Architectures

```python
PIPELINE_ARCHITECTURES = {
    'batch_etl': 'Extract→Transform→Load in scheduled batches (hourly/daily)',
    'batch_elt': 'Extract→Load→Transform in warehouse (modern approach)',
    'streaming': 'Process events as they arrive (sub-second latency)',
    'lambda': 'Batch + streaming layers combined, merged at query time',
    'kappa': 'Everything is a stream, batch is just a replay of stream',
}

class ETLPipeline:
    """Design and monitor ETL pipelines."""
    def __init__(self, name: str, schedule: str = 'daily'):
        self.name = name
        self.schedule = schedule
        self.steps = []
    
    def add_step(self, name: str, func: callable, 
                 dependencies: list = None) -> 'ETLPipeline':
        self.steps.append({
            'name': name, 'func': func, 'deps': dependencies or [],
            'status': 'pending', 'duration': None,
        })
        return self
    
    def run(self):
        for step in self.steps:
            import time
            start = time.time()
            try:
                step['func']()
                step['status'] = 'success'
            except Exception as e:
                step['status'] = 'failed'
                raise e
            finally:
                step['duration'] = time.time() - start
```

## Common Pitfalls

1. **Schema drift** — source data changes shape and breaks pipelines; use schema-on-read
2. **Backpressure** — ingestion rate > processing rate causes unbounded growth
3. **Data quality** — garbage in, garbage out; validate at ingestion
4. **No observability** — pipeline fails silently; monitor row counts, lag, errors
5. **Reprocessing cost** — replaying weeks of data is expensive; design for selective replay

## Verification Checklist

- [ ] Source data validation at ingestion point
- [ ] Schema evolution strategy defined (Avro, Protobuf, schema registry)
- [ ] Monitoring on row counts, data lag, error rates
- [ ] Idempotent writes for safe reprocessing
- [ ] Checkpointing for streaming (offset tracking)
- [ ] Data quality checks after each stage
- [ ] Alerting for pipeline failures and data anomalies
