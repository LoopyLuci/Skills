# Tauri 2 Config Schema

## Observed Versions

- `tauri-build` 2.6.3
- `tauri` 2.11.5

## Accepted Top-Level Keys

- `productName`
- `version`
- `identifier`
- `build`
- `bundle`
- `plugins`

## Rejected Keys in This Environment

- `package`
- `tauri`
- `allowlist`
- `trayIcon`
- `deb` (must go under `linux: { "deb": {} }`)
- `macOS` (must be lowercase `macos`)
- `publisher`, `homepage` (not recognized)
- `createUpdaterArtifacts` (only valid with updater plugin)

## Minimal Known-Good `tauri.conf.json`

```json
{
  "productName": "DiskRipper",
  "version": "0.1.0",
  "identifier": "com.diskripper.app",
  "build": {
    "beforeDevCommand": "",
    "devUrl": "http://localhost:1420",
    "frontendDist": "../frontend/dist"
  },
  "bundle": {
    "active": true,
    "targets": "all"
  },
  "app": {
    "windows": [{ "title": "DiskRipper", "width": 1200, "height": 800 }],
    "security": { "csp": null }
  }
}
```

## Full Packaging Config (All Targets)

```json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "copyright": "2026 Author",
    "category": "Utility",
    "shortDescription": "App description",
    "longDescription": "Longer description",
    "windows": {
      "certificateThumbprint": null,
      "digestAlgorithm": "sha256",
      "timestampUrl": ""
    },
    "linux": {
      "deb": {
        "depends": []
      }
    },
    "macos": {
      "frameworks": [],
      "minimumSystemVersion": "10.15",
      "exceptionDomain": "",
      "signingIdentity": "",
      "providerShortName": "",
      "entitlements": null
    }
  }
}
```

## Dev Workflow Note

When using Tauri 2 with a React/Vite frontend in a separate directory:
1. Start frontend first: `cd frontend && npm run dev`
2. Then run Tauri with empty `beforeDevCommand`: `cd src-tauri && cargo tauri dev`
3. Use `devUrl`: `http://localhost:1420` to connect to the running Vite server

This avoids path resolution issues with `cd ../frontend && npm run dev` in `beforeDevCommand`.
