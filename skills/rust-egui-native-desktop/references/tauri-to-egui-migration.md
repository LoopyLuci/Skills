# Migrating from Tauri to Native egui/eframe

When the user rejects a Tauri-based UI (browser engine) and demands 100%
native rendering, follow this migration path.

## Detection

Signs the current app is Tauri-based:
- `diskripper-tauri/` or `src-tauri/` directory exists
- `frontend/` with React/TypeScript/Vite
- `tauri.conf.json` with `productName`, `identifier`
- CI has `tauri-apps/tauri-action` and Node.js setup
- README mentions "Tauri 2", "WebView2", "React"

## Migration Steps

### 1. Create native egui app crate

```toml
# diskripper-app/Cargo.toml
[dependencies]
eframe = { version = "0.28", features = ["default"] }
egui = "0.28"
egui_extras = "0.28"
# ... core crate and shared deps
```

Add to workspace members in root `Cargo.toml`:
```toml
[workspace]
members = ["diskripper-core", "diskripper-app"]
```

### 2. Implement the app

Follow the architecture in SKILL.md: `eframe::run_native()`, two mpsc
channels, worker threads with tokio runtime.

### 3. Remove old Tauri/web code

```bash
rm -rf diskripper-tauri/ frontend/
```

Stage deletions: `git add -A`

### 4. Update CI workflow

Remove:
- `test-frontend` job (Node.js setup, npm ci, npm run build)
- `tauri-apps/tauri-action` build step
- Node.js setup steps

Replace with:
```yaml
- name: Build native app
  run: cargo build --release --target ${{ matrix.target }} -p diskripper-app
```

### 5. Update documentation

- README: replace "React/TypeScript desktop app (Tauri 2)" with
  "100% native desktop app (egui/eframe, no browser engine)"
- Remove `frontend/`, `diskripper-tauri/` from project structure
- Replace Tauri build instructions with `cargo build --release -p diskripper-app`
- Update architecture diagram: GUI (egui) directly calls core, no Tauri layer
- Remove all Tauri/web references from docs

### 6. Verify

```bash
cargo test --workspace --tests    # all pass
cargo build --release             # compiles clean
```

## Pitfalls

- **Stale-read guard:** After reading a file with pagination, `write_file`
  blocks overwrites. `rm` the file first, then write fresh.
- **Dead code warnings:** Unused struct fields/enum variants from stub
  implementations produce warnings. Wire them up or prefix with `_`.
- **Large binary:** egui apps are ~100MB in release mode. This is normal.