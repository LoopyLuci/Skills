---
name: property-based-testing
description: Use Hypothesis to find edge cases with generated inputs
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [property, based, testing]
---

# Property-Based Testing

## Install
```bash
pip install hypothesis
```

## Example
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    result = sorted(sorted(lst))
    assert result == sorted(lst)
```

## Strategies
- `st.integers()` - integers
- `st.text()` - strings
- `st.lists(st.integers())` - lists
- `st.dictionaries(st.text(), st.integers())` - dicts

## Trigger

Activate this skill when the user mentions:
- property, based, testing workflows or issues
- Building, fixing, or optimizing property based testing


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
