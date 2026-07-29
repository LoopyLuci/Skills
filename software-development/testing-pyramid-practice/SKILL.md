---
name: testing-pyramid-practice
description: "Use when implementing the testing pyramid strategy."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [testing-pyramid, unit-tests, integration-tests, e2e-tests, test-strategy]
    related_skills: [test-driven-development, behavior-driven-development, api-testing-patterns, mutation-testing, snapshot-testing]
---

# Testing Pyramid Practice

Implementing the testing pyramid strategy — from unit and integration through end-to-end tests, test ratios, and maintaining a healthy test suite.

## When to Use

- Designing a comprehensive testing strategy
- Balancing test types (unit, integration, e2e)
- Improving test suite speed and reliability
- Deciding what to test at each level
- Building CI/CD test pipelines

## Testing Pyramid

```python
TESTING_PYRAMID = {
    'unit': {
        'ratio': '70% of tests',
        'speed': 'Milliseconds',
        'scope': 'Single function or method',
        'goal': 'Verify business logic in isolation',
    },
    'integration': {
        'ratio': '20% of tests',
        'speed': 'Seconds',
        'scope': 'Multiple components, database, API',
        'goal': 'Verify components work together',
    },
    'e2e': {
        'ratio': '10% of tests',
        'speed': 'Minutes',
        'scope': 'Full system, UI, external dependencies',
        'goal': 'Critical user journeys work end-to-end',
    },
}

# Unit test example
def test_calculate_order_total():
    order = Order(items=[Item(price=10.0), Item(price=20.0)])
    total = calculate_total(order, tax_rate=0.1)
    assert total == 33.0  # (10 + 20) * 1.1

# Integration test example
def test_create_user_and_get_profile(db_session):
    user = User(name='Alice', email='alice@example.com')
    db_session.add(user)
    db_session.commit()
    
    profile = get_user_profile(db_session, user.id)
    assert profile['name'] == 'Alice'
```

## Common Pitfalls

1. **Too many E2E tests** — slow, flaky, expensive; use 10% as max
2. **No integration tests** — units pass individually but fail together; need integration layer
3. **Testing implementation, not behavior** — tests that break on refactoring (not behavior change) are fragile
4. **No test categorization** — can't run just unit tests quickly during development
5. **Flaky E2E tests** — flaky tests erode trust; invest in stability or replace with integration tests

## Verification Checklist

- [ ] Test ratio roughly 70/20/10 (unit/integration/e2e)
- [ ] Unit tests run in < 1 second for the full suite
- [ ] Integration tests use test containers or in-memory dependencies
- [ ] E2E tests cover only critical user journeys
- [ ] Flaky test detection and quarantine process
- [ ] CI/CD pipeline runs appropriate test level per stage
- [ ] Test coverage reports for unit tests (80%+ target)
