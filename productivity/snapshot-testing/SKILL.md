---
name: snapshot-testing
description: "Catch regressions with snapshot approval tests for APIs"
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
