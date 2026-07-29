---
name: functional-programming-concepts
description: "Use when applying FP: map, reduce, monads, immutability."
category: software-development
tags: [functional, fp, map, reduce, monads, immutability]
---
# Functional Programming Concepts

Core functional programming concepts applicable across languages.

## Higher-Order Functions

```python
# map, filter, reduce
from functools import reduce

nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, nums))        # [1,4,9,16,25]
even = list(filter(lambda x: x % 2 == 0, nums))  # [2,4]
sum_all = reduce(lambda a, b: a + b, nums)        # 15

# Partial application
from functools import partial

def train(model, data, lr=0.001):
    return f"Training {model} with lr={lr}"

train_fast = partial(train, lr=0.01)
train_fast("transformer")  # "Training transformer with lr=0.01"
```

## Immutability

```python
from dataclasses import dataclass

@dataclass(frozen=True)  # immutable
class ModelConfig:
    name: str
    hidden_size: int
    num_layers: int

config = ModelConfig("bert", 768, 12)
# config.hidden_size = 1024  # FrozenInstanceError!

# Creating modified copies
import copy
new_config = copy.replace(config, num_layers=24)
```

## Monads (Rust-style Result/Option)

```python
from typing import Optional, Union, Generic, TypeVar
T = TypeVar('T')
E = TypeVar('E')

class Result(Generic[T, E]):
    def __init__(self, value=None, error=None):
        self._value = value
        self._error = error

    @classmethod
    def ok(cls, value: T) -> 'Result[T, E]':
        return cls(value=value)

    @classmethod
    def err(cls, error: E) -> 'Result[T, E]':
        return cls(error=error)

    def map(self, fn):
        if self._error: return self
        return Result.ok(fn(self._value))

    def bind(self, fn):
        if self._error: return self
        return fn(self._value)

# Usage
def train_model(config: ModelConfig) -> Result[float, str]:
    if not config.name:
        return Result.err("name required")
    return Result.ok(0.95)

result = (train_model(ModelConfig("bert", 768, 12))
    .map(lambda acc: acc * 100)
    .map(lambda pct: f"{pct:.1f}%"))
```

## Composition

```python
# Function composition
from functools import reduce

def compose(*funcs):
    def composed(x):
        return reduce(lambda v, f: f(v), reversed(funcs), x)
    return composed

normalize = compose(
    lambda x: x.lower(),
    lambda x: x.strip(),
    lambda x: x.replace('-', ' '),
)

print(normalize("  Hello-World  "))  # "hello world"
```

## Pitfalls

- Immutable data structures have overhead — measure before optimizing
- Deeply nested monads reduce readability
- Recursion can overflow stack — use trampolining or iteration
- Function composition in imperative languages can obscure control flow
- Partial application with keyword args can behave unexpectedly
