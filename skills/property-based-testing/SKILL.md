---
name: property-based-testing
description: "Use Hypothesis to find edge cases with generated inputs"
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
