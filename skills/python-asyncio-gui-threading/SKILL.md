---
name: python-asyncio-gui-threading
description: "Run async code alongside CustomTkinter GUI without crashes"
---

# Python Asyncio + GUI Threading

Running async network code alongside a synchronous GUI requires careful threading.

## Architecture

Main thread (GUI) + background thread (asyncio) + queue to bridge them.

## Pattern

```python
import asyncio, threading, queue
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._loop = None
        self._async_queue = queue.Queue()
        self._start_async()
        self.after(100, self._poll)

    def _start_async(self):
        def run():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._async_main())
        threading.Thread(target=run, daemon=True).start()

    async def _async_main(self):
        await asyncio.sleep(1)

    def _schedule(self, fn):
        self._async_queue.put(fn)

    def _poll(self):
        try:
            while True:
                self._async_queue.get_nowait()()
        except queue.Empty:
            pass
        self.after(50, self._poll)

    def _run_async(self, coro):
        asyncio.run_coroutine_threadsafe(coro, self._loop)
```

## Critical Rule

Never call `get_event_loop()` from callbacks. Store the loop:

```python
# WRONG — crashes from mDNS/timer threads
asyncio.run_coroutine_threadsafe(coro(), asyncio.get_event_loop())

# RIGHT — use stored reference
self._loop = loop
asyncio.run_coroutine_threadsafe(coro(), self._loop)
```

## Shutdown

```python
def destroy(self):
    self._cleanup()
    try:
        super().destroy()
    except tkinter.TclError:
        pass  # Already destroyed
```
