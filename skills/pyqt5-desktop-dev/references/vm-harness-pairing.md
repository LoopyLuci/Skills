# VM-Harness Pairing Panel

For the VM-Harness desktop app's PairingPanel implementation.

## Panel Structure

```python
class PairingPanel(QWidget):
    def __init__(self, parent=None):
        self._server = None
        self._pairing_timer = QTimer()
        self._pairing_timer.timeout.connect(self._refresh_keys)
        # ... tab setup ...

    def set_server(self, server: QMCMApiServer):
        """Wire API server for token generation. MUST be called after init."""
        self._server = server
        self._generate_pairing()  # Generate QR + URI
        self._refresh_keys()      # List paired devices

    def _generate_pairing(self):
        token, payload, info = self._server.generate_pairing_token()
        uri = f"vmharness://pair?key={token}"
        # Generate QR code with qrcode library
        # Display in QLabel

    def _refresh_keys(self):
        keys = self._server.list_api_keys()
        # Display in device list

    def _revoke_key(self, key_id: str):
        self._server.revoke_key(key_id)

    def _add_remote_desktop(self):
        # Parse vmharness://pair?key=... URI
        # Verify token, register pairing
        # Save to .federation.json
```

## API Server Initialization

```python
def _init_api_server(self):
    """Initialize QMCMApiServer for pairing. Call AFTER _build_panels()."""
    from pathlib import Path
    from vm_mcp.api_server import QMCMApiServer, _load_or_generate_signing_key
    key_dir = Path(".")  # Signing key at project root
    signing_key = _load_or_generate_signing_key(key_dir)
    self._api_server = QMCMApiServer(
        host="0.0.0.0",
        port=8443,
        tailscale_only=False,
        signing_key_dir=key_dir,
    )
    # Wire to pairing panel
    if "pairing" in self.panels:
        self.panels["pairing"].set_server(self._api_server)
```

## Signing Key
- **File**: `.vmharness_signing_key` (32 raw Ed25519 bytes) at project root
- **Constant**: `_SIGNING_KEY_FILE = ".vmharness_signing_key"` in `vm_mcp/api_server.py`
- **Load**: `_load_or_generate_signing_key(key_dir)` — reads raw bytes, generates if missing

## Pitfalls

1. **QMCMApiServer constructor is keyword-only** — `QMCMApiServer(host=..., port=..., tailscale_only=..., signing_key_dir=...)`. Passing `signing_key=` raises `TypeError`.

2. **PairingPanel.set_server() must be called** — Without it, `_generate_pairing()` fails with "Server not available". Always call after `_build_panels()`.

3. **Signing key filename must match constant** — If you rename the key file, update `_SIGNING_KEY_FILE` in `vm_mcp/api_server.py` or `_load_or_generate_signing_key()` will generate a new key, breaking existing pairings.

4. **Panel wiring order** — Create ALL panels first, THEN wire bridges. Panels may reference bridges in their `__init__` if bridge is None.

5. **Stale mutex after forced kill** — When a process is killed via `taskkill /F`, Windows named mutexes persist. The second launch detects the mutex exists, then must also check for an actual window (`_find_vmharness_window()`). If no window exists, the mutex is stale — proceed with a new launch rather than exiting.

6. **System tray robustness** — Create tray icon programmatically via `QPainter` → `QPixmap` → `QIcon` (no file dependency). Wire both `activated` (double-click) and `messageClicked` signals to restore. Provide a `_quit_from_tray()` that hides the icon and calls `QApplication.quit()`.

7. **closeEvent minimize-to-tray** — Use `event.ignore()` + `self.hide()` + `tray_icon.showMessage()`. Do NOT call `event.accept()` or the app terminates. The `_cleanup()` method should release the single-instance mutex handle.
