---
name: code-migration-patterns
description: "Safe code migration rename split deprecate and refactor"
---

# Code Migration Patterns

## Rename Symbol
1. Add deprecated alias pointing to new name
2. Update all internal references
3. Remove old name in next release

```python
import warnings
def old_name():
    warnings.warn("Use new_name", DeprecationWarning)
    return new_name()
```

## Split Module
1. Create new module with extracted code
2. Re-export from old module with deprecation
3. Update imports gradually

## Safe Steps
1. Add deprecation warnings
2. Run: python -Wd
3. Fix all warnings
4. Remove deprecated code in next version
