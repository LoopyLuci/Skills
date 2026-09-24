# QT_QPA_PLATFORM=offscreen Segfault on Windows

## Problem

Running a PyQt5 GUI application in **full GUI mode** (not `--headless`) with `QT_QPA_PLATFORM=offscreen` causes a **segmentation fault (SIGSEGV, signal 11)** during `app.exec_()` teardown on some Windows hosts.

## Symptoms

- Application runs successfully — windows open, signals fire, logic works
- Crash occurs at `app.exec_()` return/teardown, not during normal operation
- Exit code 139 (SIGSEGV) or silent termination
- No Python traceback (C-level crash, Python exception hook does not fire)
- `start "" dist/QEMU-MCP.exe` launches and immediately exits with no visible window

## Cause

Qt's offscreen platform plugin on Windows has a teardown bug in some Qt/PyQt5 version combinations. The event loop runs fine, but cleanup of the OpenGL context / platform integration during `exec_()` return triggers a C-level segfault. This is a **Qt/PyQt5 platform limitation**, not a code bug.

## Workaround: Headless Mode

Use the `--headless` CLI flag which exits via `QTimer.singleShot(2000, app.quit)` before the segfault trigger:

```python
# In __main__.py
def headless_main():
    app = QApplication.instance() or QApplication(sys.argv)
    apply_global_theme(app)
    window = MainWindow()
    window.show()
    QTimer.singleShot(2000, app.quit)  # Exit before segfault
    sys.exit(app.exec_())
```

The 2-second timer gives the GUI time to initialize and render, then quits cleanly.

## Verification

```python
import os, sys, subprocess

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
sys.argv = ['app', '--headless']

# Run in subprocess to catch segfault
result = subprocess.run(
    [sys.executable, 'gui/__main__.py', '--headless'],
    capture_output=True, text=True, timeout=5
)
print('RC:', result.returncode)  # 0 = success, 139 = segfault
print(result.stdout)
```

RC 0 = headless mode works. RC 139 = segfault (full GUI mode with offscreen).

## What NOT to Do

- **Do not run full GUI mode with offscreen on a headless server** — it will segfault
- **Do not set QT_QPA_PLATFORM=offscreen for a visible GUI** — use 'windows' instead
- **Do not expect the segfault to produce a Python traceback** — it's a C-level crash

## When Full GUI Mode Is Required

Full GUI mode with offscreen platform is needed only for automated GUI testing (e.g., screenshot comparison, widget interaction tests). On Windows hosts where the segfault occurs:

1. Use `QT_QPA_PLATFORM=windows` with a virtual display driver (e.g., TurboVNC, Xephyr on WSL2)
2. Or restructure tests to use headless mode for initialization + a brief full-GUI window for the specific interaction being tested
3. Or accept that full GUI automated testing requires a visible display

## Related

- [WebBuilder Desktop App Skill](https://hermes-agent.nousresearch.com/skills/software-development/webbuilder-desktop-app) — pitfall #13
- `references/crash-reporting.md` — crash report mechanics (segfault bypasses Python hook)
