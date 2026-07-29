---
name: go-concurrency-patterns
description: "Use when implementing Go concurrency patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [go, goroutines, channels, select, sync, concurrency, pipeline]
    related_skills: [message-queue-patterns, concurrency-parallelism, data-pipeline-streaming]
---

# Go Concurrency Patterns

Implementing Go concurrency patterns — from goroutines and channels through pipelines, fan-out/in, and advanced sync primitives.

## When to Use

- Building concurrent Go applications
- Implementing worker pools and pipelines
- Managing goroutine lifecycles
- Synchronization with channels and mutexes

## Concurrency Patterns

```go
// Pipeline pattern
func gen(nums ...int) <-chan int {
    out := make(chan int)
    go func() { for _, n := range nums { out <- n }; close(out) }()
    return out
}

func sq(in <-chan int) <-chan int {
    out := make(chan int)
    go func() { for n := range in { out <- n * n }; close(out) }()
    return out
}

// Fan-out / Fan-in
func merge(cs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)
    output := func(c <-chan int) {
        for n := range c { out <- n }
        wg.Done()
    }
    wg.Add(len(cs))
    for _, c := range cs { go output(c) }
    go func() { wg.Wait(); close(out) }()
    return out
}
```

## Verification Checklist

- [ ] Goroutine lifecycle managed (no leaks)
- [ ] Channel directions (send/receive) restricted
- [ ] select with default for non-blocking
- [ ] sync.WaitGroup for goroutine coordination
- [ ] Context for cancellation and deadlines
- [ ] errgroup for error propagation
