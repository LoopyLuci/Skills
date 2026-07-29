---
name: zeroconf-async-migration
description: "Fix zeroconf async API thread safety and registration issues"
---

# Zeroconf Async Migration

Fix common issues when using `python-zeroconf` for mDNS service discovery.

## Async API (zeroconf >= 0.131)

**WRONG** (sync, deprecated):
```python
info = zeroconf.get_service_info(service_type, name, timeout=3000)
```
Error: `Use AsyncServiceInfo.async_request from the event loop`

**RIGHT** (async):
```python
info = await zeroconf.async_get_service_info(service_type, name)
```

## Thread Safety

`ServiceBrowser` fires callbacks from its own internal thread. Store the loop:

```python
# Store it:
def set_event_loop(self, loop):
    self._loop = loop

# Callback (zeroconf thread):
def on_change(self, zc, st, name, sc):
    if hasattr(self, '_loop') and self._loop:
        asyncio.run_coroutine_threadsafe(
            self._handle(zc, st, name), self._loop)

# Handler (async thread):
async def _handle(self, zc, st, name):
    info = await zc.async_get_service_info(st, name)
```

## Registration Conflicts

```python
try:
    zeroconf.register_service(info)
except Exception as e:
    if "already" in str(e).lower():
        info.name = f"{self._name}-{suffix}.{SERVICE_TYPE}"
        zeroconf.register_service(info)
```

## Properties Are Bytes

```python
# Reading properties:
device_id = info.properties.get(b"device_id", b"").decode()
```

## Cleanup

```python
def stop(self):
    if self._zeroconf:
        try: self._zeroconf.unregister_service(self._service_info)
        except: pass
        self._zeroconf.close()
```
