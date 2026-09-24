# Tauri 2 Config Pitfalls

Session-proven config field mappings and feature flags for Tauri 2.

## Config Field Evolution

Tauri 2 CLI versions change field names without warning. Using old names causes `unknown field` errors.

| Field | Old (broken) | Current (working) |
|-------|-------------|-------------------|
| Dev server | `devPath` | `devUrl` |
| Frontend dist | `distDir` | `frontendDist` |
| Tray icon | `trayIcon` (always on) | Requires `tray-icon` feature flag |
| Updater pubkey | Placeholder `dW50cnVzdGVk...` | Generate real key with `cargo tauri signer generate` |
| beforeBuildCommand | Simple string | Must include `cd` and full build pipeline |

## Minimal Working Config

```json
{
  "build": {
    "beforeBuildCommand": "cd ../frontend && npm ci && npm run build",
    "devUrl": "http://localhost:1420",
    "frontendDist": "../frontend/dist"
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

## Feature Flags

```toml
[dependencies]
tauri = { version = "2", features = ["devtools", "tray-icon"] }
```

## Common Errors

- `unknown field 'devPath'`: Use `devUrl` instead
- `unknown field 'distDir'`: Use `frontendDist` instead
- `tray-icon` not working: Add `"tray-icon"` to features array
- Updater fails with placeholder pubkey: Generate real key with `cargo tauri signer generate`
