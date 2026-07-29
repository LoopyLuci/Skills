---
name: concurrency-parallelism
description: "Use when writing concurrent or parallel code."
category: software-development
tags: [concurrency, parallelism, threads, async, multiprocessing]
---
# Concurrency & Parallelism

Patterns for concurrent and parallel programming across languages.

## CPU-Bound vs I/O-Bound

| Type | Python | Rust | C++ |
|------|--------|------|-----|
| I/O-bound | `asyncio` | `tokio` | `std::async` |
| CPU-bound | `multiprocessing` | `std::thread` | `std::thread` |
| Mixed | `concurrent.futures` | `rayon` + `tokio` | TBB |

## Python

```python
# CPU-bound: multiprocessing
from multiprocessing import Pool

def train_model(config: dict) -> float:
    return train(config)

with Pool(processes=4) as pool:
    configs = [{"lr": 0.001}, {"lr": 0.01}, {"lr": 0.1}, {"lr": 1.0}]
    results = pool.map(train_model, configs)

# I/O-bound: asyncio
import asyncio
import aiohttp

async def fetch_model(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def main():
    urls = [f"https://api.example.com/models/{i}" for i in range(10)]
    return await asyncio.gather(*[fetch_model(u) for u in urls])
```

## Rust

```rust
// CPU-bound: rayon
use rayon::prelude::*;

fn train_models(configs: Vec<Config>) -> Vec<f32> {
    configs.par_iter().map(|c| train(c)).collect()
}

// I/O-bound: tokio
#[tokio::main]
async fn main() -> Result<()> {
    let client = reqwest::Client::new();
    let urls = vec!["https://api.example.com/model/1"];
    let responses = futures::future::join_all(
        urls.iter().map(|url| client.get(*url).send())
    ).await;
    Ok(())
}
```

## Thread Safety

```python
# Python: threading.Lock
import threading
lock = threading.Lock()
shared_counter = 0

def increment():
    global shared_counter
    with lock:
        shared_counter += 1

# Rust: Send + Sync traits (enforced at compile time)
use std::sync::{Arc, Mutex};
let counter = Arc::new(Mutex::new(0));
let c = counter.clone();
std::thread::spawn(move || {
    let mut num = c.lock().unwrap();
    *num += 1;
});

# C++: std::mutex
std::mutex mtx;
int counter = 0;
std::thread t([&] { std::lock_guard<std::mutex> lock(mtx); counter++; });
```

## Pitfalls

- GIL in Python prevents true parallel CPU work in threads
- Data races cause undefined behavior in C++ and Rust (Rust prevents at compile time)
- Async code needs an event loop — can't block in async functions
- Deadlocks: always acquire locks in the same order
- Thread pool size = number of CPU cores for CPU-bound, higher for I/O-bound
