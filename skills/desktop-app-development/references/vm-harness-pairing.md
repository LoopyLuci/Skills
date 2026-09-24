# VM-Harness Pairing & Federation

## Mobile Pairing Flow

### Desktop Side
1. `MainWindow._init_api_server()` creates `QMCMApiServer` with signing key
2. `PairingPanel.set_server(server)` wires the API server
3. `PairingPanel._generate_pairing()` calls `server.generate_pairing_token()`
4. Token encoded as `vmharness://pair?key=<base64_payload>.<base64_sig>`
5. QR code generated via `qrcode` library, displayed in QLabel
6. URI displayed in read-only QLineEdit with Copy button

### Phone Side
1. User scans QR or pastes URI
2. `PairingTokenVerifier.verify(token)` validates Ed25519 signature
3. On success, `DesktopRepository.pair(token)` sends to desktop API
4. Desktop registers API key, phone stores it in EncryptedSharedPreferences

### Token Format
```
payload = {
    "v": 1,
    "purpose": "pair",
    "host": "100.0.0.0",  # Tailscale IP
    "ip": "100.0.0.0",
    "tailnet": "tailscale.net",
    "machine_id": "vm-harness-desktop",
    "display_name": "VM-Harness Desktop",
    "created": 1727000000,
    "expires": 1727003600,
    "secret": "<random_base64>"
}
token = base64(payload) + "." + base64(ed25519_sign(payload))
```

## Federation (Desktop-to-Desktop)

### Adding Remote Desktop
1. User enters remote desktop's pairing URI
2. `PairingPanel._add_remote_desktop()` parses and verifies token
3. Registers API key, saves to `.federation.json`
4. Remote desktop appears in Connected Desktops list

### Federation Config (.federation.json)
```json
{
    "remote-machine-id": {
        "host": "100.0.0.0",
        "display_name": "Remote Desktop",
        "api_key": "<registered_key>",
        "added_at": "2026-09-23T10:00:00"
    }
}
```

## Naming Conventions After Rename

| Component | Old | New |
|-----------|-----|-----|
| Android package | `com.omarchy.qmcmcp` | `com.vmharness` |
| Deep link scheme | `qmcmcp://` | `vmharness://` |
| Shared prefs | `qmcmcp_paired_prefs` | `vmharness_paired_prefs` |
| Signing key file | `.qmcmcp_signing_key` | `.vmharness_signing_key` |
| API server port | 8443 | 8443 (unchanged) |
| Streaming port | 8445 | 8445 (unchanged) |

## Ed25519 Key Management

- **Algorithm**: Ed25519 (not RSA, not ECDSA)
- **Storage**: Raw 32-byte private key in `.vmharness_signing_key`
- **Public key**: Derived from private key, exported as PEM for Android
- **Android**: Uses Tink `Ed25519Verify(rawKeyBytes)` — JCA unavailable on API 29
- **PEM format**: `-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEA...\n-----END PUBLIC KEY-----`

## ADB Commands for Phone Testing

```bash
# Port forwarding
adb -s N0AA002607K22200158 reverse tcp:8443 tcp:8443
adb -s N0AA002607K22200158 reverse tcp:8445 tcp:8445

# Force stop + relaunch
adb -s N0AA002607K22200158 shell am force-stop com.vmharness.android
adb -s N0AA002607K22200158 shell am start -n com.vmharness.android/.ui.MainActivity

# Deep link (fresh token)
TOKEN=$(cat /tmp/fresh_token.txt)
adb -s N0AA002607K22200158 shell am start -a android.intent.action.VIEW -d "vmharness://pair?key=$TOKEN"

# Grant camera permission
adb -s N0AA002607K22200158 shell pm grant com.vmharness.android android.permission.CAMERA
```

## Build & Install (Android)

```bash
cd C:/Projects/QEMU-MCP/android
./gradlew.bat clean
./gradlew.bat assembleDebug
adb -s N0AA002607K22200158 install -r app/build/outputs/apk/debug/app-debug.apk
```

## Common Pairing Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Invalid token" | Signing key mismatch | Regenerate token with current desktop key |
| "Server not available" | `set_server()` not called | Wire API server after `_build_panels()` |
| QR code blank | `qrcode` not installed | `pip install qrcode[pil]` |
| Phone shows pairing screen | Package renamed, data cleared | Re-pair with new deep link |
| Camera permission denied | Not granted via ADB | `adb shell pm grant com.vmharness.android android.permission.CAMERA` |
| Deep link not handled | Manifest scheme mismatch | Verify `android:scheme="vmharness"` in AndroidManifest.xml |
