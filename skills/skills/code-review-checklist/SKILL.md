---
name: code-review-checklist
description: "Use for code review. Correctness, security, performance."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [programming, code-review, pr-review, quality, best-practices, security]
    related_skills: [refactoring-playbook, debugging-workflow, performance-profiling]
---

# Code Review Checklist

## Overview

A comprehensive multi-dimensional code review checklist covering correctness, security, performance, maintainability, and style. Includes severity ratings, comment templates, and automation workflows for pre-commit and CI integration. Designed to produce consistent, actionable, and respectful code reviews.

## When to Use

- Reviewing a pull request from a teammate
- Performing a self-review before opening a PR
- Auditing code for a production release or security review
- Onboarding new reviewers to team standards
- Setting up automated review gates in CI

## Workflow

### Phase 1: Pre-Review Preparation

```bash
# 1. Understand the PR context
gh pr view <number>          # GitHub CLI: see description + status
gh pr diff <number>          # Full diff
gh pr review <number> --request-changes  # Or --approve / --comment

# 2. Check CI status
gh pr checks <number>

# 3. Fetch the branch locally for deeper analysis
gh pr checkout <number>

# 4. Run automated checks locally
pytest && echo "Tests pass" || echo "Tests fail"
flake8 . && echo "Lint clean" || echo "Lint issues"
mypy . && echo "Types pass" || echo "Type issues"
```

### Phase 2: Correctness (Severity: 🔴 BLOCKER unless fixed)

**Logic & Edge Cases:**
- [ ] Does the code handle the **happy path** correctly?
- [ ] Are **edge cases** covered? (empty lists, null values, max/min boundaries, negative numbers)
- [ ] Are **error states** handled explicitly? (network failures, file not found, permission denied, timeout)
- [ ] Are **race conditions** possible? (shared state without locks, non-atomic read-modify-write)
- [ ] Are **off-by-one** errors present? (loop bounds, array indices, slice ranges)
- [ ] Does the code **fail fast** on invalid input? (validate early, don't propagate bad data)
- [ ] Are **transactions** properly committed/rolled back on error?
- [ ] Are **resource leaks** possible? (file handles, DB connections, network sockets, locks)

```python
# 🔴 BLOCKER: No input validation
def process_user(user_id, amount):
    db.execute("UPDATE users SET balance = balance - %s WHERE id = %s",
               (amount, user_id))
    # What if user_id doesn't exist? What if amount > balance?

# ✅ CORRECT: Validate first, then act
def process_user(user_id, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    user = db.fetch_one("SELECT id, balance FROM users WHERE id = %s", (user_id,))
    if not user:
        raise ValueError(f"User {user_id} not found")
    if user['balance'] < amount:
        raise ValueError("Insufficient balance")
    db.execute("UPDATE users SET balance = balance - %s WHERE id = %s",
               (amount, user_id))
```

### Phase 3: Security (Severity: 🔴 BLOCKER unless fixed)

**Injection & Validation:**
- [ ] Are all **user inputs validated** against a whitelist? (never blacklist)
- [ ] Is **SQL injection** prevented? (parameterized queries only — no f-string interpolation)
- [ ] Is **NoSQL injection** prevented? (proper MongoDB/Sanitize for NoSQL queries)
- [ ] Is **command injection** prevented? (avoid `os.system()`, `subprocess(shell=True)`)
- [ ] Are **path traversal** attacks prevented? (validate file paths, no user-controlled paths)
- [ ] Is **XSS** prevented in rendered output? (escape HTML/JS context appropriately)

**Authentication & Authorization:**
- [ ] Are all endpoints properly **authenticated**?
- [ ] Is **authorization** checked per resource? (user A shouldn't access user B's data)
- [ ] Are **secrets and keys** kept out of code? (no hardcoded API keys, passwords, tokens)
- [ ] Are **API keys and tokens** properly scoped? (least privilege principle)
- [ ] Is **rate limiting** applied to sensitive endpoints? (login, password reset, payment)

**Data Protection:**
- [ ] Is **sensitive data** (PII, passwords, tokens) **not logged**?
- [ ] Are **passwords** properly hashed? (bcrypt, argon2 — not md5, sha1, or plaintext)
- [ ] Are **secrets in URLs** avoided? (don't pass tokens in query params — use headers)

```python
# 🔴 BLOCKER: SQL injection vulnerability
query = f"SELECT * FROM users WHERE email = '{email}'"  # NEVER do this

# ✅ CORRECT: Parameterized query
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))

# 🔴 BLOCKER: Hardcoded secret
API_KEY = "sk-abc123def456"  # NEVER hardcode secrets

# ✅ CORRECT: Environment variable
import os
API_KEY = os.environ["API_KEY"]
```

### Phase 4: Performance (Severity: 🟡 WARNING — context-dependent)

**Database:**
- [ ] Are **N+1 queries** avoided? (look for queries inside loops)
- [ ] Are **database indexes** used for all WHERE/JOIN/ORDER BY columns?
- [ ] Are **large result sets** paginated? (never SELECT * without LIMIT)
- [ ] Are **bulk operations** used instead of individual inserts/updates?
- [ ] Is **connection pooling** configured correctly?

**Compute:**
- [ ] Are **unnecessary computations** avoided? (memoize expensive calls, cache repeated results)
- [ ] Are **large objects** avoided in hot paths? (don't serialize gigabytes to JSON)
- [ ] Are **allocation-heavy patterns** replaced with reuse? (object pools, array reuse)
- [ ] Is **async/parallelism** used for I/O-bound tasks? (network calls, file reads)
- [ ] Are **memory leaks** possible? (growing collections, closure references, event listeners)

```python
# 🟡 WARNING: N+1 query pattern
users = db.query("SELECT id, name FROM users")
for user in users:
    # One query per user → N+1!
    orders = db.query(f"SELECT * FROM orders WHERE user_id = {user['id']}")

# ✅ PERFORMANT: Batch query
users = db.query("SELECT id, name FROM users")
user_ids = [u['id'] for u in users]
orders = db.query(
    "SELECT * FROM orders WHERE user_id = ANY(%s)",
    (user_ids,)
)
orders_by_user = defaultdict(list)
for order in orders:
    orders_by_user[order['user_id']].append(order)
```

### Phase 5: Maintainability (Severity: 🟡 WARNING — improve if practical)

**Readability:**
- [ ] Are **function names** descriptive? (verbs for functions, nouns for classes)
- [ ] Are **variable names** meaningful? (avoid `x`, `tmp`, `data`, `thing`)
- [ ] Is each function doing **one thing**? (Single Responsibility)
- [ ] Are **magic numbers** replaced with named constants?
- [ ] Is **deep nesting** avoided? (3+ levels → extract method or early return)
- [ ] Are **comments** explaining WHY, not WHAT? (code shows what; comments explain reasoning)

**Structure:**
- [ ] Is the **module/package structure** logical? (related things grouped, unrelated separated)
- [ ] Are **imports** clean? (no wildcard imports, no circular dependencies)
- [ ] Are **abstractions** appropriate for the complexity? (not over-engineered, not under-engineered)
- [ ] Is **error handling** consistent? (same pattern throughout: return vs raise vs Option)

**Testing:**
- [ ] Are there **unit tests** for the new logic?
- [ ] Do tests cover **edge cases** (not just happy path)?
- [ ] Are tests **independent**? (no shared state, no order dependency)
- [ ] Are tests **readable**? (descriptive names, Arrange-Act-Assert pattern)
- [ ] Is **test coverage** at or above team threshold?

### Phase 6: Style & Conventions (Severity: 🟢 NICE-TO-HAVE)

- [ ] Does the code follow the team's **formatter**? (black, ruff-format, prettier, gofmt, rustfmt)
- [ ] Are **type hints** used where the language supports them?
- [ ] Are **docstrings** present on public APIs?
- [ ] Does the code match the **project's existing style**? (consistency over perfection)
- [ ] Are **unused imports/variables** removed?
- [ ] Are **TODO/FIXME comments** tracked in issue tracker?

### Phase 7: Review Comment Templates

```
## Severity 🔴 BLOCKER
"User input is interpolated directly into a SQL query on line 42.
This is a SQL injection vulnerability. Please use parameterized
queries: cursor.execute(sql, (user_input,)) instead of
cursor.execute(f\"{sql}\")."

## Severity 🟡 WARNING
"There's an N+1 query pattern starting on line 87 — the database
is queried once per iteration of the user list. Consider batching
the queries with a single SELECT ... WHERE id = ANY(%s)."

## Severity 🟢 NICE-TO-HAVE
"The variable name 'd' on line 15 isn't descriptive. Consider
renaming to 'response_data' or 'payload' to clarify what it holds."

## Positive feedback 🌟
"Great use of early returns on lines 10-12 to flatten the nesting
and make the happy path obvious. The error handling is clean."
```

### Phase 8: Automated Review Gates

```yaml
# .github/workflows/code-review.yml
name: Code Review Gates
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint
        run: |
          pip install ruff
          ruff check --output-format=github .

      - name: Type Check
        run: |
          pip install mypy
          mypy src/

      - name: Security Scan
        run: |
          pip install bandit
          bandit -r src/ -f sarif

      - name: Complexity Gate
        run: |
          pip install radon
          radon cc src/ -n C | tee complexity.txt
          ! grep -q "F\|C" complexity.txt

      - name: Test Coverage Gate
        run: |
          pytest --cov=src/ --cov-fail-under=80

      - name: Dependency Audit
        run: |
          pip-audit
```

## Common Pitfalls

- **Focusing only on style**: Style is the least important dimension. Spend review energy on correctness, security, and logic.
- **Rubber-stamping**: Approving without understanding the code. If you can't explain what a PR does, you haven't reviewed it.
- **Subjective gatekeeping**: "I would have written it differently" is not a review comment. Judge by correctness and maintainability, not personal preference.
- **Bike-shedding**: Spending too much time on trivial issues (naming, formatting) while missing real bugs.
- **Reviewing too late**: Code review should happen within hours, not days. Stale reviews block progress.
- **Too many comments per review**: Focus on the 3-5 most important issues. Flooding a PR with 50 comments is demoralizing.
- **No positive feedback**: Reviews aren't just for finding problems. Acknowledge good patterns and clever solutions.
- **Not checking test quality**: Looking at production code but ignoring tests. Tests are equally important to review.
- **Reviewing giant PRs**: Break large changes into reviewable chunks (<400 lines per PR recommended).

## Verification Checklist

- [ ] Correctness: All edge cases considered, error states handled, no off-by-one
- [ ] Security: No injection vulnerabilities, auth checked per resource, no secrets in code
- [ ] Performance: No N+1 queries, pagination present, no obvious memory leaks
- [ ] Maintainability: Good naming, single responsibility, appropriate abstractions
- [ ] Style: Consistent with project conventions, formatted, type-hinted
- [ ] Tests: Cover the new logic, include edge cases, independent and readable
- [ ] Comments provided at appropriate severity levels (🔴 🟡 🟢 🌟)
- [ ] No bias toward personal preference — objective criteria only
- [ ] Reviewed within same business day (or within 24h)
- [ ] PR is of reviewable size (<400 lines), or chunked into manageable pieces
- [ ] Automated gates passed (lint, security scan, complexity, coverage)
- [ ] Reviewer understands the code path end-to-end
