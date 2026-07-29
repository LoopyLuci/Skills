---
name: performance-optimization
description: "Use when optimizing code and system performance."
category: software-development
tags: [performance, optimization, profiling, benchmarking]
---
# Performance Optimization

Systematic approach to profiling, identifying bottlenecks, and optimizing performance.

## The 80/20 Rule

- 80% of execution time spent in 20% of code
- Profile first, optimize second — never guess about bottlenecks
- Measure before and after every change

## Profiling Python

```python
# cProfile (built-in)
python -m cProfile -o profile.out my_script.py

# Analyze profile
import pstats
p = pstats.Stats('profile.out')
p.sort_stats('cumtime').print_stats(20)  # top 20 by cumulative time
p.sort_stats('time').print_stats(20)     # top 20 by time per call

# line_profiler (per-line timing)
# pip install line_profiler
@profile
def slow_function():
    for i in range(1000000):
        _ = i ** 2

# kernprof -l -v my_script.py

# memory_profiler
# pip install memory_profiler
@profile
def memory_hungry():
    data = [i for i in range(1000000)]
```

## Profiling C++

```cpp
// Built-in timing
#include <chrono>
auto start = std::chrono::high_resolution_clock::now();
// ... code ...
auto end = std::chrono::high_resolution_clock::now();
auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();

// Perf (Linux/WSL2)
// perf stat ./myapp
// perf record ./myapp && perf report

// Very Sleepy (Windows GUI profiler)
// https://www.codersnotes.com/sleepy/

// Tracy (frame profiler)
// https://github.com/GPUOpen-Tools/tracy
```

## Common Optimization Patterns

```python
# 1. Use local variables (avoid attribute lookup)
# SLOW
def process(data):
    for i in range(len(data)):
        data[i] = data[i] * 2
# FAST
def process(data):
    local_data = data
    multiply = 2
    for i in range(len(local_data)):
        local_data[i] = local_data[i] * multiply

# 2. List comprehension vs loop
squares = [x**2 for x in range(1000)]  # faster than for-loop

# 3. Set membership (O(1)) vs list (O(n))
valid = {"docker", "podman", "containerd"}  # set
if name in valid:  # O(1)

# 4. Generator vs list (memory)
def read_large_file():
    for line in open("huge.log"):
        yield process(line)  # lazy, not loading all at once
```

## C++ Optimization

```cpp
// 1. Pass by reference
void process(const std::vector<float>& data);  // no copy

// 2. Reserve capacity
std::vector<int> v;
v.reserve(1000000);  // one allocation instead of many

// 3. Move semantics
std::vector<int> createData() {
    std::vector<int> result(1000000);
    return result;  // move (not copy) in C++11+
}

// 4. constexpr (compile-time evaluation)
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}
std::array<int, factorial(5)> arr;  // computed at compile time

// 5. Fast math
-ffast-math  // relaxes IEEE compliance for speed (GCC/Clang)

// 6. Link-time optimization
-flto -fuse-linker-plugin  // cross-module optimization
```

## Memory Optimization

```python
# Python: __slots__ reduces instance memory
class Point:
    __slots__ = ('x', 'y')  # no __dict__ overhead
    def __init__(self, x, y):
        self.x, self.y = x, y

# NumPy: pre-allocate, don't append
arr = np.zeros((1000, 1000))  # pre-allocated
# vs arr = np.array([]); arr = np.append(arr, ...)  # reallocates each time

# Rust: stack allocation
fn process() {
    let arr: [f32; 1000] = [0.0; 1000];  // stack allocated
    let vec: Vec<f32> = Vec::with_capacity(1000);  // heap, pre-reserved
}
```

## I/O Optimization

```python
# Buffer reads (not line-by-line)
with open("large_file.bin", "rb") as f:
    while chunk := f.read(8192):  # 8KB buffer
        process(chunk)

# Async I/O for concurrent reads
import asyncio
async def read_all(files):
    async with aiofiles.open("file.txt") as f:
        content = await f.read()
```

## Pitfalls

- Premature optimization is the root of all evil — profile first
- Micro-benchmarks don't reflect real workloads — test end-to-end
- Compiler optimizations (-O2, -O3) can change behavior — test thoroughly
- Memory vs speed tradeoff — caching speeds up but uses memory
- One bottleneck fix moves the bottleneck elsewhere — iterate profiling
