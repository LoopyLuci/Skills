# Async Backend Adapter Pattern

## Problem

GUI panels (PyQt5) run on the main thread and call methods synchronously. Backend
methods (Docker, Kubernetes, QEMU, VMware, etc.) are `async def`. Calling them
without `await` returns a coroutine object, not the actual result:

```python
# WRONG — returns coroutine, not data
containers = backend.list_containers()  # coroutine object, not list

# CORRECT — use adapter
from gui.async_adapter import get_adapter
containers = get_adapter().docker.list_containers()  # actual list
```

## Solution: AsyncAdapter Singleton

```python
class AsyncAdapter:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._loop.run_forever, daemon=True
        )
        self._thread.start()

    def _run_async(self, coro):
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result(timeout=30)
```

## Per-Backend Adapters

Each backend gets its own adapter class that:
1. Wraps async methods with `self._run(coro)`
2. Normalizes return values to dicts for GUI consumption
3. Handles backend connection lazily

```python
class _DockerAdapter:
    def __init__(self, backend, run_async):
        self._backend = backend
        self._run = run_async

    def list_containers(self, all: bool = True) -> list:
        containers = self._run(self._backend.list_containers(all=all))
        result = []
        for c in containers:
            if hasattr(c, 'name'):
                result.append({
                    "name": c.name,
                    "image": str(c.image) if hasattr(c, 'image') else "",
                    "status": c.status if hasattr(c, 'status') else "",
                    "ports": str(c.ports) if hasattr(c, 'ports') else "",
                })
            elif isinstance(c, dict):
                result.append(c)
        return result
```

## Integration Test Pattern

1. Write test suite that exercises ALL backends
2. Run tests → identify coroutine warnings (`RuntimeWarning: coroutine ... was never awaited`)
3. Create AsyncAdapter to bridge async → sync
4. Re-run tests → verify all pass
5. Build exe with adapter in `--hidden-import`

```bash
# Run integration tests
.venv/Scripts/python.exe -m unittest tests.test_integrations -v

# Check for async issues
grep -n 'coroutine.*never awaited' logs/vmharness.log
```

## Common Normalization Patterns

| Backend Returns | GUI Expects | Adapter Does |
|-----------------|-------------|--------------|
| `Container` object with `.name`, `.status` | `dict` with `"name"`, `"status"` | `hasattr` check → dict |
| `list[str]` (just VM names) | `list[dict]` with `"name"` key | `isinstance(str)` → wrap in dict |
| `Image` object with `.tags` | `dict` with `"repository"` | Extract `tags[0]` as repository |
| `CommandResult` object | `str` (stdout) | `result.stdout` |
| `VMStatus` dataclass | `str` status like `"running"` | `status.state.value` if nested, `status.value` if flat |
| `list[str]` (VirtualBox `list_vms()`) | `list[dict]` for GUI | Wrap each name as `{"name": vm}` |

## VirtualBox Backend Quirks

- `list_vms()` returns `list[str]` (VM names), NOT `list[dict]` — wrap each in adapter
- `stop_vm(name, force=True)` uses `controlvm poweroff`; `force=False` uses `acpipowerbutton`
- No `power_off()` / `power_on()` methods — use `start_vm()` / `stop_vm()`
- `get_status()` returns a `VMStatus` dataclass with `state` field being a `VMState` enum — adapter must return `status.state.value`
- `stop_vm()` raises error on already-stopped VM — wrap initial stop in `try/except`

## Abstract Method Naming

Before writing integration tests, ALWAYS check that abstract base class method
names match implementation names:

```bash
grep -n 'def execute_command\|def exec_command' \
  src/vm_harness/container/backend.py \
  src/vm_harness/container/docker/backend.py \
  src/vm_harness/container/kubernetes/backend.py
```

If they differ (e.g., abstract says `execute_command` but implementation
uses `exec_command`), rename the abstract method to match the implementation.
```
