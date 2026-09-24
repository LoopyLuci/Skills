---
name: snapshot-testing
description: Catch regressions with snapshot approval tests for APIs
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [snapshot, testing]
---

# Snapshot Testing

## syrupy (Python)
```bash
pip install syrupy
```

```python
def test_api_response(snapshot):
    resp = client.get("/api/users")
    assert resp.json() == snapshot
```

## First Run
Creates snapshot file. Subsequent runs compare.

## Update Snapshots
```bash
pytest --snapshot-update
```

## Best For
- API response shapes
- Serialization output
- Error message formatting

## Trigger

Activate this skill when the user mentions:
- snapshot, testing workflows or issues
- Building, fixing, or optimizing snapshot testing


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
