---
name: performance-profiling
description: "Profile Python apps with cProfile py spy and scalene"
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
