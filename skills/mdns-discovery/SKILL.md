---
name: mdns-discovery
description: "Discover devices on LAN using mDNS Zeroconf from Python"
---

# mDNS Discovery

Discover services and devices on a local network using **mDNS** (Multicast DNS) / **Zeroconf**. Zero configuration.

## Python Library

```bash
pip install zeroconf
```

## Publishing a Service

```python
from zeroconf import Zeroconf, ServiceInfo
import socket

zeroconf = Zeroconf()

info = ServiceInfo(
    type_="_myservice._tcp.local.",
    name="MyDevice._myservice._tcp.local.",
    addresses=[socket.inet_aton("192.168.1.100")],
    port=8000,
    properties={"version": "1", "name": "My Device"},
)

zeroconf.register_service(info)
```

## Browsing for Services

```python
from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange

def on_change(zeroconf, service_type, name, state_change):
    if state_change == ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            device_id = info.properties.get(b"device_id", b"").decode()
            host = socket.inet_ntoa(info.addresses[0])
            port = info.port
            print(f"Found: {name} @ {host}:{port}")

zeroconf = Zeroconf()
browser = ServiceBrowser(zeroconf, "_myservice._tcp.local.", [on_change])
```

## TXT Record Properties

Attach metadata to your service advertisement:

```python
properties={
    "device_id": "uuid-here",
    "device_name": "My Laptop",
    "device_type": "windows",
}
```

Retrieve on the browsing side:
```python
val = info.properties.get(b"device_id", b"").decode()
```

## Key Patterns

| Pattern | Approach |
|---------|----------|
| Browse in background | Use `ServiceBrowser` with callbacks |
| Update properties | Call `zeroconf.update_service(info)` |
| Remove service | Call `zeroconf.unregister_service(info)` |
| Filter self | Compare `device_id` against own ID |

## Local IP Helper

```python
def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()
```

## Service Name Convention

Services use the format `_<name>._tcp.local.`:
- `_instanttransfer._tcp.local.`
- `_http._tcp.local.`
- `_ssh._tcp.local.`

## Pitfalls

- **Same network required** — mDNS does not route across subnets
- **Firewall** — Windows Firewall may block mDNS (UDP 5353)
- **VPNs** — may interfere with mDNS discovery
- **Properties are bytes** — keys/values must be under 255 bytes each
