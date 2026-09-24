# Threading + asyncio Bridge Pattern

For PyQt5 apps that need to run async operations (SSH, QMP, HTTP) in background threads.

## Pattern: threading.Thread + asyncio

Prefer `threading.Thread` over `QThread` for asyncio bridges — simpler and more reliable on Windows.

```python
import asyncio
import threading
from PyQt5.QtCore import QObject, pyqtSignal

class Bridge(QObject):
    """Background bridge that runs asyncio event loop in a thread."""
    connected = pyqtSignal(bool)
    error = pyqtSignal(str)
    data_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._loop = None
        self._thread = None
        self._running = False

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)

    def _run_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    async def _do_work(self):
        """Override this method."""
        pass
```

## QThread + asyncio Alternative

```python
class BridgeThread(QThread):
    result_ready = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self._async_work())
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurped.emit(str(e))
        finally:
            loop.close()

    async def _async_work(self):
        """Override this method."""
        pass
```

## Pitfalls

1. **QThread + asyncio**: Must create new event loop in `run()`, not reuse. Windows + QThread + asyncio can deadlock if the loop is created in `__init__`.

2. **Signal emission from asyncio**: Always use `pyqtSignal` to communicate back to the GUI thread. Never call Qt widget methods directly from asyncio coroutines.

3. **Cleanup**: Always stop the event loop before joining the thread. Use `call_soon_threadsafe(loop.stop)` to avoid race conditions.

4. **Error handling**: Wrap `run_until_complete()` in try/except and emit an error signal. Unhandled exceptions in asyncio threads crash silently.
