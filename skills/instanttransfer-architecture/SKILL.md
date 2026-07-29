---
name: instanttransfer-architecture
description: "Design choices for InstantTransfer LAN file sync tool"
---

# InstantTransfer Architecture

Design decisions for the InstantTransfer LAN file transfer app.

## Core Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Transport | Direct TCP over LAN | Fastest no cloud |
| Discovery | mDNS Zeroconf | Zero config automatic |
| Pairing | 6-digit PIN dual approval | Simple verifiable |
| Windows GUI | CustomTkinter | Modern native feel |
| Android GUI | Jetpack Compose | Material 3 |
| Async | asyncio | Python native |

## Protocol

Control port: 48761. Messages: [4-byte length][JSON payload]
Max message: 10MB. Chunk size: 1MB.

## Connection Flow

mDNS broadcast -> discover -> TCP connect -> HELLO -> pairing or transfer

## Threading

Async event loop in background thread. Queue bridges to GUI thread.

## Lessons Learned

1. Store event loop ref never get_event_loop from callbacks
2. Use async_get_service_info in new zeroconf
3. Fallback names for mDNS registration conflicts
4. Guard destroy against TclError
5. Path formats differ bash Java Python on Windows
6. mDNS callbacks fire from non-async thread
