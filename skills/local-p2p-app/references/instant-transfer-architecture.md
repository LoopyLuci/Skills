# InstantTransfer — Architecture & Design

## Overview
A pair of apps (Windows desktop + Android) that transfer files of any size and quantity **instantly** over the local network. No cloud, no internet dependency — pure LAN peer-to-peer.

## Core Principles
1. **Speed** — Direct TCP socket transfer over LAN, parallel streams for large files
2. **No size limits** — Streaming transfers, not loading into memory
3. **No count limits** — Batch folder transfers with directory structure preservation
4. **Zero setup** — Auto-discovery via mDNS, QR pairing fallback
5. **Resumable** — Partial transfers can resume on reconnection

## Architecture

### Discovery Protocol (mDNS/ZeroConf)
- Both apps broadcast a service type `_instanttransfer._tcp` on the LAN
- Each device advertises: device name, device type (Windows/Android), version
- No router config needed — works on any local network (including mobile hotspot)

### Transfer Protocol
- **Control channel**: Persistent TCP connection for commands (list, send, receive, cancel)
- **Data channel**: Separate TCP connections per file transfer, parallelizable
- **Protocol format**: JSON control messages over length-prefixed frames
- **File streaming**: Chunked transfer (1MB chunks) with CRC32 verification
- **Parallelism**: Up to 4 simultaneous file streams for large files (>50MB)
- **Encryption**: Optional TLS (self-signed certs, trust-on-first-use)

## Pairing Protocol (PIN-based, permanent)

### Flow
1. **Discovery** — Both devices broadcast via mDNS: `_instanttransfer._tcp`. Each advertisement includes `device_id` (UUID), `device_name`, `device_type`, and `paired=<comma-separated known IDs>`.
2. **Initiate** — User taps "Pair" on Device A next to Device B's listing.
3. **PIN Generation** — Device A sends a `PAIR_INIT` message to Device B. Device B generates a random 6-digit PIN and sends it back. **Both devices display the same PIN.**
4. **Approval** — Both users see: *"Approve pairing with [Device Name]? Code: [XXXXXX]"* with Approve / Decline buttons. Both must tap Approve within 30 seconds.
5. **Confirmation** — When both approve, Device A sends `PAIR_CONFIRM` with its permanent device info. Device B stores A as paired and sends `PAIR_ACK`. Device A stores B as paired.
6. **Permanent** — Paired devices are stored in `paired_devices.json` (or Android SharedPreferences). On future discovery, they recognize each other and auto-connect — no pairing prompt ever again.

### Persistence
- Each device generates a **permanent UUID** on first launch (stored in config)
- Paired devices are stored with: device_id, name, device_type, paired_at timestamp
- To unpair: user goes to settings → Manage Paired Devices → Remove

### Security
- PIN is 6 digits (1,000,000 combinations) — sufficient for LAN pairing
- Timeout of 30s after PIN display
- Rate limit: max 3 pairing attempts per minute from same IP

---

### Message Types (Control Channel)
| Message | Direction | Purpose |
|---------|-----------|---------|
| `HELLO` | Both | Handshake with device info |
| `DIR_LIST` | Both | Request/send directory listing |
| `FILE_OFFER` | Windows→Android | Offer file(s) for transfer |
| `FILE_ACCEPT` | Android→Windows | Accept transfer |
| `FILE_REJECT` | Android→Windows | Reject transfer |
| `FILE_META` | Sender→Receiver | File metadata (name, size, modified, checksum) |
| `FILE_CHUNK` | Sender→Receiver | Binary data chunk |
| `FILE_DONE` | Sender→Receiver | Transfer complete signal |
| `FILE_ERROR` | Either | Error occurred |
| `CANCEL` | Either | Cancel in-progress transfer |
| `PROGRESS` | Receiver→Sender | Periodic progress updates |
| `BYE` | Either | Disconnect |

---

## Windows App (Python)

### Stack
- **GUI**: CustomTkinter (modern, native-feel themed)
- **Network**: asyncio + raw sockets
- **Discovery**: python-zeroconf
- **File handling**: aiofiles for async I/O
- **Build**: PyInstaller → single .exe

### UI Screens
1. **Discovery** — Auto-finds nearby devices, shows them as cards
2. **File Browser** — Tree view of local files/folders, drag-select or checkbox
3. **Transfer Queue** — Active transfers with progress bars, speed, ETA
4. **History** — Recent transfers log
5. **Settings** — Download folder, max parallel streams, theme

### Key Features
- Drag & drop files/folders onto device cards to send
- System tray background operation
- Right-click → "Send via InstantTransfer" in Explorer context menu
- Auto-accept from trusted devices option
- Bandwidth throttle setting

---

## Android App (Kotlin)

### Stack
- **UI**: Jetpack Compose with Material 3
- **Network**: Kotlin coroutines + NIO sockets
- **Discovery**: Android NSD (Network Service Discovery) API
- **File access**: SAF (Storage Access Framework) + MediaStore
- **Build**: Gradle with Kotlin DSL

### UI Screens
1. **Home/Discovery** — Shows discovered Windows devices on the LAN
2. **File Picker** — System file picker (SAF) for selecting files/folders
3. **Receive** — Shows incoming file offers with accept/reject
4. **Transfers** — Active and completed transfers with progress
5. **Settings** — Save location, auto-accept, theme

### Key Features
- Background file receiving (Foreground Service with notification)
- Share sheet integration — "Share via InstantTransfer" from any app
- Download to SD card or internal storage
- Notification on transfer complete
- Batch send from gallery/file manager

---

## Project Structure

```
InstantTransfer/
├── ARCHITECTURE.md         ← This file
├── protocol.md             ← Protocol specification
├── windows/                ← Python Windows app
│   ├── main.py
│   ├── requirements.txt
│   ├── src/
│   │   ├── gui/            ← UI components
│   │   ├── network/        ← Discovery + transfer protocol
│   │   ├── models/         ← Data models
│   │   └── utils/          ← Helpers
│   ├── resources/          ← Icons, themes
│   └── build.spec          ← PyInstaller config
├── android/                ← Kotlin Android app
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/instanttransfer/
│   │   │   │   ├── ui/         ← Compose screens
│   │   │   │   ├── network/    ← Discovery + transfer
│   │   │   │   ├── service/    ← Foreground service
│   │   │   │   └── data/       ← Models, repo
│   │   │   ├── res/
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle.kts
│   ├── gradle/
│   └── settings.gradle.kts
└── README.md
```
