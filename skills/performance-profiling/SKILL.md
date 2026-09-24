---
name: performance-profiling
description: Profile Python apps with cProfile py spy and scalene
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [performance, profiling]
---

# Performance Profiling

## cProfile
```bash
python -m cProfile -o output.prof myapp.py
python -m pstats output.prof
```

## py-spy (Running Process)
```bash
pip install py-spy
py-spy record -o profile.svg --pid 12345
py-spy top --pid 12345
```

## Scalene
```bash
pip install scalene
scalene myapp.py
```

## What to Profile
- CPU hotspots (cProfile, py-spy)
- Memory allocation (tracemalloc)
- I/O bottlenecks
- Database queries
- API call latency

## Trigger

Activate this skill when the user mentions:
- performance, profiling workflows or issues
- Building, fixing, or optimizing performance profiling


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
