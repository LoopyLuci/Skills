---
name: python-error-hardening
description: Elevate excepts to typed errors, isolate test singletons.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [python, error-handling, testing, refactoring]
---

# Python Error Hardening

Systematically elevate bare `except Exception:` to typed errors across Python production code, and manage test singleton isolation to prevent state leakage between test files.

## Trigger

Use when:
- A Python codebase has bare `except Exception:` clauses in production code that should be typed
- Test suite has flaky failures caused by shared mutable state between test files
- A codebase is being hardened for production and error handling needs to be specific

## Phase 1: Audit — Find All Bare Excepts

### Step 1: Grep for bare except Exception:

```bash
# Find bare except Exception: (no 'as e' binding)
grep -rn "except Exception:" <dir> --include="*.py" | grep -v "except.*Exception as"

# Find all except Exception (bare + bound) for review
grep -rn "except Exception" <dir> --include="*.py"
```

### Step 2: Categorize each hit

For each bare `except Exception:` found, read the surrounding context (10-15 lines) and classify:

| Pattern | Action |
|---------|--------|
| Top-level crash handler (`main()`, `run()`) that logs and exits | **Keep as Exception** — genuinely needs to catch everything |
| Context manager that rolls back and re-raises | **Keep as Exception** — safety net, re-raises anyway |
| File I/O block (read/write/delete) | **Replace** with `(OSError, IOError)` |
| subprocess call block | **Replace** with `(subprocess.TimeoutExpired, ProcessLookupError, OSError)` |
| JSON parse block | **Replace** with `json.JSONDecodeError` |
| Network/socket call block | **Replace** with `(OSError, TimeoutError, ConnectionError)` |
| QIcon/Qt resource load | **Replace** with `(RuntimeError, OSError)` |
| Signal/slot connection (PyQt) | **Replace** with `(AttributeError, RuntimeError)` |
| Dictionary key access that falls back to default | **Replace** with `KeyError` |
| Import block | **Replace** with `ImportError` |
| `logger.error(...)` inside except with `as e` binding | **Review** — if it logs the error and continues, keep but add specific types; if it's a genuine catch-all, document why |

### Step 3: Batch the replacements

Group files by the exception types needed and apply patches. For each file:

```python
# BEFORE (bare):
try:
    result = some_operation()
except Exception:
    return default

# AFTER (typed):
try:
    result = some_operation()
except (OSError, ValueError):
    return default
```

**Rule**: Always replace with a tuple of the most specific types that cover the actual failure modes of the called code. Do not use a single broad type like `OSError` when `subprocess.TimeoutExpired` is also possible.

## Phase 2: Verify Each Replacement

After patching each file:

```bash
# Syntax check
python -m py_compile <file>

# Import check
python -c "import <module>"

# Run the file's tests
pytest <test_file> -q
```

## Phase 3: Handle Genuine Catch-Alls

Some `except Exception:` clauses are correct and should stay. Document them with an inline comment:

```python
# Top-level safety net — never let state save crash the app
 try:
     state.save()
 except Exception:
     pass
```

Criteria for keeping:
1. The except block is at the outermost scope of a critical operation
2. The failure mode is truly unknowable (e.g., `QApplication` teardown)
3. The except block does not swallow the error silently — it logs, falls back, or re-raises
4. Narrowing the type would introduce a new unhandled exception path

## Phase 4: Test Singleton Isolation

### Problem

Tests in separate files interfere through shared module-level singletons (AuditLogger, ProviderStore, MetricsStore, QApplication). When one test creates/destroys a QApplication with a Qt-parented singleton, later tests find the deleted C++ object and crash with:

```
RuntimeError: wrapped C/C++ object of type X has been deleted
```

### Root Cause

PyQt5 deletes all QObjects parented to a QApplication when that QApplication is destroyed. A module-level singleton that gets reparented to the test's QApplication is deleted when the test tears down. The Python reference still exists but the C++ object is gone.

### Fix Options

**Option A: Don't reparent singletons to QApplication**

Create singletons without a Qt parent. The Python-level module reference keeps the C++ object alive. If signal delivery is needed, use `QTimer.singleShot(0, ...)` to deliver on the current event loop without requiring a parent.

```python
# Module-level singleton — no Qt parent
audit_log = AuditLogger()  # No parent argument

# In log() method, lazy-attach to current QApplication if needed for signals
def _ensure_parent(self):
    if self._parent is None:
        try:
            app = QApplication.instance()
            if app is not None:
                self._parent = app
        except ImportError:
            pass
```

**Option B: Fresh fixture per test**

```python
# conftest.py
@pytest.fixture
def fresh_audit_log():
    from gui.audit_log import AuditLogger
    logger = AuditLogger()
    yield logger
    logger.close()
```

Each test gets a new instance. No shared state.

**Option C: Reset module state between files**

```python
# conftest.py — NOT RECOMMENDED for Qt apps
@pytest.fixture(autouse=True, scope="session")
def reset_module_state():
    yield
    import importlib
    importlib.reload(gui.audit_log)  # Breaks Qt parent attachment!
```

**Pitfall**: Module reload (`importlib.reload`) breaks Qt parent attachments and signal delivery. The reloaded module creates new objects without the original Qt parent chain. Use Option A or B instead.

### Detection

```bash
# Run tests in different orders to expose state leakage
pytest tests/ -q --tb=short          # default order
pytest tests/test_audit_log.py tests/test_gui.py -q  # specific order
pytest tests/test_gui.py tests/test_audit_log.py -q  # reverse order
```

If tests pass in one order and fail in another, state leakage is the cause.

## Pitfalls

1. **Bare `except Exception:` in context managers**: A context manager that catches `Exception`, rolls back, and re-raises is a genuine safety net. Narrowing it breaks the rollback-on-any-error guarantee. Keep these.

2. **`except Exception:` that logs `as e`**: Just because it binds `as e` and logs doesn't mean it should be narrowed. If the called code can raise many types and the handler treats them all identically, keep it broad but add a comment explaining why.

3. **Replacing `except Exception:` with a single type**: Using `except OSError:` when the code can also raise `ValueError`, `KeyError`, etc. introduces new unhandled paths. Always use a tuple of all plausible types.

4. **`cryptography.fernet.Fernet.InvalidToken` does not exist**: The `Fernet` class has no `InvalidToken` attribute. Import `InvalidToken` directly from `cryptography.fernet` and catch it by name. See [webbuilder-desktop-app references/sqlite-crypto-pitfalls.md](https://hermes-agent.nousresearch.com/skills/software-development/webbuilder-desktop-app/references/sqlite-crypto-pitfalls.md).

5. **`sqlite3.connect()` needs `uri=True` for `file:` URIs**: When connecting to `file:memdb_...?mode=memory&cache=shared`, you must pass `uri=True`. Without it, SQLite treats the URI as a file path and fails with `OperationalError: unable to open database file`.

6. **conftest.py module-reload breaks Qt parent attachment**: Reloading a module that contains Qt-parented singletons creates new objects without the original parent chain. Signals break, and C++ objects may be deleted prematurely. Use fresh fixtures or parentless singletons instead.

## Tools

- `grep -rn "except Exception" <dir>` — find all bare excepts
- `python -m py_compile <file>` — syntax check after patch
- `python -c "import <module>"` — import check
- `pytest <test_file> -q` — verify tests still pass
- `subprocess.run([...], capture_output=True, timeout=5)` — test for segfaults in subprocess

## Reference

- [webbuilder-desktop-app: SQLite + cryptography pitfalls](https://hermes-agent.nousresearch.com/skills/software-development/webbuilder-desktop-app/references/sqlite-crypto-pitfalls.md)
- [webbuilder-desktop-app: QT_QPA_PLATFORM=offscreen segfault](https://hermes-agent.nousresearch.com/skills/software-development/webbuilder-desktop-app/references/qt-offscreen-segfault.md)
