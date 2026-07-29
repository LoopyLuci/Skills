---
name: p2p-lan-transfer
description: "Peer to peer file transfer patterns for local networks"
---

# P2P LAN File Transfer

Patterns and approaches for direct device-to-device file transfer over a local network. No cloud, no internet required.

## When to Use

| Scenario | Best Approach |
|----------|---------------|
| Same WiFi network | Direct TCP over LAN |
| Mobile hotspot | Direct TCP (both on hotspot) |
| Ethernet + WiFi | Direct TCP (same subnet) |
| Different subnets | UPnP / NAT traversal or relay |
| No network | WiFi Direct or USB tethering |

## Architecture Options

### 1. Direct TCP (Simplest)

```
Device A (server) ←→ TCP connection ←→ Device B (client)
```

- One device acts as TCP server
- Other connects directly
- Fastest possible speed (full LAN bandwidth)
- No dependencies beyond Python stdlib

### 2. WebSocket

```
Device A ←→ WebSocket ←→ Device B
```

- Built-in browser support
- Framing protocol built in
- Slightly more overhead than raw TCP

### 3. WebRTC

```
Device A ←→ WebRTC ←→ Device B
```

- NAT traversal built in
- Browser-compatible
- Works across some subnets
- Complex setup

## Recommended: Direct TCP

For Python-to-Python transfers on the same LAN, direct TCP is fastest and simplest:

```python
# Server
import asyncio

async def handle_client(reader, writer):
    # Receive file metadata
    data = await reader.readexactly(4)
    # ... receive file

async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 8877)
    await server.serve_forever()

# Client
async def send_file(host, port, filepath):
    reader, writer = await asyncio.open_connection(host, port)
    # Send file
    writer.write(data)
    await writer.drain()
```

## Discovery Methods

| Method | Library | Requires |
|--------|---------|----------|
| mDNS | `zeroconf` | Same network, UDP 5353 open |
| Broadcast ping | UDP broadcast | Same subnet |
| Manual IP | User input | User knows the IP |
| QR code | `qrcode` | One device has a screen |

## Speed Optimization

| Technique | Gain |
|-----------|------|
| Chunk size 1MB | Reduces syscall overhead |
| Parallel streams (2-4) | 2-4x on high-latency links |
| TCP_NODELAY | Reduces Nagle algorithm delay |
| Large socket buffers | 256KB+ for fast networks |
| Async I/O | Non-blocking, efficient |

## Security

- **Same network** = same trust domain (typically)
- **Add pairing/PIN** to prevent unauthorized access
- **TLS** for encryption over LAN (self-signed certs)
- **Rate limit** connection attempts to prevent scanning

## Pitfalls

- **Windows Firewall** blocks inbound connections by default
- **Mobile networks** isolate devices (carrier NAT)
- **Company WiFi** may have client isolation (AP isolation)
- **VPNs** route traffic externally, defeating LAN transfer
