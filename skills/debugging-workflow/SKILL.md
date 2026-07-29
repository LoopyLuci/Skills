---
name: debugging-workflow
description: "Use for debugging. Systematic: reproduce, isolate, fix."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [programming, debugging, troubleshooting, bugs, root-cause-analysis]
    related_skills: [code-review-checklist, refactoring-playbook, performance-profiling]
---

# Debugging Workflow

## Overview

A systematic, scientific-method approach to debugging. Covers the full lifecycle from reproduction through root cause analysis to fix verification. Techniques include: binary search through commits, log analysis, exception chain inspection, differential testing, hypothesis-driven debugging, 5 Whys, fishbone diagrams, and the scientific method applied to software defects.

## When to Use

- An intermittent bug that's hard to reproduce
- A regression introduced in a recent deployment
- A crash or error with an unclear stack trace
- Performance degradation with no obvious cause
- A bug reported by a user that you cannot reproduce
- Legacy code where the root cause is buried
- Race conditions or timing-related failures

## Workflow

### Phase 1: Reproduce & Characterize

Before anything else, reliably reproduce the issue.

```bash
# 1. Capture the exact environment
echo "OS: $(uname -a)"
echo "Python: $(python --version 2>&1)"
echo "Node: $(node --version 2>&1)"
echo "Git commit: $(git rev-parse HEAD)"
git status --short

# 2. Check for uncommitted changes
git diff HEAD > /tmp/uncommitted_changes.patch

# 3. Capture environment variables (redact secrets)
env | grep -v -E '(SECRET|KEY|PASSWORD|TOKEN|AUTH)' | sort > /tmp/env_snapshot.txt

# 4. Check logs around the failure time
journalctl --since "5 minutes ago" --no-pager 2>/dev/null || \
  tail -100 /var/log/syslog 2>/dev/null || \
  tail -100 /var/log/app/error.log 2>/dev/null || \
  echo "No system logs found"

# 5. Record the exact error message (complete, not summary)
python -c "
import traceback, sys
# Capture the full traceback, not just the last line
try:
    # reproduce the bug
    buggy_function()
except Exception:
    traceback.print_exc()
"
```

**Reproduction checklist:**
- [ ] Can I reproduce it 3 times in a row? (If no, it's intermittent → Phase 2 stress testing)
- [ ] Does it happen in production but not development? (Environment mismatch)
- [ ] Does it happen with specific data only? (Data-dependent bug)
- [ ] Does it happen at a specific time? (Scheduled job, rate limit, cache expiry)
- [ ] Can I write a unit test that fails with this bug? (Gold standard for verification)

### Phase 2: Isolate (Narrow the Search Space)

**Technique A: Binary Search Through Commits**

```bash
# Find the commit that introduced the regression
# 1. Bisect start
git bisect start

# 2. Mark current commit as bad
git bisect bad

# 3. Mark a known-good commit (e.g., last release tag)
git bisect good v1.2.0

# 4. Git will checkout commits in the middle — test each:
pytest tests/test_bug.py -x  # should fail on bad, pass on good
git bisect good  # if the bug is NOT present
git bisect bad   # if the bug IS present

# 5. When done:
git bisect reset
echo "First bad commit: $(git log --oneline -1)"

# Alternative: quick manual binary search
git log --oneline | nl | tail -50
# Pick midpoint, checkout, test, narrow by half
```

**Technique B: Comment Out & Binary Chop**

```python
# In the function, remove half the code at a time
def buggy_function(data):
    # Block A — comment out
    # result = step_one(data)
    # if not result: return None

    # Block B
    processed = step_two(data)  # ← Keep

    # Does it still fail? If yes, bug is in B.
    # If no (failure goes away), bug is in A.
    # Repeat on the offending half.
    return processed
```

**Technique C: Differential Testing**

```bash
# Compare working vs failing inputs
# Capture both
curl https://api.example.com/v1/endpoint -d '{"valid": true}' > /tmp/good_response.json
curl https://api.example.com/v1/endpoint -d '{"valid": false}' > /tmp/bad_response.json

# Diff the code paths
# Use strace, ltrace, or logging
strace -f -e trace=network python run.py 2>&1 | head -100
```

### Phase 3: Root Cause Analysis

**The 5 Whys Technique:**

```
Symptom: User gets 500 error when checking out.

Why 1: Payment gateway returns "card_declined" but the app returns 500 instead of 402.
Why 2: The exception handler catches all PaymentErrors but not GatewayTimeoutError.
Why 3: GatewayTimeoutError inherits from BaseException, not PaymentError.
Why 4: The third-party SDK changed their exception hierarchy in v2.0.
Why 5: The SDK upgrade (PR #1423) didn't include a changelog review.
→ Root cause: SDK upgrade process lacks mandatory changelog diff review.
```

**Fishbone (Ishikawa) Diagram for Debugging:**

```text
Environment          Code                    Data
  ────────────    ──────────────        ─────────────
  Python 3.12   │  Missing null check │   Empty string
  Docker image  │  Wrong enum value   │   NaN values
  Timezone UTC  │  Off-by-one         │   Unicode chars
                │  Race condition     │   Very large input
  ────────────    ──────────────        ─────────────
                │                     │
                ▼                     ▼
         ┌──────────────────────────────────┐
         │         THE BUG                  │
         │  500 error on checkout           │
         └──────────────────────────────────┘
                ▲                     ▲
  ────────────    ──────────────        ─────────────
  Dependencies     Configuration        Infrastructure
  Stripe SDK v2   │  Missing env var   │  Pod restart
  Flask 3.0       │  Wrong DB URL      │  DNS resolution
  Redis 7         │  Rate limit        │  Network latency
```

**Hypothesis-Driven Debugging (Scientific Method):**

```python
"""
1. OBSERVE: Product page fails to load for users in EU region
2. HYPOTHESIS: CDN cache miss causes slow origin fetch
3. PREDICTION: Adding Cache-Control headers will fix it
4. EXPERIMENT: Set Cache-Control: public, max-age=3600 on product endpoint
5. RESULT: Bug persists → Hypothesis WRONG, try next
6. NEW HYPOTHESIS: EU data residency routing is sending to wrong DB
7. PREDICTION: Requests to EU arrive at wrong region
8. EXPERIMENT: Log X-Region header on every request
9. RESULT: Region header is 'us-east' for EU users
   → Root cause: GeoDNS not configured for eu-west load balancer
"""
```

### Phase 4: Log Analysis

```bash
# Structured log analysis with jq
# Find all errors in a time window
cat app.log | jq 'select(.level == "ERROR" and .timestamp > "2025-07-28T10:00:00Z")'

# Group errors by message to find the most frequent
cat app.log | jq -r 'select(.level == "ERROR") | .message' | sort | uniq -c | sort -rn | head -10

# Trace a single request through the system
cat app.log | jq 'select(.request_id == "req_abc123")' | head -50

# Find latency outliers
cat app.log | jq 'select(.duration > 5000) | {request_id, duration, path}' | head -10

# PostgreSQL slow query log analysis
tail -10000 /var/log/postgresql/postgresql-*.log | grep "duration:" | \
  sed 's/.*duration: \([0-9.]*\) ms.*/\1/' | sort -rn | head -10

# Python traceback aggregation
grep -A5 "Traceback (most recent call last)" app.log | grep -v "^--$" | head -30
```

### Phase 5: Exception Chain & Stack Trace Deep Dive

```python
# Python: Decode chained exceptions
try:
    try:
        raise ValueError("inner cause")
    except ValueError as e:
        raise RuntimeError("outer wrapper") from e
except RuntimeError as e:
    print(f"Exception: {e}")
    print(f"Cause: {e.__cause__}")     # → ValueError: inner cause
    print(f"Context: {e.__context__}")  # → also ValueError: inner cause (auto-chained)
    print(f"Traceback: {e.__traceback__}")

    # Full chain walk
    def walk_chain(exc):
        while exc:
            print(f"  {type(exc).__name__}: {exc}")
            exc = exc.__cause__ or exc.__context__
    walk_chain(e)

# Python: Post-mortem debugging
python -m pdb script.py  # Run in debugger
# At crash: pdb.set_trace() or breakpoint()
# Commands: where, list, print var, up, down, p locals()

# JavaScript: Stack trace parsing
# Error.stack gives full trace
# Chrome DevTools: "Pause on caught exceptions" for debugging catch blocks
```

### Phase 6: Debugging Intermittent & Concurrency Bugs

```python
import threading, time

# Technique: Add logging with thread/process ID
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(threadName)s] %(message)s'
)

# Technique: Stress test to increase reproduction rate
import concurrent.futures

def stress_test(func, args=(), n_threads=20, n_calls=100):
    """Run function many times concurrently to surface race conditions."""
    errors = []
    def wrapper():
        for _ in range(n_calls):
            try:
                func(*args)
            except Exception as e:
                errors.append(e)
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as ex:
        futures = [ex.submit(wrapper) for _ in range(n_threads)]
        concurrent.futures.wait(futures)
    print(f"Errors: {len(errors)}/{n_threads * n_calls}")
    return errors

# Technique: ThreadSanitizer for C/C++/Rust
# Compile with -fsanitize=thread
# clang -fsanitize=thread -g -O1 program.c -o program

# Technique: Python race detection
pip install pytest-repeat 2>/dev/null
pytest tests/test_concurrent.py --count=100 -x  # Run 100 times, stop on first failure
```

### Phase 7: Fix & Verify

```bash
# 1. Write a failing test that reproduces the bug
# 2. Apply the minimal fix
# 3. Confirm the test now passes
# 4. Run the full test suite to check for regressions
# 5. Run for 5 min under load to verify no new failures
pytest && echo "GREEN" || echo "REGRESSION"

# 6. Document the root cause
cat >> CHANGELOG.md << 'EOF'
## Fixed
- **500 error on checkout** when payment gateway times out.
  Root cause: GatewayTimeoutError inherits from BaseException,
  bypassing the PaymentError handler. Added explicit catch for
  GatewayTimeoutError. (PR #1482)
EOF

# 7. Add a monitoring alert for the failure pattern
cat > /tmp/alert_rule.yaml << 'EOF'
groups:
  - name: debugging-fixes
    rules:
      - alert: PaymentGatewayTimeout
        expr: rate(payment_gateway_errors_total{error="timeout"}[5m]) > 0.01
        for: 2m
        labels: { severity: warning }
        annotations:
          summary: Payment gateway timeouts detected
EOF
```

## Common Pitfalls

- **Skipping reproduction**: Never debug a bug you can't reproduce. Invest time in reliable reproduction first.
- **Confirmation bias**: Don't look for evidence that supports your first hypothesis. Actively try to disprove it.
- **Changing too many things at once**: Change one variable, test, then change the next. Multi-variable changes mask root cause.
- **Ignoring the environment**: The bug often lives in the gap between development and production environments (OS, dependencies, config).
- **Not reading the full error message**: The first line of the traceback is often more important than the last. Read the whole thing.
- **Assuming "it worked before"**: Regression doesn't mean the old code was correct — it might have been working by accident.
- **Fixing symptoms, not root cause**: If the 5 Whys ends at "add a try/except", you haven't gone deep enough.
- **No verification after fix**: Running the original reproduction case after the fix is mandatory. The test stays as a regression guard.
- **Not documenting root cause**: If you don't document what happened, the team will repeat the same debugging next month.

## Verification Checklist

- [ ] Bug reliably reproduced (3/3 attempts or stress-tested for intermittents)
- [ ] Environment captured (commit hash, OS, dependency versions, env vars)
- [ ] Test case written that fails with the bug
- [ ] Binary search or equivalent isolation technique used to narrow location
- [ ] Root cause identified via 5 Whys or hypothesis testing (not just "fixed it")
- [ ] Minimal fix applied (no scope creep, no refactoring mixed in)
- [ ] Test passes after fix
- [ ] Full test suite passes (no regressions)
- [ ] Reproduction case kept as automated test (regression guard)
- [ ] Root cause documented in changelog or bug tracker
- [ ] Monitoring/alert considered for this failure pattern
- [ ] Fix deployed to production and monitored for 24h
