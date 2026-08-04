---
name: debugging-techniques-advanced
description: "Use when doing advanced debugging and root cause analysis."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [debugging, reverse-debugging, rr, gdb, post-mortem, tracing]
    related_skills: [systematic-debugging, advanced-version-control-git, performance-optimization, node-inspect-debugger]
---

# Advanced Debugging Techniques

Beyond print-debugging — reverse debugging, time-travel, core dump analysis, tracing, and systematic root cause analysis.

## When to Use

- Bugs that are hard to reproduce consistently (race conditions, heisenbugs)
- Crashes that only occur in production
- Performance regressions needing profiling
- Memory corruption or undefined behavior
- Complex multi-threaded or distributed system bugs

## Systematic Root Cause Analysis

### The Scientific Method

```python
def debug_systematically(failure_scenario):
    """
    1. HYPOTHESIS: Form a hypothesis about the root cause
    2. PREDICTION: Predict what will happen if hypothesis is true
    3. EXPERIMENT: Design minimal experiment to test
    4. OBSERVE: Run and collect data
    5. CONFIRM/REFUTE: Does evidence support or reject hypothesis?
    """
    
    techniques = [
        'reproduce_minimally',    # Simplest input that triggers bug
        'binary_search_history',  # git bisect to find regression
        'add_assertions',         # Contract checking
        'enable_logging',         # Targeted log points
        'check_recent_changes',   # What changed near regression time
        'isolate_component',      # Test component in isolation
    ]
```

## Time-Travel Debugging (rr)

```bash
# rr — record and replay execution (Linux)
# Record: captures all non-determinism
rr record ./my_program --arg1 value

# Replay
rr replay

# Reverse-continue in gdb within rr
# reverse-continue  — go back to previous crash
# reverse-step      — step backward
# reverse-next      — step over backward

# Watchpoint + reverse-continue to find when variable changed
watch -l my_variable
reverse-continue
# Lands exactly on the instruction that modified the variable

# Randomize thread scheduling to surface race conditions
rr record --chaos
```

## Core Dump Analysis

```bash
# Enable core dumps
ulimit -c unlimited
echo "/tmp/core.%e.%p" | sudo tee /proc/sys/kernel/core_pattern

# Analyze with gdb
gdb ./my_program /tmp/core.my_program.12345

# In gdb:
# bt              — backtrace (call stack)
# bt full         — backtrace with local variables
# frame 3         — switch to frame 3
# info locals     — show local variables
# p variable      — print variable
```

## Python Advanced Debugging

### Post-Mortem on Exception

```python
import sys, traceback, pdb

def post_mortem_on_error():
    """Enter pdb on any unhandled exception."""
    def excepthook(type, value, tb):
        traceback.print_exception(type, value, tb)
        pdb.post_mortem(tb)
    sys.excepthook = excepthook
```

### Memory Leak Detection

```python
import tracemalloc
import objgraph

class MemoryDebugger:
    @staticmethod
    def start(): tracemalloc.start()
    
    @staticmethod
    def show_top(n=10):
        snapshot = tracemalloc.take_snapshot()
        for stat in snapshot.statistics('lineno')[:n]:
            print(f"{stat.count:6d} × {stat.size_kb:8.1f} KB")
    
    @staticmethod
    def show_growth():
        """Show memory growth since last call."""
        current = tracemalloc.take_snapshot()
        if hasattr(MemoryDebugger, '_last'):
            for d in current.compare_to(MemoryDebugger._last, 'lineno')[:10]:
                print(f"{d.size_diff:8.1f} KB {d.count_diff:4d}")
        MemoryDebugger._last = current
```

## Rust Debugging

```rust
// Set for full backtraces
// RUST_BACKTRACE=1
// RUST_LIB_BACKTRACE=1

// dbg! macro — prints file, line, and value
fn example() {
    let x = 42;
    let y = dbg!(x * 2);  // [src/main.rs:4] x * 2 = 84
}
```

## Common Pitfalls

1. **Heisenbugs** — logging/printing changes timing; use rr for time-sensitive bugs
2. **Not minimizing the repro case** — debugging in full system is slow; isolate
3. **Confirmation bias** — actively try to disprove your hypothesis
4. **Skipping binary search** — git bisect finds the offending commit in O(log n) steps
5. **No core dumps** — a crash without a dump is lost information; enable them
6. **Production debug overhead** — don't run heavy debuggers in prod; use post-mortem

## Verification Checklist

- [ ] Reproducer minimized to simplest possible input
- [ ] Git bisect identified the regression commit
- [ ] Core dumps enabled and retrievable in production
- [ ] Root cause confirmed (changing the cause changes the symptom)
- [ ] Fix verified by tests
- [ ] Regression test added

## See Also

- systematic-debugging — structured 4-phase debugging
- advanced-version-control-git — using bisect
- performance-optimization — profiling
- node-inspect-debugger — Node.js debugging
