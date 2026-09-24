# Crash Reporting & Logging — Reference

## Crash Handler Pattern

The exception hook must write crash reports to files — never show a dialog.
Dialogs with dark text on dark backgrounds are invisible on the user's machine.

```python
def setup_exception_handler(app: QApplication) -> None:
    def exc_hook(exctype, value, tb):
        error_msg = ''.join(traceback.format_exception(exctype, value, tb))
        logger.error(f"Uncaught exception:\n{error_msg}")
        
        # Write to file — the only reliable output channel
        crash_dir = "logs/crashes"
        os.makedirs(crash_dir, exist_ok=True)
        crash_file = os.path.join(crash_dir, f"crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(crash_file, 'w', encoding='utf-8') as f:
            f.write(f"WebBuilder Crash Report\n")
            f.write(f"Time: {datetime.now().isoformat()}\n")
            f.write(f"Exception: {exctype.__name__}\n")
            f.write(f"Message: {value}\n\n")
            f.write(f"Traceback:\n{error_msg}\n")
        
        sys._excepthook(exctype, value, tb)
    
    sys._excepthook = sys.excepthook
    sys.excepthook = exc_hook
```

## Early Crash Capture

Crashes before QApplication init bypass the exception hook. Capture early:

```python
def main():
    crash_file = os.path.join("logs", "crashes", f"early_crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    os.makedirs(os.path.dirname(crash_file), exist_ok=True)
    
    def _write_crash(label, msg):
        with open(crash_file, 'w', encoding='utf-8') as f:
            f.write(f"Stage: {label}\nError: {msg}\n")
            f.write(f"Python: {sys.version}\nPlatform: {sys.platform}\n")
    
    try:
        app = QApplication(sys.argv)
        # ... rest of init
    except Exception as e:
        _write_crash("main()", f"{type(e).__name__}: {e}")
        raise
```

## Crash Report Contents

| Field | Source |
|-------|--------|
| Exception type | `type(e).__name__` |
| Exception message | `str(e)` |
| Traceback | `traceback.format_exc()` |
| Local variables | `frame.f_locals` at each stack level |
| Python version | `sys.version` |
| Platform | `sys.platform`, `platform.machine()` |
| RAM | `psutil.virtual_memory()` |
| Telemetry context | Session ID, event count, user actions |
| Crash stage | `_crash_stage()` — 38 stages tracked from start to complete |

## Crash Stage Instrumentation

Every startup phase is tracked via `_crash_stage()` in the main window. If a crash occurs, the last recorded stage identifies exactly where failure happened. 42 stages: start → qt_init → exception_hook → stability_monitor → autosave_manager → retry_manager → circuit_breaker → resource_guard → state_manager → error_boundary → memory_guard → thread_safety → lazy_loader → cache_manager → async_executor → batch_processor → memory_pool → debouncer → throttler → parallel_executor → performance_profiler → connection_pool → lazy_init → resource_pool → compression_manager → incremental_updater → logging → theme → project_manager → export_manager → scaling_init → autosave → memory_monitor → crash_recovery → setup_ui → setup_menu → new_project → autosave_timer → state_manager → complete → window_create → window_show

## Telemetry Integration

Crash reports include telemetry context (session ID, event count, user actions) for post-mortem analysis. The telemetry module captures usage analytics and session stats alongside crash data.

## Log Files Layout

```
logs/
├── crashes/
│   ├── early_crash_*.txt      ← pre-Qt-init crashes
│   └── crash_*.txt            ← uncaught exception crashes
├── app.log                    ← structured JSON log
├── app_rotating.log           ← rotated log (10MB, 5 backups)
├── console_output.txt         ← captured console output
└── telemetry/                 ← telemetry events
```

## Verification

```bash
# Test crash reporter
python -c "from webbuilder.crash_reporter import capture_crash; \
    capture_crash(RuntimeError('test'), {'source': 'verify'})"

# Verify crash files exist
ls -la logs/crashes/

# Run exe and check output (all 42 stages visible)
grep "stage" logs/crashes/early_crash_*.txt 2>/dev/null | tail -42
```

## Pitfalls

1. **Invisible error dialogs**: QMessageBox with dark text on dark background cannot be read. Always write to files, not dialogs.
2. **Crashes before Qt init**: The exception hook only catches Python exceptions after QApplication exists. Pre-Qt crashes need early capture in `main()`.
3. **PyInstaller hides stderr**: With `--windowed`, console output is suppressed. Crash reports must be written to files.
4. **Crash report not generated**: If the crash is a segfault or C-level error, Python's exception hook won't fire. The early capture file is the only evidence.
