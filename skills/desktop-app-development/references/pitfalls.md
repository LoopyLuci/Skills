# Desktop App Development Pitfalls

## PyQt5 Pitfalls

1. **QPushButton has no `setDragEnabled`**. Use mousePressEvent/mouseMoveEvent for drag-and-drop on buttons.
2. **PyQt5 stream timeouts**: Large `write_file` calls (>40KB) can timeout. Break into smaller files or use multiple `patch` calls.
3. **SQLAlchemy model re-registration**: Define models outside `create_app()` to avoid "Table already defined" errors when reloading.
4. **Python path issues on Windows**: Use raw strings (`r'C:\\path'`) or forward slashes. `sys.path.insert(0, 'packages/core/src')` works but `packages.core.src` does not.
5. **Background process management**: Use `terminal(background=true)` with `notify_on_complete=true` for bounded tasks.
6. **Lambda capture in loops**: Use `lambda checked, t=cid: func(t)` to capture current value.
7. **Memory leaks**: Call `child.deleteLater()` before clearing layouts.
8. **Stale state**: Always call `render_canvas()` and `render_properties()` after state changes.
9. **QWebEngineView in headless environments**: `QWebEngineView` crashes without a display server. Use `QT_QPA_PLATFORM=offscreen` env var or fall back to `QTextBrowser`. Import `QWebEngineView` lazily inside the preview widget constructor with try/except.
10. **Stale `__pycache__`**: Clear `__pycache__` directories when imports fail unexpectedly: `find . -type d -name "__pycache__" -exec rm -rf {} +`.
11. **Widget factory style mapping**: When mapping declarative styles to Qt stylesheets, check attribute names match exactly (e.g., `border_color` not `border`).

## Flask Integration Pitfalls

1. **Port conflicts**: Check if port 5000 is already in use before starting Flask.
2. **Process cleanup**: Ensure Flask process is terminated on app exit.
3. **CORS**: Configure CORS properly for cross-origin requests.

## Export System Pitfalls

1. **Path handling**: Use `Path` from pathlib for cross-platform compatibility.
2. **File encoding**: Always specify `encoding='utf-8'` when writing files.
3. **Directory creation**: Call `Path.mkdir(parents=True, exist_ok=True)` before writing.

### 12. Widget Update Methods Called Before Widgets Exist

**Error:** `AttributeError: 'X' object has no attribute 'snap_btn'` (or similar)

**Cause:** `_update_snap_button()` or similar widget-update methods are called during `setup_ui()`, but the widgets they reference (buttons, labels) are created later in the same method. The update runs before the widgets exist.

**Fix:** Separate state initialization from widget updates:
```python
def __init__(self):
    self._is_snapped = False  # State BEFORE setup_ui
    self.setup_ui()            # Creates widgets
    self._update_snap_button()  # Update AFTER widgets exist

def setup_ui(self):
    # Create widgets first
    self.snap_btn = QPushButton("Snap")
    # DON'T call _update_snap_button() here
```

**Prevention:** When adding widget-update methods, check the initialization order. State variables go before `setup_ui()`, widget-update calls go after.

### 13. Python Logging Handler Added During Widget Init Causes Segfault

**Error:** Segmentation fault during `QApplication` widget initialization.

**Cause:** Adding a logging handler that references Qt widgets during `__init__` can trigger log emits before widgets are fully constructed, causing a crash in Qt's event loop.

**Fix:** Defer logging handler setup with `QTimer.singleShot`:
```python
def __init__(self):
    # Create widgets first
    self.terminal_cli = TerminalCLI()
    self.activity_tab = ActivityTab()
    # ... other init ...
    # Defer logging handler to avoid segfault
    QTimer.singleShot(100, self._setup_logging_handler)

def _setup_logging_handler(self):
    handler = _TerminalActivityHandler(self.terminal_cli, self.activity_tab)
    logging.getLogger("webbuilder").addHandler(handler)
```

**Prevention:** Never add logging handlers that reference Qt widgets during `__init__`. Always defer with `QTimer.singleShot`.
