# Isolation pattern for desktop apps alongside Hermes

When a desktop GUI runs alongside the Hermes agent installation, Hermes exports
`PYTHONPATH` pointing at its own `site-packages` (built for a different Python
version, e.g., cp314). Every child process inherits it, and `sys.path` is built
at interpreter startup — clearing the environment variable after import does not
remove the entries that are already in `sys.path`.

The fix must run in the entry-point file (`run.py`, `test_gui.py`, `test_*.py`),
before any project import that touches `numpy`, `matplotlib`, or other binary
modules:

```python
import sys, os
from pathlib import Path

# 1. Find the project's own root.
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# 2. Load isolation and apply it immediately.
from hermes_manager.isolation import isolate
removed = isolate()

# 3. Report (optional) for debugging.
if removed:
    print(f"Stripped foreign paths: {removed}")
```

`isolate()` removes both `PYTHONPATH` entries and the live `sys.path` entries
that contain `"hermes"` (excluding the project directory, identified by the
marker `"hermestelegrammanager"`).

Always verify isolation with `assert_isolated()` in entry points that must
run cleanly:

```python
from hermes_manager.isolation import assert_isolated
assert_isolated()
```

This is a workflow-level requirement, not a one-off fix. A desktop app that
reads Hermes internals must import a self-contained Python environment, or any
update to Hermes' venv can silently break the GUI's binary modules.
