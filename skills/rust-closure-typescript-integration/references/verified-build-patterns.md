# Verified Build Patterns — Polyglot Desktop (VM-Harness Type)

Reference for: `rust-closure-typescript-integration` skill (Verified Pitfalls section).

## Frozen Build Verification Checklist (Always Run After Rebuild)

```
1. ls target/release/*.pyd          → must exist (rebuild completed)
2. cp *.pyd dist/VM-Harness/_internal/
3. ls dist/VM-Harness/_internal/*.pyd → must exist (embedded)
4. ls dist/VM-Harness/python311.dll  → must exist (frozen loader fix)
5. cat gui/widgets.py | grep "_matplotlib_available" → minimum 6 matches
6. cargo build --release -p vmharness-supervisor → exit 0 (<5s)
7. .venv python -c "import sys; sys.path.insert(0, 'target/release'); import vmharness_supervisor; s=vmharness_supervisor.QemuSupervisor('test'); print(s.start(), s.state(), s.stop(), s.state())" → all PASS
8. ls installer.nsi | grep ".pyd" → NSIS includes .pyd
```

If ANY of steps 3, 4, or 5 fail: DO NOT launch EXE — exit 127 or `ModuleNotFoundError` is guaranteed.

## Graceful Dependency Fallback Pattern (matplotlib verified fix)

```python
try:
    import matplotlib
    HAS_MPL = True
except:
    HAS_MPL = False

class TelemetryChart(QWidget):
    def __init__(self, ...):
        try:
            from matplotlib.figure import Figure
            ...
            self._matplotlib_available = True
        except:
            self._matplotlib_available = False
            # placeholder
            placeholder = QLabel("No matplotlib available")
            placeholder.setStyleSheet("color: #64748b; font-size: 10px;")
            self.layout().addWidget(placeholder)

    def update_data(self):
        if not getattr(self, '_matplotlib_available', True): return
        ...  # original matplotlib code
```

Guarded methods: `update_data()`, `clear()`, `set_color()`, `export_to_png()`.

## File-Based Lock (Single-Instance — Frozen EXE Compatible)

```python
# gui/__main__.py — verified working
LOCK_FILE = os.path.expandvars(r"%LOCALAPPDATA%\VM-Harness\instance.lock")
os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)
self.lock_fd = open(LOCK_FILE, "w")
try:
    import msvcrt
    msvcrt.locking(self.lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
    if not self._is_pid_running():
        raise RuntimeError("Another instance is running.")
except:
    ...
```

`_is_pid_running()` uses `OpenProcess` + `GetExitCodeProcess` (ctypes) to detect stale locks from crashed instances.

## Rust `.pyd` Import Verification (Always After Build)

```python
import sys, importlib.util
sys.path.insert(0, "target/release")
# Rebuild forces reload even with cached module
if "vmharness_supervisor" in sys.modules:
    del sys.modules["vmharness_supervisor"]
import vmharness_supervisor
sup = vmharness_supervisor.QemuSupervisor("test-vm")
assert sup.start() is not None
assert sup.state()  # returns state dict or string
assert sup.stop() is not None
assert "stopped" in str(sup.state())
```

If `ModuleNotFoundError` for `vmharness_supervisor`: the `.pyd` is either missing from `target/release/` or the build failed silently (check `cargo build` output — must say `Finished` not `Compiling` interrupted).
