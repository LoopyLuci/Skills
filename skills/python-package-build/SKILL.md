---
name: python-package-build
description: "Build+verify Python pkgs: CLI/GUI/TUI, async, xplat."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [python, packaging, pyproject, cross-platform, verification, desktop-app, setuptools]
    related_skills: [test-driven-development, systematic-debugging, service-orchestration]
---

# Python Package Build

## Overview

Build complete, verifiable Python packages from scratch — covering project structure, cross-platform concerns, multi-UI backends, async networking, and the verification pipeline that proves the package works.

## When to Use

- Building a new Python package from scratch (CLI app, desktop app, library)
- Creating a cross-platform Python application with multiple UI backends (CLI + GUI + TUI)
- Verifying a Python package before declaring it done
- Setting up a package with optional dependency groups (extras)

## Project Structure

```
my-package/
├── pyproject.toml          # Build config & metadata
├── requirements.txt        # Pinned versions (optional)
├── README.md               # Full documentation
└── my_package/             # Source package
    ├── __init__.py         # Package metadata, version, logger
    ├── __main__.py         # `python -m my_package` entry point
    ├── core/               # Core logic (no UI deps)
    │   ├── __init__.py
    │   ├── config.py       # Config management
    │   └── ...
    ├── ui/                 # User interfaces
    │   ├── __init__.py     # Auto-detect backend
    │   ├── cli_app.py      # Click/argparse CLI
    │   ├── tui_app.py      # Textual TUI (optional dep)
    │   └── qt_app.py       # PyQt6/PySide6 GUI (optional dep)
    └── server/             # Background daemon
        ├── __init__.py
        └── server.py       # Background service
```

## pyproject.toml Essentials

### Optional dependency groups (extras)

```toml
[project]
requires-python = ">=3.9"
dependencies = [
    "click>=8.1.0",
    # Core deps only — UI/networking extras below
]

[project.optional-dependencies]
gui = ["PyQt6>=6.5.0"]
tui = ["textual>=0.52.0"]
streaming = ["python-vlc>=3.0.0"]
all = ["my-package[gui,tui,streaming]"]

[project.scripts]
myapp = "my_package.ui.cli_app:cli"
```

### Entry points

- `[project.scripts]` for installed CLI entry point (`myapp` on PATH)
- `__main__.py` for `python -m my_package` — should auto-detect best UI backend

## Multi-UI Backend Auto-Detection

The `ui/__init__.py` should auto-detect the best available backend at runtime.

```python
def detect_ui_backend() -> str:
    """Auto-detect: PyQt6 > PySide6 > Textual > CLI."""
    force = os.environ.get("MYAPP_UI", "").lower()
    if force: ...
    for mod_name in ("PyQt6", "PySide6"):
        if importlib.util.find_spec(mod_name):
            return "gui"
    if importlib.util.find_spec("textual"):
        return "tui"
    return "cli"
```

### Deferred Qt imports (critical)

Never import Qt at module level — it makes the whole package require PyQt6 even in CLI mode:

```python
# WRONG — breaks the whole package if PyQt6 is missing
from PyQt6.QtWidgets import QMainWindow

# RIGHT — deferred import
def _get_qt():
    try:
        from PyQt6 import QtWidgets, QtCore, QtGui
        return QtWidgets, QtCore, QtGui
    except ImportError:
        from PySide6 import QtWidgets, QtCore, QtGui
        return QtWidgets, QtCore, QtGui
```

## Cross-Platform Paths

```python
import platform
from pathlib import Path

def get_config_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        base = Path(os.environ.get("APPDATA",
            str(Path.home() / "AppData" / "Roaming")))
    elif system == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME",
            str(Path.home() / ".config")))
    return base / "myapp"
```

## Async in Background Threads

```python
import threading, asyncio

class Transport:
    def start_server(self, host, port):
        self._thread = threading.Thread(
            target=self._run_loop, args=(host, port), daemon=True
        )
        self._thread.start()

    def _run_loop(self, host, port):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._async_server(host, port))

    def send_message(self, device_id, message):
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self._async_send(device_id, message), self._loop
            )
```

## Multi-Stage Verification Pipeline

Each stage catches a different class of problem cheaply before the next (more expensive) stage runs.

### Stage 1 — Syntax check every file
```bash
python -m py_compile my_package/core/module.py
find my_package -name '*.py' -exec python -m py_compile {} \;
```

### Stage 2 — AST validation
```python
import ast, os
for dirpath, _, filenames in os.walk('my_package'):
    for fn in filenames:
        if fn.endswith('.py'):
            with open(os.path.join(dirpath, fn)) as f:
                ast.parse(f.read())
```

### Stage 3 — Import test
```python
import sys
sys.path.insert(0, '.')
__import__('my_package.core.config')    # stdlib-only first
__import__('my_package.core.protocol')  # stdlib-only
__import__('my_package.ui.cli_app')     # external deps last
```

### Stage 4 — CLI smoke test
```bash
python -m my_package --help
myapp --help
myapp discover --help
pip install -e . && myapp --help
```

### Stage 5 — Behavioral test
Write a stand-alone verification script that exercises real behavior:
- Config save/load roundtrip (including from string paths)
- Crypto encrypt/decrypt roundtrip
- Protocol message serialization roundtrip
- Transfer init/simulate/complete lifecycle
- Stream start/stop lifecycle
- All previously caught bugs regression-tested by this script

## Common Pitfalls

### `Optional[Path]` accepting `str`
```python
# WRONG — crashes when caller passes a string
def load(config_path: Optional[Path] = None):
    if config_path.exists():  # AttributeError

# RIGHT — convert at function entry
def load(config_path: Optional[Path] = None):
    if isinstance(config_path, str):
        config_path = Path(config_path)
    # Now safe: .exists(), .parent, etc.
```

Apply to **both** `load()` and `save()` — same signature, same bug.

### Module-level Qt imports
Deferred imports in functions, never `from PyQt6` at module scope.

### `Optional[Path]` ≠ runtime guarantee
Python doesn't enforce type hints. A caller can pass `None`, `str`, or `Path`. Always convert defensively.

## Verification Checklist

- [ ] All `.py` files pass `py_compile` and `ast.parse`
- [ ] All modules import without error
- [ ] CLI entry point works (`python -m pkg` AND installed script)
- [ ] Each subcommand shows correct help text
- [ ] Config save/load roundtrip works (including from string paths)
- [ ] Crypto/protocol layer passes roundtrip tests
- [ ] Transfer/streaming state machines have lifecycle tests
- [ ] Behavioral verification script passes all checks
- [ ] Editable install (`pip install -e .`) works cleanly

## Reference Files

| File | Covers |
|---|---|
| `references/streamsync-verification.md` | Behavioral verification script for StreamSync file transfer, streaming, clipboard sync, and screen mirroring. |
| `references/rust-build-patterns.md` | Rust protobuf compilation patterns (prost-build 0.13 API, isolated gen-project workaround, third-party API gotchas for mdns-sd, aes-gcm, tokio-tungstenite). |

## Related Skills

- **test-driven-development** — write failing tests first for new features
- **systematic-debugging** — root-cause bugs found during verification
- **service-orchestration** — auto-start and monitor background daemon processes
