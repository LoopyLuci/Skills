---
name: bare-except-elimination
description: Replace bare except Exception: with typed exceptions.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [exceptions, error-handling, code-quality]
---

# Bare Except Elimination

## Overview

Bare `except Exception:` (no `as e`, no logging) silently swallows errors. This skill covers the workflow to find and replace them with typed exceptions, and the pitfalls that cost time.

**When:** Code quality audit, hardening pass, production release prep.

**What it produces:** Every bare `except Exception:` replaced with a specific typed exception (or removed), with tests passing.

## Categorizing Bare Excepts

Before editing, categorize each occurrence:

### 1. Logged and re-raised — LEAVE ALONE

```python
try:
    yield self._local.cx
except Exception:
    self._local.cx.rollback()
    raise  # Re-raise after rollback
```

**Why:** Context manager safety net. The exception caught is from the `with` block body (caller's code), not from the `yield`. Narrowing breaks the guarantee that ANY caller error triggers rollback.

**Rule:** Context managers wrapping `yield` with rollback/re-raise — keep broad.

### 2. Logged with `logger.error(..., e)` — LEAVE ALONE

```python
try:
    result = await self._send("query-status")
except Exception as e:
    logger.error("Failed: %s", e)
    return {}
```

**Why:** Error is recorded with full context. Narrowing adds little value.

**Rule:** `except Exception as e` + `logger.error(..., e)` — leave alone.

### 3. Silent `pass` — ELIMINATE

```python
try:
    self._window.setGeometry(...)
except Exception:
    pass
```

**Why:** Silently swallows errors. If `setGeometry` fails because the window closed, you want `RuntimeError` or `TypeError` — not a hide-all swallow.

**Rule:** `except Exception: pass` without logging — always elevate.

### 4. Subprocess/timeout errors — ELEVATE TO `(subprocess.TimeoutExpired, ProcessLookupError, OSError)`

```python
try:
    backup.terminate()
    backup.wait(timeout=3)
except Exception:
    backup.kill()
```

**Why:** Only failures from `terminate()` + `wait(timeout=N)` are timeout, process already dead, or OS errors. Catching `Exception` also swallows `AttributeError` if `backup` is None, hiding a bug.

### 5. IO/file errors — ELEVATE TO `OSError` or `(OSError, json.JSONDecodeError)`

**Rule:** File operations → OSError. JSON parsing → json.JSONDecodeError. Add other likely exception types.

### 6. Import/reload errors — ELEVATE TO `(RuntimeError, OSError)` or `(ImportError, RuntimeError)`

### 7. Qt signal/slot patterns — ELEVATE TO `(AttributeError, RuntimeError)`

## Workflow

### Step 1: Find all bare excepts

```bash
# Bare except Exception: (no 'as e', no logging)
grep -rn "except Exception:" gui/ --include="*.py" \\
  | grep -v "except.*Exception as" \\
  | grep -v "logger\.error\|log\.error"

# Bare except Exception as e: that are NOT logged
allowed="logger\.error|log\.error|warnings\.warn"
grep -rn "except Exception as e:" gui/ --include="*.py" \\
  | grep -v "$allowed"
```

### Step 2: Group by file and context

Read 5-10 lines around each occurrence. Categorize using the buckets above.

### Step 3: Eliminate in batches by category

Order: subprocess/timeout → IO/file → import/reload → Qt signal/slot → geometry/window.

### Step 4: Verify after each batch

```bash
QT_QPA_PLATFORM=offscreen pytest tests/test_gui.py tests/test_audit_log.py \
  tests/test_e2e_qmp_ssh.py tests/test_core.py -q --tb=line
```

If a batch introduces failures, the exception types are too narrow — widen or revert.

### Step 5: Handle failures

- **NameError: name 'X' is not defined** — missing import. Add it.
- **AttributeError: type object 'X' has no attribute 'Y'** — wrong exception path (e.g. `Fernet.InvalidToken` doesn't exist; use `InvalidToken` imported from `cryptography.fernet`).
- **sqlite3.OperationalError** — exception too narrow. Widen or revert.

## Pitfalls

### Context manager safety nets must stay broad

A `yield` inside `try/except Exception: rollback(); raise` is a deliberate safety net. The broad catch handles ANY exception the caller's `with` block body could raise — not just the operation after `yield`. Narrowing it breaks the guarantee.

**Mechanism:** The exception caught originates from the `with` block body (caller's code), not the `yield` expression. Possible exceptions are unbounded.

### Fernet.InvalidToken does not exist on the Fernet class

```python
# WRONG — Fernet has no InvalidToken attribute
from cryptography.fernet import Fernet
except Fernet.InvalidToken:

# CORRECT — InvalidToken is module-level
from cryptography.fernet import Fernet, InvalidToken
except InvalidToken:
```

**Mechanism:** `InvalidToken` is defined at the `cryptography.fernet` module level, not as a class attribute on `Fernet`. `Fernet.InvalidToken` raises `AttributeError` at runtime, crashing the except handler itself.

### sqlite3.connect with URI-mode paths requires uri=True

```python
# When db_path is "file:memdb_123?mode=memory&cache=shared"
conn = sqlite3.connect(db_path, uri=True)  # MUST pass uri=True
```

Without `uri=True`, sqlite3 treats the whole string as a file path and fails with `sqlite3.OperationalError: unable to open database file`.

**Mechanism:** The `file:` URI scheme is only activated when `uri=True` is passed.

### QApplication teardown kills Qt parents

When a test creates a `QApplication` and it's destroyed, any `QObject` parented to it is also destroyed. Module-level singletons that set a Qt parent lazily crash on subsequent test imports.

**Fix:** Create module-level singletons without a Qt parent. Attach parent lazily on first use only if a `QApplication` exists. Initialize `_qt_parent_app = None` in `__init__`.

### Conftest module-reload breaks singleton state

Using `importlib.reload()` in conftest to reset module-level globals between test files breaks Qt parent attachments and C++ object state. Use session-scoped fixtures that create fresh instances instead.

**Mechanism:** `importlib.reload()` re-executes the module, re-creating the singleton, but Qt C++ objects from the old instance may still be referenced elsewhere, causing `RuntimeError: wrapped C/C++ object has been deleted`.

## Quick Reference

| Pattern | Action |
|---------|--------|
| `except Exception: pass` (silent) | **Eliminate** — elevate to specific types |
| `except Exception: rollback(); raise` (context manager) | **Leave alone** — safety net |
| `except Exception as e: logger.error(..., e)` | **Leave alone** — logged |
| `except Exception: return default` (fallback) | **Elevate** — to specific IO/parse errors |
| `except Exception: kill()` (subprocess cleanup) | **Elevate** — to `TimeoutExpired, ProcessLookupError, OSError` |
| `except Exception: pass` (Qt signal connect) | **Elevate** — to `AttributeError, RuntimeError` |
| `except Exception: pass` (geometry) | **Elevate** — to `RuntimeError, TypeError` |

## Verification

After all elevations:

```bash
grep -rn "except Exception:" gui/ --include="*.py" \\
  | grep -v "except.*Exception as" \\
  | grep -v "logger\.error\|log\.error" \\
  | grep -v "rollback\|raise  # Re-raise"
```

Expected: only context-manager safety nets and logged patterns remain.
