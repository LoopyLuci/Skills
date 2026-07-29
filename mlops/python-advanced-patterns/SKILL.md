---
name: python-advanced-patterns
description: "Use when writing advanced Python: async, decorators, metaprog."
category: mlops
tags: [python, advanced, async, decorators, metaprogramming]
---
# Python Advanced Patterns

Advanced Python: async/await, decorators, context managers, metaprogramming, descriptors.

## Async/Await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    urls = ["https://api.example.com/1", "https://api.example.com/2"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())
```

## Decorators

```python
from functools import wraps
import time

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (attempt + 1))  # exponential backoff
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2.0)
def unreliable_network_call():
    ...
```

## Context Managers

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(resource_id: str):
    print(f"Acquiring {resource_id}")
    resource = {"id": resource_id}
    try:
        yield resource
    finally:
        print(f"Releasing {resource_id}")

with managed_resource("db-conn") as conn:
    print(f"Using {conn}")
```

## Dataclasses with Validation

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ModelConfig:
    name: str
    hidden_size: int = 768
    num_layers: int = 12
    dropout: float = 0.1
    vocab_size: int = 50257
    special_tokens: List[str] = field(default_factory=list)

    def __post_init__(self):
        assert self.hidden_size > 0, "hidden_size must be positive"
        assert 0 <= self.dropout <= 1, "dropout must be in [0, 1]"
```

## Metaprogramming

```python
class AutoRegistry(type):
    _registry = {}

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if not name.startswith('Base'):
            AutoRegistry._registry[name] = new_class
        return new_class

class BaseModel(metaclass=AutoRegistry):
    pass

class TransformerModel(BaseModel): pass
class LSTMModel(BaseModel): pass

print(AutoRegistry._registry)
# {'TransformerModel': ..., 'LSTMModel': ...}
```

## Pitfalls

- Async code needs an event loop — can't call async functions directly
- Decorators lose function metadata without `@wraps`
- Dataclass `__post_init__` doesn't run for `InitVar` fields
- Metaclass conflicts when multiple metaclasses are involved
- Context managers should handle exceptions, not suppress them
