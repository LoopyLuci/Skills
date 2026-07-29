---
name: python-metaclasses-descriptors
description: "Use when implementing metaclasses and descriptors."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [python, metaclass, descriptor, __new__, __init_subclass__, meta]
    related_skills: [python-typing-advanced, python-decorators-advanced, type-system-design-theory]
---

# Metaclasses and Descriptors

Implementing Python metaclasses and descriptors — from __new__ to descriptor protocol, __init_subclass__, and practical metaclass patterns.

## When to Use

- Building DSLs and APIs with metaclasses
- Implementing property-like descriptors
- Automatic registration of subclasses
- ORM-like model definitions

## Metaclass Patterns

```python
class RegistryMeta(type):
    registry = {}
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != 'BaseModel':
            mcs.registry[name] = cls
        return cls

class BaseModel(metaclass=RegistryMeta): pass

class ValidatedField:
    """Descriptor pattern."""
    def __init__(self, validator): self.validator = validator
    def __set_name__(self, owner, name): self.name = name
    def __get__(self, obj, objtype=None): return obj.__dict__.get(self.name)
    def __set__(self, obj, value):
        self.validator(value)
        obj.__dict__[self.name] = value
```

## Verification Checklist

- [ ] Metaclass __new__ vs __init__ understood
- [ ] Descriptor protocol (__get__, __set__, __delete__)
- [ ] __set_name__ for automatic naming
- [ ] __init_subclass__ as metaclass alternative (Python 3.6+)
- [ ] Practical use cases (registries, validation, ORMs)
