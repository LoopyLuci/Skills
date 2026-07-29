---
name: python-testing-advanced
description: "Use when implementing advanced Python testing."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [python, testing, pytest, fixtures, mocking, parametrize]
    related_skills: [testing-pyramid-practice, property-based-testing, behavior-driven-development]
---

# Advanced Python Testing

Implementing advanced Python testing — from pytest fixtures and conftest through mocking, parametrization, and test infrastructure.

## When to Use

- Building robust test suites with pytest
- Implementing reusable fixtures and conftest
- Mocking external dependencies
- Parametric and property-based testing

## Testing Patterns

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.close()

@pytest.mark.parametrize("input,expected", [
    (1, 2), (2, 4), (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected

class TestUserAPI:
    @patch('app.api.get_user')
    def test_get_user(self, mock_get):
        mock_get.return_value = {'id': 1, 'name': 'Test'}
        response = client.get('/users/1')
        assert response.status_code == 200
```

## Verification Checklist

- [ ] Fixture scope (function, class, module, session) chosen appropriately
- [ ] conftest.py for shared fixtures
- [ ] Mock objects for external dependencies
- [ ] Parametrize for data-driven tests
- [ ] Monkeypatch for environment modifications
- [ ] Test coverage > 80%
