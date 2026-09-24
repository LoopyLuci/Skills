# Headless GUI Testing for PyQt5 Apps

## Environment Setup

```python
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # BEFORE any PyQt imports
os.environ['QT_OPENGL'] = 'software'  # Software rendering for headless

# CRITICAL: Set attribute via QCoreApplication BEFORE QtWidgets import
from PyQt5.QtCore import Qt, QCoreApplication
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

from PyQt5.QtWidgets import QApplication
app = QApplication([''])
```

**Why `Qt.AA_ShareOpenGLContexts = True` AFTER `from PyQt5.QtCore import Qt` doesn't work:**
The static attribute assignment is too late — `from PyQt5.QtCore import Qt` itself may trigger module initialization. Use `QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)` after importing `QCoreApplication` but BEFORE importing `QtWidgets`.

## Test Script Pattern (`test_gui.py`)

```python
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtCore import Qt
Qt.AA_ShareOpenGLContexts = True

from PyQt5.QtWidgets import QApplication
app = QApplication([''])

from desktop_app import WebBuilderApp

window = WebBuilderApp()

# ---- Verification ----
print(f'Title: {window.windowTitle()}')
print(f'Min size: {window.minimumSize().width()}x{window.minimumSize().height()}')
print(f'Current: {window.size().width()}x{window.size().height()}')

tabs = window.tabs
print(f'Tabs: {tabs.count()}')
for i in range(tabs.count()):
    tab = tabs.widget(i)
    print(f'  Tab {i} ("{tabs.tabText(i)}"): {type(tab).__name__}')

# Check specific attributes based on app
print(f'Canvas frame: {window.canvas_frame.size() if hasattr(window, "canvas_frame") else "N/A"}')
print(f'Preview frame: {type(window.preview_frame).__name__ if hasattr(window, "preview_frame") else "N/A"}')

print('=== VERIFICATION COMPLETE ===')
```

## What to Verify

| Check | Expected |
|-------|----------|
| Window title | App name |
| Min size | Set minimum (e.g. 1400x800) |
| Tab count | Number of tabs in QTabWidget |
| Tab labels | Correct names for each tab |
| Canvas frame | QFrame with sections rendered |
| Preview frame | QWebEngineView (or placeholder) |
| Settings dialog | Opens via Ctrl+, or toolbar |

## Limitations

- Offscreen mode may not render WebGL/QWebEngine content correctly
- Use `capture_after=True` on computer_use for visual verification of actual rendering
- Some styling may differ between offscreen and real display
