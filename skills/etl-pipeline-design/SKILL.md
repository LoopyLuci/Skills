---
name: etl-pipeline-design
description: "Design ETL pipelines with error handling and idempotency"
---

# ETL Pipeline Design

## Pattern
```python
def extract():
    return fetch_from_api()

def transform(data):
    return [clean(item) for item in data]

def load(data):
    for item in data:
        upsert_to_db(item)

def run_pipeline():
    data = extract()
    cleaned = transform(data)
    load(cleaned)
```

## Idempotency
Use upsert (INSERT ON CONFLICT UPDATE) so re-running is safe.

## Error Handling
Wrap each stage in try/except, log errors, and continue.

## Incremental Loading
Track last_processed timestamp in a control table.
