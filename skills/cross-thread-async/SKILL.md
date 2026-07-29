---
name: cross-thread-async
description: "Debug asyncio callbacks from non-async threads GUI or mDNS"
---

# Cross-Thread Async Patterns

Handle asyncio callbacks that fire from **non-async threads** — GUI event loops, mDNS service browsers, hardware polling, or thread-pool workers.

## The Problem

When `asyncio.get_event_loop()` is called from a thread that wasn't started by `asyncio.run()`, Python 3.10+ raises:

```
RuntimeError: There is no current event loop in thread 'zeroconf-ServiceBrowser-...'
```

Because `asyncio.run()` installs the loop only on the calling thread. Sub-threads do not inherit it.

## The Fix: Store the Loop Reference

```python
class ServiceWithCallbacks:
    def __init__(self):
        self._loop = None  # Set externally

    def set_event_loop(self, loop):
        self._loop = loop

    def _on_service_state_change(self):
        # WRONG — fails in non-async threads:
        # asyncio.get_event_loop()  → RuntimeError

        # RIGHT:
        asyncio.run_coroutine_threadsafe(
            self._on_device_added(),
            self._loop  # stored reference
        )
```

**Wire at startup:**
```python
loop = asyncio.get_running_loop()
service.set_event_loop(loop)
```

## When This Pattern Applies

| Scenario | Library | Thread Source |
|----------|---------|--------------|
| mDNS discovery | `zeroconf` | ServiceBrowser background thread |
| GUI toolkit | `tkinter`, `PyQt`, `CustomTkinter` | Main thread ≠ async loop thread |
| File watcher | `watchdog` | Observer thread |
| Hardware events | `pyserial`, `bluetooth` | Reader threads |
| Thread pool | `concurrent.futures` | Worker threads |

## Alternative: Dedicated Async Thread

When ALL async work lives in a background thread:

```python
def background_worker():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

thread = threading.Thread(target=background_worker, daemon=True)
thread.start()
# Now get_event_loop() works inside this thread
```

Use this for pure async-daemon patterns. Don't use it if the main thread also needs async.

## Detecting the Bug Early

```python
# Add a guard at API boundaries
import asyncio

def schedule_coro(coro):
    try:
        loop = asyncio.get_running_loop()
        # We're in an async context — schedule directly
        asyncio.ensure_future(coro)
    except RuntimeError:
        # No running loop — must have stored reference
        raise RuntimeError(
            "Called from non-async thread without stored loop reference"
        )
```

## Source of the Pattern

Discovered while debugging the InstantTransfer project:
- `zeroconf.ServiceBrowser` fires `ServiceStateChange` callbacks from a background thread
- Calling `asyncio.get_event_loop()` there raises `RuntimeError`
- Fix: store `self._loop = asyncio.get_running_loop()` in the async init, use `asyncio.run_coroutine_threadsafe(coro, self._loop)` in callbacks
