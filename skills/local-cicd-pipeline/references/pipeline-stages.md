# Pipeline Stages Reference

## Stage Configuration

Each stage is a function that takes a context dict and returns `(bool, str)` — passed/failed and a message.

### preflight
- Python version check (minimum 3.10)
- venv detection and validation
- `pip check` for dependency consistency
- Git state (branch, commit)
- Disk space (minimum 2 GB free)
- Optional tools: QEMU, JDK

### static
- `compileall` on src/, gui/, tests/, ci/
- Ruff with `--select E9,F63,F7,F82,B006,B008` (bugs, not hygiene)
- Bare `except:` detection
- Secret pattern scanning (API keys, tokens, private keys)
- Big file detection (>5 MB) — **scan working tree only, not historical range**

### tests
- pytest with `-n auto` (xdist) when available
- `--timeout 600` per test
- JUnit XML output
- Flaky rerun: failed tests re-run once on their own
- QT_QPA_PLATFORM=offscreen for headless GUI tests

### smoke
- Start real hub in throwaway VMH_HOME on free port
- Verify /v1/health returns 200
- Verify /v1/operations returns 100+ operations
- Verify MCP over HTTP (initialize, tools/list)
- Verify MCP over stdio
- Clean shutdown via /v1/service/stop

### android
- Requires JDK 17+ and Android SDK
- Runs `gradlew testDebugUnitTest assembleDebug`
- **Parse Gradle errors properly**: look for `FAILURE:` and `What went wrong:` blocks, NOT `tail(out)`

### build
- PyInstaller executable build
- Requires PyInstaller in venv

### deploy
- Restart running hub from this checkout
- Only if hub is already running

## Change Detection

The pipeline uses git diff to determine which stages to run:
- `CODE` paths: src/, gui/, tests/, pyproject.toml, requirements, conftest.py, setup, ci/
- `ANDROID` paths: android/
- `BUILD` paths: src/, gui/, scripts/build_pyinstaller.py, pyproject.toml, requirements
- `DEPLOY` paths: src/, gui/, pyproject.toml, requirements

If change detection fails (no upstream, no merge base), run everything.

## Lock Mechanism

A lock file (`ci/.pipeline.lock`) contains the PID of the running pipeline. If the PID is alive, another run is refused. If the PID is dead (stale lock), it's taken over.

## Reports

Each run produces:
- `ci/logs/<timestamp>.log` — full console output
- `ci/reports/<timestamp>.json` — structured JSON report
- `ci/reports/latest.json` — symlink to latest report
- `ci/reports/history.jsonl` — one line per run with stage durations

Old logs and reports are pruned to keep the last 50.
