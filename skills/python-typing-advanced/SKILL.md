---
name: python-typing-advanced
description: "Use when implementing advanced Python typing patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [python, typing, generics, Protocol, TypeVar, mypy]
    related_skills: [python-decorators-advanced, python-generators-coroutines, type-system-design-theory]
---

# Advanced Python Typing

Implementing advanced Python typing — from generics and protocols through variadic generics, type narrowing, and mypy strict mode.

## When to Use

- Type-safe Python codebases at scale
- Generic functions and classes
- Structural subtyping with Protocol
- Custom type guards and narrowing

## Typing Patterns

```python
from typing import TypeVar, Protocol, Generic, overload

T = TypeVar('T')
S = TypeVar('S')

class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...

class Stack(Generic[T]):
    def __init__(self): self.items: list[T] = []
    def push(self, item: T) -> None: self.items.append(item)
    def pop(self) -> T: return self.items.pop()

@overload
def process(x: int) -> str: ...
@overload
def process(x: str) -> int: ...
def process(x):
    if isinstance(x, int): return str(x)
    return int(x)
```

## Verification Checklist

- [ ] TypeVar for generic functions and classes
- [ ] Protocol for structural subtyping
- [ ] @overload for type-specific signatures
- [ ] Literal, TypedDict, Final type constructs
- [ ] mypy --strict compliance
