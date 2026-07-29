---
name: local-p2p-app
description: >-
  Build LAN P2P apps with discovery, PIN pairing, streaming.
---

# Building Local P2P Applications

Trigger: user asks to build an app where two or more devices on the same LAN
discover each other, pair, and exchange data — file transfer, remote control,
sync tools, chat, screen sharing, etc.

## Architecture Canvas

Before writing any code, produce a short architecture doc covering:

1. **Discovery** — How devices find each other on the LAN without typing IPs
2. **Connection** — What transport (TCP/WebSocket/UDP) and how the control vs data channels are separated
3. **Pairing** — How trust is established (PIN, QR, manual accept)
4. **Data transfer** — Message format, chunking, parallelism, error recovery
5. **Persistence** — What state survives restarts (paired devices list, settings)

## Step 1 — Protocol Layer

Design a length-prefixed JSON message format over TCP:

```
[4-byte big-endian length][JSON payload]
```

Define message types as an enum. Keep the core messages lean — you can always add more:

- `HELLO` — handshake with device info
- Direction-specific messages (e.g., `FILE_OFFER`, `FILE_META`, `FILE_CHUNK`, `FILE_DONE`)
- Control messages (`CANCEL`, `BYE`, `PING`/`PONG`)
- Pairing messages (`PAIR_INIT`, `PAIR_PIN`, `PAIR_APPROVE`, `PAIR_CONFIRM`, `PAIR_ACK`)

**Pitfall**: Enforce a max message size (e.g. 10MB on control channel). For file data, send it in chunks and separate the data channel from the control channel when throughput matters.

## Step 2 — Discovery (mDNS / NSD)

**Windows (Python)**: Use `zeroconf` library. Register a service of type `_<appname>._tcp.local.`. Include key metadata in TXT records (`device_id`, `device_name`, `device_type`, `paired_ids`).

**Android**: Use `NsdManager` (Network Service Discovery API). Register and discover the same service type. Resolve services to get host/port.

**Pitfall**: Android NsdManager's `getAttribute()` method changed across API levels. Use reflection or a utility function to read TXT records. On Android 14+, you may need `NEARBY_WIFI_DEVICES` permission.

**Pitfall**: mDNS only works within the same broadcast domain (subnet). On enterprise WiFi with client isolation, this won't work.

### Production-Grade Discovery (Liveness + Quality)

For a production P2P app, basic mDNS discovery is not enough. Add these layers:

**Device data model**: Each discovered device should carry:
```
Device:
  device_id, name, device_type, host, port, paired
  first_seen, last_seen, last_heartbeat   # timing
  connection_quality: ConnectionQuality   # enum: EXCELLENT, GOOD, FAIR, POOR, OFFLINE
  rtt_ms: float                           # round-trip time in ms
  _online: bool                           # computed liveness flag
```

**Heartbeat monitor**: A background thread that runs every ~15s and marks devices OFFLINE when `last_seen` exceeds a threshold (e.g. 45s). This handles devices that leave the network without sending an mDNS goodbye.

**Connection quality estimation**: Classify connections based on subnet:
- `192.168.x.x` or `10.x.x.x` → EXCELLENT (same subnet)
- `172.16-31.x.x` → GOOD (private VLAN)
- Cross-subnet → FAIR or POOR

Refine with actual RTT when available: `<5ms` Excellent, `<20ms` Good, `<100ms` Fair, `>100ms` Poor.

**Multi-callback notification**: Three distinct callbacks let the UI update cleanly:
```
on_device_online(device)   # Device first seen or came back
on_device_offline(device)  # Device went away (heartbeat timeout)
on_device_updated(device)  # Device metadata changed (e.g., name update)
```

**Persistent device registry**: Keep a dict of all known devices (including offline ones). Only purge after extended absence or explicit user removal. Paired devices persist in the registry indefinitely even when offline — this lets the GUI show "Offline — 2 known devices" status.

**Pitfall**: Without heartbeat monitoring, devices that disconnect without a clean mDNS removal (network drop, sleep mode, airplane mode) remain "online" in your UI indefinitely. Always pair mDNS discovery with a periodic liveness check.

**Pitfall**: The `_online` flag should be computed from `last_seen` timing, not set directly by mDNS events. An mDNS "added" event updates `last_seen`; the heartbeat loop marks `_online = false` when timeout is exceeded. This decouples event timing from state.

## Step 3 — Pairing (PIN-based, Permanent)

Design a handshake that establishes permanent trust:

1. **Initiation** — User clicks "Pair" → `PAIR_INIT` sent to peer
2. **PIN generation** — Receiver generates 6-digit random PIN, sends it back, both display it
3. **Dual approval** — Both users see the same PIN and tap "Approve" within a timeout (30s is good)
4. **Confirmation** — Exchange device info via `PAIR_CONFIRM`/`PAIR_ACK`
5. **Storage** — Each side saves the other's device_id, name, type, and paired_at timestamp permanently

**Why PIN works**: 6 digits = 1M combinations, plenty for LAN. The dual-approval prevents a MITM who can see the PIN but can't get the user to tap "Approve".

### Pairing State Machine (Production)

Model pairing as an explicit state machine. This prevents edge cases (double-approve, timeout-after-approve, race conditions):

```
IDLE → CONNECTING → PIN_DISPLAYED → WAITING_APPROVAL → APPROVED → CONFIRMED
                                      ↓                   ↓
                                 DECLINED/CANCELLED    TIMEOUT/ERROR
```

Terminal states: CONFIRMED (success), DECLINED, CANCELLED, TIMEOUT, ERROR.

**Implementation**: Use a `PairingSession` dataclass to hold all session state:
```
PairingSession:
  state: PairingState
  pin: str
  peer_device_id, peer_device_name, peer_device_type
  peer_host, peer_port
  reader, writer (async Stream)
  started_at, pin_displayed_at (timestamps for timeout tracking)
  is_initiator: bool
```

**Rate limiting**: Track timestamps of pairing attempts. Allow max 3 per 60s window. Return remaining lockout time in the error message so the UI can show "Try again in 47s."

**Timeout**: After PIN is displayed, start a 30s countdown. If the user has not approved by then, auto-cancel. Prevents stale pairing dialogs from lingering.

**Pitfall**: The state machine must handle the `approve()` call from BOTH the initiator and receiver paths. The initiator sends PAIR_APPROVE then reads; the receiver reads PAIR_APPROVE then sends one. Both paths converge at the same `_finalize()` method.

**Pitfall**: Rate-limit pairing attempts (3 per 60s per IP) to prevent brute force. Cancel after timeout automatically.

**Pitfall**: When a paired device comes back online, it should auto-connect without re-pairing. On discovery, check if the peer's device_id is in your paired list AND if your device_id is in the peer's `paired_ids` TXT record.

## Step 4 — Data Transfer

For file/streaming data:

1. **Offer** — Sender sends `FILE_OFFER` with metadata (file count, total size, file list)
2. **Accept/Reject** — Receiver chooses to accept or reject
3. **Per-file streaming** — For each file: send `FILE_META` (path, size, checksum), then stream chunks of 1MB, then `FILE_DONE`
4. **Parallel streams** — For large files, open additional TCP connections on incrementing ports (CONTROL_PORT + 1 through N)
5. **Progress** — Periodically emit `PROGRESS` from receiver back to sender for UI updates
6. **Resume** — Track transferred bytes; on reconnection, sender skips already-transferred bytes

**Pitfall**: Never load entire files into memory. Read and send in fixed-size chunks (~1MB).

**Pitfall**: Handle cancellation gracefully — the sender loop should check a `_cancelled` flag after every chunk.

## Step 5 — Cross-Platform Companion Apps

When building across Windows and Android:

| Aspect | Windows | Android |
|--------|---------|---------|
| GUI framework | CustomTkinter (Python) | Jetpack Compose (Kotlin) |
| Async runtime | asyncio | Kotlin coroutines |
| Discovery | python-zeroconf | NsdManager |
| Storage | JSON files in %APPDATA% | SharedPreferences |
| Background | System tray | Foreground Service + Notification |
| File access | Direct filesystem | SAF / MediaStore |

**Pitfall**: Android scoped storage (API 30+) means you can't use arbitrary file paths for user-accessible files. Use `MediaStore` for photos/video/audio and SAF `DocumentFile` for arbitrary documents.

**Pitfall**: On Android, network operations must run on a background thread (Dispatchers.IO). Use `lifecycleScope` or `MainScope` + `launch(Dispatchers.IO)` for IO.

### GUI Patterns for Device Discovery Cards

The device discovery screen is the user's first impression. Make each device card show:

**Status at a glance**:
- Online/offline badge — colored dot or text (green = online, gray = offline)
- Connection quality indicator — ⚡ excellent, ✓ good, 〜 fair, ⚠ poor, ○ offline
- Paired status — 🔗 or "Paired" badge for already-trusted devices

**Device identity**:
- Platform icon (📱 Android / 💻 Windows)
- Device name (bold, 15-16px)
- Device type + IP on a secondary line (smaller, gray)

**Actions**:
- "Pair" button (green) for unpaired online devices
- "Send →" button (blue) for paired online devices
- "Offline" label (disabled) for known but unreachable devices

**Layout** (CustomTkinter):
```python
card = ctk.CTkFrame(parent, corner_radius=10, border_width=1)
card.grid_columnconfigure(1, weight=1)

# Row 0, Col 0: Platform icon (emoji)
# Row 0, Col 1: Name + status badge (flow layout)
# Row 0, Col 2: Pair/Send button
# Row 1, Col 1: Type + IP subtitle
```

**Windows-specific (tkinter.filedialog)**:
When using `filedialog.askdirectory()` or `askopenfilenames()` with CustomTkinter, the dialog may appear behind the window. Fix with:
```python
self.lift()
self.focus_force()
self.update_idletasks()
folder = filedialog.askdirectory(parent=self, title="...", mustexist=False)
```

Also set `mustexist=False` so users can create new folders, and `initialdir` to a sensible default (current path or home directory).

**Pitfall**: Avoid cramming too much info into a single card. Three lines max: (1) icon + name + status, (2) type + IP + quality, (3) action button. More than that and the list becomes unreadable on mobile-sized windows.

## Step 6 — Building the Android APK from CLI on Windows

When Android Studio isn't available, you can build the APK entirely from the command line. This is the complete zero-to-APK sequence.

### Prerequisites

1. **Portable JDK 17+** — Download from Adoptium and extract anywhere. No Windows installer needed.
2. **Android command-line tools** — Download `commandlinetools-win-*.zip` from the Android developer site.
3. **Gradle wrapper** — Generated once with `gradle wrapper` from a system that has Gradle installed (or from a project template).

### Setup Sequence

```bash
# 1. Unpack JDK somewhere writeable
unzip OpenJDK17U-jdk_x64_windows_hotspot_*.zip -d /path/to/jdk/
export JAVA_HOME="C:\\path\\to\\jdk\\jdk-17.0.x+7"   # Windows-style path

# 2. Install Android cmdline-tools into SDK structure
mkdir -p "$ANDROID_SDK_ROOT/cmdline-tools/latest"
unzip commandlinetools-win-*.zip -d /tmp/cmdtmp
mv /tmp/cmdtmp/cmdline-tools/* "$ANDROID_SDK_ROOT/cmdline-tools/latest/"

# 3. Accept licenses and install required SDK components
yes | sdkmanager.bat --sdk_root="C:\\path\\to\\Sdk" \
  "platforms;android-34" "build-tools;34.0.0"

# 4. Create local.properties in project
echo "sdk.dir=C:/path/to/Sdk" > android/local.properties

# 5. Build
cd android
./gradlew assembleDebug --no-daemon
```

### MSYS/Git-Bash Path Quirks

The sdkmanager.bat and gradlew.bat scripts read JAVA_HOME as a Windows path. **Do not use MSYS-style paths** (`/c/Users/...`) for JAVA_HOME or sdkmanager. Use `C:\\...` or `C:/...` format.

**Curl file output**: When downloading with `curl` inside git-bash, use Windows paths for `-o`:
```bash
curl -L -o "C:\\Users\\<user>\\Downloads\\file.zip" "<url>"   # Works
curl -L -o "/c/Users/<user>/Downloads/file.zip" "<url>"       # May fail
```

### Common Gradle/Kotlin Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Android resource linking failed: resource mipmap/ic_launcher not found` | Missing launcher icon | Create mipmap-{density} dirs with PNGs or use `@android:mipmap/sym_def_app_icon` |
| `Unresolved reference: HorizontalDivider` | API change in Material3 | Use `Divider` (pre-1.2) or `HorizontalDivider` (1.2+) depending on BOM version |
| `LinearProgressIndicator(progress = { lambda })` wrong overload | API changed from `Float` to `() -> Float` lambda parameter | Pass raw `Float` for BOM < 2024.02, use `{ lambda }` for BOM >= 2024.02 |
| `Unresolved reference: dependencyResolution` | Typo in settings.gradle.kts | Use `dependencyResolutionManagement` (the full name with `Management` suffix) |
| `Val cannot be reassigned` on `job.state = x` | Data class field is `val` | Change to `var` in the data class for mutable fields |
| `sdkmanager: command not found` in bash | .bat files need explicit path | Call `sdkmanager.bat` (with extension) from git-bash |
| `JAVA_HOME is set to an invalid directory` | MSYS path format in JAVA_HOME | Use `C:\\Users\\...` format instead of `/c/Users/...` |

### Speeding Up Iteration

After the first successful build, subsequent builds are much faster because Gradle caches dependencies:
```bash
./gradlew assembleDebug --no-daemon   # Slowest: first run (downloads Gradle + deps)
./gradlew assembleDebug --no-daemon   # Fast: cached, only recompiles changed files
```

For incremental Kotlin-only changes, you can skip resource processing:
```bash
./gradlew compileDebugKotlin    # Just check Kotlin compilation (fast)
```

**Pitfall**: The Gradle wrapper (`gradlew`) downloads a `gradle-*.zip` distribution on first run if it doesn't match a cached version. This is normal but takes ~30s on first build.

**Pitfall**: If you see `Could not determine the dependencies of null` with a path error, your `local.properties` `sdk.dir` has an invalid format. Use forward slashes: `sdk.dir=C:/Users/.../Sdk`.

## Step 7 — Keeping Python and Kotlin Protocol Implementations in Sync

When maintaining two implementations of the same wire protocol:

1. **Single source of truth** for message types: maintain one file (e.g., `protocol.md` or a shared `protocol.json`) that both implementations reference during code review.
2. **Test with a loopback harness**: Before testing cross-device, test the protocol by having Python talk to Python over localhost and Kotlin talk to Kotlin over localhost.
3. **Critical fields to match exactly** between implementations:
   - Message type enum values (case-sensitive strings)
   - Payload key names (including underscores vs camelCase)
   - Chunk size constant
   - Port numbers
   - HEX encoding format (lowercase in both)
- **Pitfall**: If the Android app acts as a server, make sure the `HELLO` message exchange is symmetric — both sides send AND receive a HELLO before proceeding to the next message type.

### Pitfall: Connection Demultiplexing (One Port, Two Handlers)

When a single TCP control port handles **multiple protocol intents** (e.g., pairing handshake AND file transfer), a naive architecture of separate handler classes connecting to the same port causes a **route failure**:

| Broken pattern | What happens |
|---------------|-------------|
| PairingHandler opens its own `open_connection()` to the same port | Creates a second TCP connection |
| TransferServer._handle_incoming() accepts first connection, reads HELLO | Consumes the message PairingHandler was waiting for |
| PairingHandler.handle_incoming() expects pre-routed connection | Never gets called |

**Symptom**: Pairing stalls after the initial handshake. Server logs show "Ignored message: PAIR_INIT" or pairing times out silently.

**Fix**: Use a **single connection router** pattern:

```
TCP Server (one port)
    │ accept()
    ▼
Connection Router
    │ read HELLO → send our HELLO
    │ read 2nd message (determines intent)
    ├── PAIR_INIT  → PairingHandler(reader, writer, payload)
    ├── FILE_OFFER → TransferSession(reader, writer, payload)
    └── else       → close with error
```

Key rules:
1. **One server, one accept loop.** All connections enter through the same listener.
2. **Common handshake first.** Every connection starts with HELLO↔HELLO.
3. **Read the intent before routing.** After HELLO, read one more message to decide the handler.
4. **Pass the reader/writer pair downstream.** Handlers receive an already-connected socket — they do NOT open their own connection.
5. **Don't re-read HELLO downstream.** The router already consumed it. Pass the second message's payload to the handler as context.

This applies to any P2P app where features share a control port — pairing, file transfer, chat, remote control, etc.

## References

- `references/instant-transfer-architecture.md` — Full architecture doc from a working implementation
- `references/instant-transfer-protocol.md` — Complete wire protocol specification with message flow diagrams
- `references/android-cli-build.md` — Detailed zero-to-APK build process on bare Windows
