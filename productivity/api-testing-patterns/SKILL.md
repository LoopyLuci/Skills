---
name: api-testing-patterns
description: "Test REST APIs contracts auth pagination and errors"
---

# API Testing Patterns

## Basic Structure
```python
def test_create_user(client):
    resp = client.post("/users", json={"name": "Alice"})
    assert resp.status_code == 201
    assert resp.json()["name"] == "Alice"
```

## What to Test
- 200/201 for success
- 400 for validation errors
- 401/403 for auth
- 404 for not found
- Pagination: page size, cursors
- Edge cases: empty body, wrong types
