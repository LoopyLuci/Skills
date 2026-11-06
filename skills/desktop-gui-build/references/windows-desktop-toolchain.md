# Windows desktop toolchain (this host)

## Toolchain facts

- `cargo`/`rustc` live on `X:` (`X:\Dev\cargo\bin`); `cargo-tauri` (tauri-cli 2.11.4) is there too. Use the full path `X:\Dev\cargo\bin\cargo.exe tauri ...` or rely on the bash env, never `cargo` from an unqualified `cmd /c` (cmd does not see it).
- The terminal tool runs commands through **bash (git-bash/MSYS)** on this host, not PowerShell/cmd. MSYS paths like `/c/Users/...` work; native Windows tools need `C:/Users/x`-style forward-slash paths (they are NOT translated).
- npm is `npm.CMD` (a batch file) — Python `subprocess.run` cannot exec it directly; use `cmd /c npm ...`.
- Node 26, npm 11, pnpm, Python 3.14, git all present. Network access to `registry.npmjs.org` works, so `npm install` is the dependency source of truth.

## Dev flow

1. Backend: `cargo check` + `cargo fmt --check` + `cargo clippy`, then `cargo test` (unit + integration test).
2. Frontend: `npm install` (project-local), `npm run build` (`tsc && vite build`) — no type errors in the console output.
3. Desktop: `cargo tauri build` (or `cargo tauri dev` in dev) ends with a built binary and the frontend assets embedded.
4. End-to-end smoke test with the real project (see desktop-gui-build SKILL.md section 7).

## Native launch recovery recipes

- **Stale `app.exe` lock**: kill it with `taskkill /F /IM <app>.exe` before rebuilding; if the lock persists, temporarily rename the binary in `Cargo.toml` to break the lock, rebuild, restore the name.
- **Exit 124 from a non-tty shell**: prefer the manual dev flow (build the frontend, start `cargo tauri dev` or run the binary manually and open the Vite dev server URL) over blind retries.
- **WebView2 missing (`0x800700AA`)**: confirm WebView2 runtime is installed on the host; on a dev machine this is usually a stale binary. Kill `app.exe`, remove `src-tauri/target`, rebuild.
- **`base: './'` requirement**: in a Tauri desktop app the frontend is served as `file://` assets under `base: './'` — Vite must output `./assets/...` references, not absolute `/assets/...`, or JS/CSS never load in the native window.
- **Embedded binary path**: the desktop app references the embedded CLI binary via the `NLP_CLI_BIN` env var pointer; the `build.rs` copies the release binary to `src-tauri/bin/nlp-cli.exe` and emits the env var at compile time.
