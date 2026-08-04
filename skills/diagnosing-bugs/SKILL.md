---
name: diagnosing-bugs
description: Use when diagnosing hard bugs, debugging failures, or investigating performance regressions
tags: [debugging, bugs, diagnosis, bisect, testing]
related_skills: [systematic-debugging, debugging-techniques-advanced, qa]
---

# Diagnosing Bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

## Phase 1 - Build a feedback loop
**This is the skill.** Everything else is mechanical. If you have a tight pass/fail signal for the bug - one that goes red on *this* bug - you will find the cause.

Ways to construct one, in roughly this order:
1. **Failing test** at whatever seam reaches the bug
2. **Curl / HTTP script** against a running dev server
3. **CLI invocation** with a fixture input
4. **Headless browser script** (Playwright / Puppeteer)
5. **Replay a captured trace**
6. **Throwaway harness** with mocked deps
7. **Property / fuzz loop** - run 1000 random inputs
8. **Bisection harness** for git bisect run

## Phase 2 - Find the fault
With the loop in place, let it guide you. Narrow by bisection, hypothesis testing, or instrumentation.

## Phase 3 - Fix
Apply the fix and confirm the loop goes green. Consider whether the same class of bug exists elsewhere.

## Common Pitfalls

- **Starting to code before building a feedback loop**: The first phase is the skill. Without a tight pass/fail signal, no amount of staring at code will find the bug.
- **Skipping the feedback loop for 'simple' bugs**: Even seemingly simple bugs benefit from an automated signal. Manual verification is slow and error-prone.
- **Over-instrumenting without a hypothesis**: Adding logging everywhere without a theory of the root cause creates noise, not signal. Form a hypothesis first, then instrument to test it.

## Code Examples

```python
# Example: Bug where session expires at 29min instead of configured 60min

# Build the feedback loop - a failing test
def test_session_expires_at_configured_timeout():
    session = Session(timeout_minutes=60)
    advance_time(minutes=29)
    assert session.is_valid()  # Should be True, but might be False

# Property-based test to narrow the failure
@pytest.mark.parametrize("ttl", [1, 5, 30, 60, 120])
def test_timeout_matches_ttl(ttl):
    session = Session(timeout_minutes=ttl)
    advance_time(minutes=ttl - 1)
    assert session.is_valid()
    advance_time(minutes=2)
    assert not session.is_valid()
```

## Verification Checklist

- [ ] Feedback loop built (failing test, curl, or harness)
- [ ] Pass/fail signal is tight (goes red on this bug specifically)
- [ ] Bisection or hypothesis-testing performed
- [ ] Root cause identified and documented
- [ ] Fix verified by the feedback loop going green
