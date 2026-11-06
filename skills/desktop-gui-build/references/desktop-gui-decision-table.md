# Desktop GUI decision table

## Shell choice

| Option | Best for | Drawbacks |
|---|---|---|
| **Tauri 2** (WebView2) | Every desktop GUI job (user default). Native window, small bundle, Rust backend. | WebView2 runtime required on the host; dev-mode quirks on Windows. |
| pywebview + local backend | Quick wrappers, fallback when WebView2 is blocked. | Heavier runtime, less "native". |
| ratatui TUI (same binary) | Terminal-first products (docs/GUI-DESIGN may propose this). | Not a windowed GUI; user asked for GUI, not the default. |

Decision rule: user asked for a GUI -> Tauri 2 first. If a Tauri native launch fails (no WebView2, file locks), fall back to pywebview with the same frontend bundle, then report the blocker.

## Backend wiring

| Approach | When to use | Pitfall |
|---|---|---|
| Core in-process | Everything derived from the CLI (routing, teach/review, verify, training, eval). | Desktop shell can drift from CLI if logic duplicates; keep the verified core in-process and only thin-wrap. |
| CLI binary as child | `cli(args)` diagnostics, running the command line. | Must not be a console window (`CREATE_NO_WINDOW` on Windows); keep this the ONLY subprocess. |
| Service layer `Result<T, String>` | Testable without a Tauri app. | Don't leak Tauri types into the service; commands are thin wrappers. |
| Train progress | `train_observed` on a background thread, mpsc JSON progress, async command polls and emits events. | Cancel = global `Arc<AtomicBool>` (thread_local, reachable from `cancel_train`); worker joined, state cleared. |

## Feature brief template (9-screen desktop app)

1. **Ask** — input, decision card, trace, confirm dialog, suggestions, status line. Keyboard: Enter submit, Alt+Enter new line, Up/Down history, Ctrl+R reverse search, Ctrl+P palette.
2. **History** — item list, filter/sort, expand details, clear. Keyboard: Arrow keys navigate, Enter open, Ctrl+F filter.
3. **Review** — submitted text, critique list (approve/decline each), regenerate, teach/review round-trip.
4. **Train** — config (epochs/hidden/seed), Start with progress log + Cancel, results summary + digest + comparison with the previous model.
5. **Model** — path, digest, verify-on-start, provenance, format/version, Verify now, Retrain.
6. **Evaluate** — T1 classifier alone, full pipeline, safety suite tables + misses + export (Markdown + JSON).
7. **Tools** — catalogue from the spec (name, risk, slots, templates, broad flags) + search + Try to fill the Ask input. Generated from the spec, never hand-maintained.
8. **Settings** — category tree + search box; each field shows name/eff/default/origin/locked with a lock icon and reason; editable text/number/select/bool/path/list; protected paths add-only; export/import; theme picker (auto/dark/light/mono/high-contrast); colour + glyphs; history retention; keys preset/bindings; advanced log level/diagnostics.
9. **Help** — quickstart, concept list, key bindings, project pages, how to report.
10. **Diagnostics** — tool layout, settings schema, host info, audit log read, config show, lights. For debugging the app itself.

Key bindings (standard): Enter activate, Escape close, Ctrl+P command palette, Ctrl+R reverse search, Alt+Enter new line, Up/Down navigate lists, Ctrl+F filter, Ctrl+S save (where applicable).
