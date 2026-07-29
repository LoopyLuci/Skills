---
name: instanttransfer-protocol
description: "InstantTransfer wire protocol pairing and file transfer spec"
---

# InstantTransfer Protocol

The InstantTransfer protocol enables instant LAN-based file transfer between Windows and Android. No cloud, no internet.

## Transport

- **TCP** connections, length-prefixed JSON messages
- Format: `[4-byte big-endian length][JSON payload]`
- **Control port:** 48761

## Message Format

```json
{
  "type": "MESSAGE_TYPE",
  "payload": { ... }
}
```

## Message Types

| Message | Purpose |
|---------|---------|
| HELLO | Handshake with device info |
| PAIR_INIT | Start 6-digit PIN pairing |
| PAIR_PIN | Send generated PIN |
| PAIR_APPROVE | User approved pairing |
| PAIR_CONFIRM | Exchange permanent device IDs |
| PAIR_ACK | Acknowledge pairing is stored |
| PAIR_DECLINE | User declined |
| FILE_OFFER | Offer files for transfer |
| FILE_ACCEPT | Accept incoming transfer |
| FILE_REJECT | Reject incoming transfer |
| FILE_META | File metadata (name, size) |
| FILE_CHUNK | Binary data chunk (1MB) |
| FILE_DONE | Transfer complete signal |
| FILE_ERROR | Error occurred |
| CANCEL | Cancel transfer |
| BYE | Clean disconnect |

## Discovery

Devices broadcast via **mDNS** under `_instanttransfer._tcp` with TXT records:

| Record | Purpose |
|--------|---------|
| `device_id` | Permanent UUID |
| `device_name` | Human-readable name |
| `device_type` | "windows" or "android" |
| `paired_ids` | Comma-separated known device IDs |

## Pairing Flow

```
Initiator                    Receiver
   │                           │
   ├── HELLO ────────────────► │
   │ ◄── HELLO ───────────────┤
   │                           │
   ├── PAIR_INIT ────────────► │
   │ ◄── PAIR_PIN (6-digit) ──┤
   │                           │
   │  (Both display PIN)       │
   │  (User taps Approve)      │
   │                           │
   ├── PAIR_APPROVE ─────────► │
   │ ◄── PAIR_APPROVE ────────┤
   │                           │
   ├── PAIR_CONFIRM ─────────► │
   │ ◄── PAIR_ACK ────────────┤
   │                           │
   │   ✅ Paired permanently   │
```

## File Transfer Flow

```
Sender                       Receiver
  │                            │
  ├── FILE_OFFER (file list)  ►│
  │ ◄── FILE_ACCEPT ──────────┤
  │                            │
  │  For each file:            │
  ├── FILE_META ─────────────►│
  ├── FILE_CHUNK (1MB) ──────►│
  ├── FILE_CHUNK ... ────────►│
  ├── FILE_DONE ─────────────►│
  │                            │
  │   ✅ Transfer complete     │
```

## Constants

| Constant | Value |
|----------|-------|
| CONTROL_PORT | 48761 |
| CHUNK_SIZE | 1,048,576 bytes (1 MB) |
| MAX_PARALLEL | 4 streams |
| PAIR_TIMEOUT | 30 seconds |
| MAX_MESSAGE | 10 MB |
