# Crash Debugging & Diagnostics

## Early Crash Capture Pattern

When a PyQt5 app crashes before the GUI appears, capture crash stages to a file before any Qt initialization:

```python
_crash_stage_file = os.path.join("logs", "crashes", f"early_crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

def _crash_stage(stage, msg="OK"):
    """Write startup stage to crash log for diagnosis."""
    try:
        os.makedirs(os.path.dirname(_crash_stage_file), exist_ok=True)
        with open(_crash_stage_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] {stage}: {msg}\n")
            f.flush()
            os.fsync(f.fileno())
    except Exception:
        pass

def main():
    _crash_stage("start", "Starting WebBuilder")
    app = QApplication(sys.argv)
    _crash_stage("qt_init", "QApplication created")
    # ... each initialization step gets a stage
    window = WebBuilderWindow()
    _crash_stage("window_create", "WebBuilderWindow created")
    window.show()
    window.raise_()
    window.activateWindow()
    _crash_stage("window_show", "Window shown and activated")
```

**Why fsync:** Without `os.fsync()`, crash reports may not be written to disk before the process terminates.

## Crash Stages Interpretation

If stages stop at `crash_recovery` but `setup_ui` is missing, the crash is inside `_check_crash_recovery()`. If `setup_ui` appears but `setup_menu` is missing, the crash is in `setup_menu()`. Each stage pinpoints the exact failure location.

## QMessageBox.question() Blocks in Headless Mode

**Pitfall:** `QMessageBox.question()` blocks indefinitely waiting for user input. In headless/auto mode, the app hangs and the GUI never appears.

```python
# WRONG — blocks forever in headless mode
reply = QMessageBox.question(self, "Crash Recovery", "...", QMessageBox.Yes | QMessageBox.No)

# CORRECT — auto-recover without prompting
if crash_recovery.has_recovery():
    data = crash_recovery.get_recovery()
    if data and "project" in data:
        self.current_project = Project.from_dict(data["project"])
        crash_recovery.clear_recovery()
```

## Crash Report Files

After a crash, check these files in order:
1. `logs/crashes/early_crash_*.txt` — pre-Qt initialization crashes
2. `logs/crashes/crash_*.txt` — runtime crashes with full traceback
3. `logs/crashes/crash_*.json` — detailed JSON reports with local variables
4. `logs/console_output.txt` — captured console output

## Crash Reporter Integration

```python
from webbuilder.crash_reporter import capture_crash

# In exception handler
capture_crash(exception, {"source": "global_exception_hook", "stage": current_stage})
```

The crash reporter captures: exception type, message, full traceback, local variables, system info (OS, Python, CPU, RAM), and telemetry context.

## Window Visibility After Launch

If the app launches but the GUI is not visible:
1. Call `window.showMaximized()` after `window.show()` — ensures window is on screen
2. Call `window.raise_()` and `window.activateWindow()` — brings to foreground
3. Check for blocking dialogs during init (QMessageBox.question is the usual culprit)
4. Verify no crash stages are missing — missing stages indicate where the crash occurred