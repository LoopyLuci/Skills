# Desktop GUI — PySide6/Qt Build + Server Boot + File Restoration

Class-level reference for the ItemForge desktop GUI. Covers the toolkit decision, the reusable module layout, threading for AI calls, the shared-DB path rule, the reliable server boot, and precise restoration of a corrupted `guilib.py`.

---

## 1. GUI toolkit decision

| Fact | Rule |
|------|------|
| Python 3.14 no longer bundles pywebview's native `_webview` C extension | `import pywebview` may succeed, but `import webview._webview` raises `ImportError`. The native C extension is the hard requirement for the native GUI. |
| Decision | Default to **PySide6 (Qt for Python) + FastAPI backend**. Only fall back to pywebview if `import webview._webview` succeeds. |
| Detection command | `import webview._webview` (run from the repo root, or set `sys.path` first). Failure to import = PySide6/Qt. |

**Why:** pywebview is pure-Python on the `guilib.py` side, but the GUI engine itself is a native extension (`_webview`). On Python 3.14 that extension is not built/installed, so every pywebview GUI attempt silently fails at show time. The signal to switch is the import check, not an error message.

## 2. GUI module layout

| File | Role |
|------|------|
| `app/gui/forge_service.py` | Data-access layer: wraps `app.services` + `app.database`. Single `ForgeService` singleton. Keeps the GUI decoupled from the backend HTTP layer. |
| `app/gui/models.py` | Qt data model, e.g. `ItemsTableModel` for `QStandardItemModel` display. |
| `app/gui/pages.py` | Page widgets (items list + detail, listings, status, settings), PySide6 widgets. |
| `app/gui/forge_window.py` | `QMainWindow` with fixed-width `QListWidget` sidebar (menu → stacked page) + `QStackedWidget` content area. |
| `app/gui/main.py` | Entry: build `QApplication`, `MainWindow`, `exec()`. |

**Layout rule:** one `QMainWindow` → sidebar navigation + `QStackedWidget`. Each page is a `QWidget` with `QVBoxLayout` (filter/search bar, `QListWidget`, right-side `ItemDetailWidget`).

## 3. Threading for AI calls

Long-running AI calls must not block the UI thread. Worker pattern:

```python
from PySide6.QtCore import QObject, Signal, QThreadPool

class _Worker(QObject):
    done = Signal(object)
    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(coro)
            self.done.emit(result)
        except Exception as e:
            self.done.emit(e)

# submit:
_w = _Worker()
QThreadPool.globalInstance().start(_w)
```

`run_ai(coro)` in `pages.py` wires a coroutine to this worker and reports results on the main thread.

## 4. Shared database path

- The backend chdirs to the repo root at startup → opens `<repo>/itemforge.db`.
- The GUI data layer must resolve the DB **against the repo root**, not the CWD. Otherwise it opens an empty `<CWD>/itemforge.db` and shows nothing.
- In `forge_service.py`:

```python
import app.database
from pathlib import Path
_app_root = Path(__file__).resolve().parent.parent.parent
app.database.DB_PATH = _app_root / "itemforge.db"
```

## 5. Reliable server boot

The terminal tool's `nohup`/`&` and plain `subprocess.Popen` often kill the child before it binds. Reliable pattern — a launch script:

```python
import subprocess, time, urllib.request

PORT = 8000
BASE = f"http://127.0.0.1:{PORT}"
proc = subprocess.Popen(
    ["python3", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(PORT)],
    cwd="Z:/Projects/ModelMistress/itemforge",
    stdout=open("server8000.log", "w"), stderr=subprocess.STDOUT,
)

def wait_ready(timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urllib.request.urlopen(BASE + "/health", timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.5)
    return False

# seed real DB, then keep the script alive so the child keeps running
# (do NOT terminate proc in a finally block if you want the server persistent)
proc.wait()
```

Verify with: `curl -s http://127.0.0.1:8000/health` → `{"status":"healthy","service":"itemforge"}`

## 6. Restoring a corrupted `guilib.py`

If pywebview's `guilib.py` was accidentally overwritten (e.g. by a GUI data-layer write), restore it byte-precisely:

```bash
pip download pywebview==6.2.1 --no-deps --no-build-isolation -d /tmp/pywebview_wheel
python -m zipfile -e /tmp/pywebview_wheel/pywebview-6.2.1-py3-none-any.whl /tmp/pywebview_wheel/extracted
cp /tmp/pywebview_wheel/extracted/webview/guilib.py <pywebview>/Lib/site-packages/webview/guilib.py
```

Then verify:

```bash
wc -c <pywebview>/Lib/site-packages/webview/guilib.py   # expect 3823
head -1 <pywebview>/Lib/site-packages/webview/guilib.py # expect 'from __future__ import annotations'
grep -c 'forge_service' <pywebview>/Lib/site-packages/webview/guilib.py   # expect 0
```

The genuine pywebview `guilib.py` (6.2.1) is exactly **3823 bytes**, starts with `from __future__ import annotations`, and contains `webview.platforms` module imports — it does **not** contain an `ItemForge Desktop GUI - Data access layer` docstring.

## 7. Verification checklist (end-to-end)

1. Backend: all modules import; `uvicorn app.main:app` boots; `curl /health` → `{"status":"healthy","service":"itemforge"}`.
2. Seed data: `itemforge.db` has items and listings; `GET /v1/forge/items` returns them with `images` field; `GET /v1/forge/listings` returns `item_id` mappings.
3. GUI imports: `from app.gui import pages, forge_window, main` + `forge_service` — all OK.
4. GUI data layer: `ForgeService().items_with_images()` and `.get_listings()` return the same rows the backend serves.
5. MainWindow constructs: `QApplication` + `MainWindow().show()` → window titled "ItemForge", 4-page sidebar + stack.
6. `guilib.py` restored: byte-identical to the wheel.
