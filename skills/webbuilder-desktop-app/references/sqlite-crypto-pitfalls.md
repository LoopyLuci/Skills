# SQLite + Cryptography Pitfalls

## sqlite3.connect() `uri=True` for In-Memory Shared Cache

### Problem

When using `file:memdb_<unique>?mode=memory&cache=shared` URI format for an in-memory SQLite database with shared cache across threads, `sqlite3.connect()` **requires** `uri=True`. Without it, SQLite interprets the URI string as a file path and fails with:

```
sqlite3.OperationalError: unable to open database file
```

### Correct Pattern

```python
db_path = f"file:memdb_{id(self)}?mode=memory&cache=shared"
cx = sqlite3.connect(
    db_path,
    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
    check_same_thread=False,
    uri=True,  # ← REQUIRED for file: URI format
)
```

### How It Bites

The `MetricsStore` class uses this pattern for in-memory databases shared across threads. Without `uri=True`, the connection fails at `sqlite3.connect()` time, and every metrics operation raises `OperationalError`. The bug is silent until a metrics operation is actually called.

### Detection

```python
# BUG: missing uri=True
cx = sqlite3.connect("file:memdb_123?mode=memory&cache=shared", check_same_thread=False)
# → OperationalError: unable to open database file

# FIX:
cx = sqlite3.connect("file:memdb_123?mode=memory&cache=shared", check_same_thread=False, uri=True)
# → Works
```

### Rule

Any `sqlite3.connect()` call where the first argument starts with `file:` **must** pass `uri=True`. This is a SQLite3 requirement, not Python.

---

## cryptography.fernet.Fernet.InvalidToken Does Not Exist

### Problem

`cryptography.fernet.Fernet` has **no** `InvalidToken` attribute. Attempting to catch `Fernet.InvalidToken` raises:

```
AttributeError: type object 'Fernet' has no attribute 'InvalidToken'
```

### Correct Import

```python
from cryptography.fernet import Fernet, InvalidToken

# Use:
try:
    decrypted = fernet.decrypt(token)
except InvalidToken:
    # Handle corrupted/invalid token
    pass
```

### How It Bites

Code that catches `cryptography.fernet.Fernet.InvalidToken` (fully qualified) or `Fernet.InvalidToken` (via class attribute) will raise `AttributeError` at the `except` clause evaluation time — which happens when the `try` block succeeds and the `except` is never entered, or when it's entered and the attribute lookup fails.

The `CredentialStore` class in QEMU-MCP had this exact bug: `except cryptography.fernet.Fernet.InvalidToken:` → `AttributeError: type object 'Fernet' has no attribute 'InvalidToken'`.

### Detection

```python
from cryptography.fernet import Fernet
print(hasattr(Fernet, 'InvalidToken'))  # False — does not exist
from cryptography.fernet import InvalidToken
print(InvalidToken)  # <class 'cryptography.fernet.InvalidToken'> — correct
```

### Rule

Always import `InvalidToken` directly from `cryptography.fernet` and catch it by name. Never qualify it as `Fernet.InvalidToken` or `cryptography.fernet.Fernet.InvalidToken`.

---

## General Pattern

Both of these pitfalls share a root cause: **assuming a library's API based on naming convention rather than verifying the actual exported symbols**. When using exception handling for third-party libraries:

1. Check `dir(ModuleOrClass)` for the actual exception name
2. Import the exception directly, not as a qualified attribute
3. Verify with a quick `python -c "from X import Y; print(Y)"` before relying on it
