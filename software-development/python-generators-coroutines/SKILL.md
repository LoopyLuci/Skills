---
name: python-generators-coroutines
description: "Use when implementing Python generators and coroutines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [python, generators, yield, coroutines, send, yield-from]
    related_skills: [python-async-patterns, python-decorators-advanced, data-pipeline-streaming]
---

# Python Generators and Coroutines

Implementing Python generators — from generator expressions through yield from, send/throw/close, and bidirectional coroutines.

## When to Use

- Processing data streams with generator pipelines
- Implementing coroutines for cooperative multitasking
- Lazy evaluation and infinite sequences
- Data pipeline composition

## Generator Patterns

```python
def pipeline(*steps):
    """Chain generator functions."""
    def run(initial):
        result = initial
        for step in steps:
            result = step(result)
        return result
    return run

def read_chunks(file, size=8192):
    while True:
        chunk = file.read(size)
        if not chunk: break
        yield chunk

def grep(pattern):
    """Bidirectional coroutine generator."""
    while line := (yield):
        if pattern in line:
            yield line
```

## Verification Checklist

- [ ] Generator expressions vs list comprehensions
- [ ] yield from for subgenerator delegation
- [ ] .send() for bidirectional communication
- [ ] Generator pipeline composition
- [ ] Memory-efficient large data processing
