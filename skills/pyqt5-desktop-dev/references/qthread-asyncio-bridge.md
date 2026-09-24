# Threading + Asyncio Bridge for PyQt5

Run async operations (SSH, QMP, HTTP calls, etc.) on a background thread while
keeping the GUI responsive. The bridge is a QObject that owns a `threading.Thread`
(NOT QThread), runs an asyncio event loop on it, and emits PyQt5 signals on completion.

## When to Use

- Any PyQt5 panel that needs to call async functions without blocking the UI
- SSH/terminal panels, QMP control panels, telemetry refresh, any network I/O
- When the async API is module-level functions (not a class) — common with
  asyncssh-based clients

## Threading.Thread vs QThread

**Use `threading.Thread` (NOT QThread) for asyncio bridges.** QThread's `run()` method
executes in the thread, but `moveToThread` + `start` + `started.connect` has subtle
race conditions on Windows. `threading.Thread` with `daemon=True` is simpler and more
reliable for running a persistent asyncio loop.

## Architecture

```
QWidget Panel  ←  pyqtSignal  →  QObject Bridge  →  threading.Thread + asyncio loop
     (slots)                        (methods call                  (run()
                                     async functions)               loop.run_forever)
```

## Bridge Skeleton

```python
import asyncio
import threading
from PyQt5.QtCore import QObject, pyqtSignal

class AsyncBridge(QObject):
    finished = pyqtSignal(bool, str)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._thread = None
        self._loop = None
        self._loop_ready = threading.Event()

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return
        self._loop_ready.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        if not self._loop_ready.wait(timeout=5.0):
            raise RuntimeError("Bridge event loop failed to start within 5s")

    def _run_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop_ready.set()
        self._loop.run_forever()

    def _schedule(self, coro):
        if self._loop is None or not self._loop.is_running():
            self.error.emit("Bridge not running")
            return
        asyncio.run_coroutine_threadsafe(coro, self._loop)

    def stop(self):
        if self._loop is not None and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread is not None:
            self._thread.join(timeout=5.0)
```

## Key Rules

1. **`threading.Thread(daemon=True)`** — thread dies with the main process; no hangs on exit
2. **`threading.Event`** — use `_loop_ready` event to wait for loop initialization
3. **`asyncio.run_coroutine_threadsafe()`** — schedule coroutines from the GUI thread
4. **`call_soon_threadsafe(self._loop.stop)`** — stop the loop from another thread
5. **module-level async functions are called with `await`** — they are NOT class methods
6. **clean up on close** — call `bridge.stop()` in MainWindow.closeEvent BEFORE `app.quit()`

## Pitfalls

- **`loop.run_until_complete()` on every call** — creates a new loop each time, blocks the thread.
  Use `run_forever()` + `run_coroutine_threadsafe()` instead.
- **Emitting signals from async function body** — async function may run on a different thread
  than the bridge's thread. Use `pyqtSignal.emit()` which is thread-safe in PyQt5.
- **Forgetting to stop the loop** — process hangs on exit. Always call `loop.stop()` via
  `call_soon_threadsafe` before `thread.join()`.
- **Assuming async functions are class methods** — many async SSH/QMP libraries expose
  module-level functions. Verify the API: it may be `ssh_client.connect()` not
  `SSHClient().connect()`.
- **SSH connection leak** — when the bridge reconnects on every call instead of reusing
  a cached connection, you get 20+ stale connections. Add a `_connecting` flag to prevent
  concurrent connect attempts, and ensure the underlying client caches connections with
  an asyncio lock.
- **No clean shutdown** — without signal handlers, background threads leak on exit.
  Install `signal.SIGINT`/`signal.SIGTERM` handlers that call `_cleanup()` before
  `sys.exit(0)`. Wrap `app.run()` in try/except to catch crashes and clean up.
- **`setStretchFactor` requires int, not float** — `setStretchFactor(widget, 0.5)` raises.
  Use integer stretch factors only.
- **`QTextBrowser` for display-only text** — prefer `QTextBrowser` over `QTextEdit` when
  the widget is purely for display (log viewers, terminal output). `QTextEdit` when the
  user can edit.
- **matplotlib backend: `backend_qtagg`, not `backend_qt`** — matplotlib ≥ 3.8 renamed the
  Qt backend. `FigureCanvasQTAgg` is now `FigureCanvasQtAgg` under `backend_qtagg`.
  Import: `__import__("matplotlib.backends.backend_qtagg", fromlist=["FigureCanvasQtAgg"]).FigureCanvasQtAgg`
