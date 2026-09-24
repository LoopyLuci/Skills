# Qt Import Ordering and Headless GUI Testing

## Qt.AA_ShareOpenGLContexts Import Ordering Pitfall

### The Problem

When building PyQt5 desktop apps with `QWebEngineView`, the following pattern **fails**:

```python
from PyQt5.QtCore import Qt
Qt.AA_ShareOpenGLContexts = True          # TOO LATE — QCoreApplication already created

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
```

**Error:** `QtWebEngineWidgets must be imported or Qt.AA_ShareOpenGLContexts must be set before a QCoreApplication instance is created`

**Root Cause:** `from PyQt5.QtCore import Qt` itself triggers `QCoreApplication` creation. Setting `Qt.AA_ShareOpenGLContexts = True` after that import is too late.

### The Fix

**Option 1: Environment variable (preferred for headless/offscreen testing)**
```python
import os
os.environ['QT_OPENGL_TYPE'] = 'software'
os.environ['QT_OPENGL'] = 'software'

# Prevents QtWebEngineWidgets import error in headless/offscreen testing
os.environ['PYQT5_ALLOW_HEADLESS'] = '1'

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
```

**Option 2: Lazy import** — remove `QWebEngineView` from top-level imports entirely and import it inside the method that creates the preview widget:
```python
def _create_preview_tab(self):
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    self.preview_frame = QWebEngineView()
```

**Option 3: qputenv before imports** — set `os.environ['QT_OPENGL']` before the PyQt import line:
```python
import os
os.environ['QT_OPENGL'] = 'software'  # must be set BEFORE any PyQt import

from PyQt5.QtWidgets import *
```

### Verification

Test with offscreen platform to confirm no crashes:
```python
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from desktop_app import WebBuilderApp
window = WebBuilderApp()
print(f'Tabs: {window.tabs.count()}')  # Should not crash
```

## Headless GUI Testing Pattern

### Purpose

Verify PyQt5 GUI structure without a display server (CI, remote SSH, WSL, headless servers).

### Setup

```python
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Must set before importing PyQt5 or desktop_app
from PyQt5.QtWidgets import QApplication

app = QApplication([])  # Empty args — no sys.argv needed for offscreen

from desktop_app import WebBuilderApp
window = WebBuilderApp()

# Inspect widget tree programmatically
print(f'Tabs: {window.tabs.count()}')
for i in range(window.tabs.count()):
    tab = window.tabs.widget(i)
    print(f'  Tab {i}: {window.tabs.tabText(i)} -> {type(tab).__name__}')
    # Query child widgets, geometry, etc.
```

### Common Inspection Targets

| Target | Pattern |
|--------|---------|
| Tab count | `window.tabs.count()` |
| Tab widget type | `type(window.tabs.widget(i)).__name__` |
| Window size | `window.size().width(), window.size().height()` |
| Menu items | `window.menuBar().count()` menus, iterate each menu |
| Settings button | Check toolbar for `QToolButton` with `toolTip() == 'Settings'` |
| Canvas geometry | `window.canvas_frame.geometry()` |
| Section widgets | Count children of canvas layout |
| Property panel | Look for `QTabWidget` with `objectName() == 'properties_tabs'` |

### Why This Matters

- Catches missing methods (`Method 'to_html' not found`) before running the full app
- Verifies UI structure without needing screenshots
- Works in CI/CD pipelines and remote environments without X11/Wayland
- Faster iteration than launching full GUI and using MCP computer_use captures

### Caveats

- `QWebEngineView` may still fail in offscreen mode even with the Qt fix — use lazy import
- Geome tries may differ slightly from running GUI (no DPI scaling, etc.)
- Stylesheets still apply but visual fidelity requires actual display

## QtWebEngineWidgets Module Loading

### Issue

`PyQt5.QtWebEngineWidgets` is a separate extension module that:
- Requires OpenGL context sharing (the `AA_ShareOpenGLContexts` flag)
- Can block headless/offscreen testing
- Must be imported AFTER `QCoreApplication` is set up correctly

### Solution: Lazy Import in Preview Creation

```python
# In _create_preview_tab():
def _create_preview_tab(self):
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    self.preview_frame = QWebEngineView()
    self.preview_frame.setFixedSize(800, 500)
    # ... rest of tab setup
```

This deferred import:
- Avoids the import-time OpenGL context check
- Allows headless/offscreen testing of the rest of the app
- Only loads QtWebEngineWidgets when the preview tab is actually created

### Alternative: Disable Preview in Tests

For headless tests that don't need the preview:
```python
# In test setup:
window.preview_tab = None  # Skip creation
# Or mock:
from unittest.mock import MagicMock
window.preview_frame = MagicMock()
```

## PyQt5 Process Management (Windows)

### Problem: Multiple Stale Python Processes

After running desktop apps, multiple `python.exe` processes may linger:
```bash
tasklist | grep python
# May show 5-10 python.exe processes with varying memory
```

### Cleanup

```bash
# Kill all python.exe processes (aggressive)
taskkill /F /IM python.exe

# Or kill by PID:
taskkill /F /PID <pid>
```

### Verification After Restart

```bash
# Kill all, then start fresh
taskkill /F /IM python.exe
sleep 2
python desktop_app.py &
sleep 3
tasklist | grep python  # Should show exactly one new python.exe
```

## MCP Computer-Use Capture Limitations

### Qt App Window Detection

When using `computer_use` MCP tool to capture PyQt5 app windows:

```python
computer_use(action='capture', app='WebBuilder', mode='vision')
```

**Known issue:** On Windows, Qt apps may not register under a recognizable app name. The capture may return `app=''` with `window_title='<no on-screen window matched app=...>'`.

### Workaround

Use `list_apps` to find the actual app name, or capture the whole screen:
```python
# List available apps
computer_use(action='list_apps')

# Then capture by the discovered name, or use app='screen' for full desktop
computer_use(action='capture', app='screen', mode='vision')
```

### Why Qt Apps May Be Hard to Detect

- Qt apps on Windows use window class names like `Qt5QWindowIcon` or generic titles
- The `app` parameter in `computer_use` matches against process names or bundle IDs
- Python (Qt) apps often show as `python.exe` rather than a named app

## Summary: Checklist for PyQt5 GUI Development

- [ ] Set `os.environ['QT_OPENGL'] = 'software'` BEFORE any PyQt import
- [ ] Use lazy `QWebEngineView` import in preview tab creation
- [ ] Test with `QT_QPA_PLATFORM=offscreen` for CI/headless
- [ ] Clean up stale python.exe processes between runs
- [ ] Verify GUI structure programmatically, not just visually
- [ ] Check that `_create_<tab>` methods exist for all referenced tabs
- [ ] Ensure slot methods (for `addAction`) are real methods, not `None`
