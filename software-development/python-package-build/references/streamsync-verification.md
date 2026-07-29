# StreamSync Verification Reference

Concrete example of building and verifying a cross-platform Python desktop companion app.

## Package Structure (22 Python files)

```
desktop-python/
├── pyproject.toml
├── requirements.txt
├── README.md
└── streamsync_cli/
    ├── __init__.py          # Version, logger, re-export StreamSyncConfig
    ├── __main__.py          # --gui / --tui / auto-detect → click CLI
    ├── core/
    │   ├── config.py        # StreamSyncConfig dataclass, platform paths
    │   ├── crypto.py        # AES-256-GCM encrypt/decrypt, HKDF key derivation
    │   ├── protocol.py      # JSON message protocol, 20+ convenience constructors
    │   ├── discovery.py     # mDNS via zeroconf, DeviceInfo dataclass
    │   ├── transport.py     # WebSocket async server/client, event loop thread
    │   ├── transfer.py      # FileTransferManager, chunked send/receive, SHA-256
    │   ├── streaming.py     # MediaStreamer: VLC/MPV/HTTP backends
    │   └── clipboard.py     # ClipboardSync: pyperclip polling, echo prevention
    ├── server/
    │   └── server.py        # StreamSyncDaemon — wires all components
    └── ui/
        ├── __init__.py      # detect_ui_backend(): PyQt6 > PySide6 > Textual > CLI
        ├── cli_app.py       # Click CLI: discover/send/receive/stream/clipboard/daemon
        ├── tui_app.py       # Textual TUI: devices/transfers/log panels
        ├── qt_app.py        # PyQt6/PySide6 entry, dark theme stylesheet
        ├── qt_main_window.py# Tab widget, menu bar, system tray, 2s auto-refresh
        ├── qt_devices.py    # Device table with file send dialog
        ├── qt_transfer.py   # Transfer list with progress bar, speed, ETA
        ├── qt_streaming.py  # Media file browser, method/port, start/stop
        └── qt_settings.py   # 4-tab settings dialog with JSON persistence
```

## Dependency Breakdown

| Group | Packages | When Needed |
|-------|----------|-------------|
| core | click, zeroconf, websockets, cryptography, pyperclip, rich, psutil | Always (CLI mode) |
| gui | PyQt6 (or PySide6) | GUI mode |
| tui | textual, textual-dev | TUI mode |
| streaming | python-vlc | VLC streaming |
| all | everything above | Full install |

## Bug Found: `Optional[Path]` Not Converting `str`

**File:** `streamsync_cli/core/config.py` — `load()` and `save()` both had this bug.

**Signature:**
```python
def load(cls, config_path: Optional[Path] = None) -> "StreamSyncConfig":
```

**Problem:** When the test script passed `test_path` (a `str` from `tempfile.mktemp()`), the method called `config_path.exists()` and `config_path.parent.mkdir()` — both `Path` methods that crash on `str`.

**Fix applied to both methods:**
```python
if isinstance(config_path, str):
    config_path = Path(config_path)
```

**Lesson:** `Optional[Path]` in a type annotation is not enforced at runtime. Callers can pass `str`, `Path`, or `None`. Convert `str` to `Path` at function entry in both `load()` and `save()`.

## Verification Pipeline Used

1. `python -m py_compile` on each `.py` file (22 files)
2. `ast.parse()` whole-tree validation
3. Module import test (stdlib-only first, then external-dependency modules)
4. CLI --help on every subcommand
5. `pip install -e .` + `streamsync --help` (installed entry point)
6. Ad-hoc behavioral script testing:

| Test | What It Verified |
|------|-----------------|
| Config save/load roundtrip | JSON persistence, `str`→`Path` conversion |
| Encrypt/decrypt roundtrip | AES-256-GCM correctness |
| HKDF key derivation | Same password+salt → same key |
| Protocol serialization | 14 message types roundtrip cleanly |
| File transfer lifecycle | Init→chunk→complete, SHA-256 hash |
| Receive simulation | chunk reassembly, .part rename, progress calc |
| Stream lifecycle | HTTP server start/stop, FileNotFoundError |
| Clipboard sync | enable/disable toggle, get_current_content |

## CLI Commands Verified

```
streamsync --help              → 6 commands listed
streamsync discover --help     → --timeout, --json flags
streamsync send --help         → FILE_PATH, DEVICE_ID args
streamsync receive --help      → OUTPUT_DIR arg, --port, --timeout
streamsync stream --help       → --method (vlc/mpv/http/auto), --port
streamsync clipboard --help    → --port flag
streamsync daemon --help       → --port, --daemon/--no-daemon
```
