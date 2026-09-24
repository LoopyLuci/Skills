# QtWebEngineWidgets OpenGL Context Fix

## Problem
When importing `QWebEngineView` in a PyQt5 application, you get:
```
ImportError: QtWebEngineWidgets must be imported or Qt.AA_ShareOpenGLContexts must be set before a QCoreApplication instance is created
```

## Root Cause
`QWebEngineView` requires OpenGL context sharing to be enabled. PyQt5's `QCoreApplication` (created implicitly when `QtWidgets` is imported) must have this enabled BEFORE it's instantiated.

## Correct Import Order
```python
import sys
import os

# CRITICAL: Set attribute via QCoreApplication BEFORE QtWidgets import
# QtWidgets import creates QCoreApplication, so the attribute must be set first
from PyQt5.QtCore import Qt, QCoreApplication
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Now safe to import Qt modules
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView  # module-level
```

**Why `Qt.AA_ShareOpenGLContexts = True` AFTER `from PyQt5.QtCore import Qt` doesn't work:**
The static attribute assignment is too late — `from PyQt5.QtCore import Qt` itself may trigger module initialization. Use `QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)` after importing `QCoreApplication` but BEFORE importing `QtWidgets`.

## What FAILS

| Approach | Result |
|----------|--------|
| Flag after `QtWidgets` import | Too late — already failed |
| Lazy `QWebEngineView` in method | RuntimeError at call time |
| Flag after other PyQt imports | Too late |
| No flag at all | ImportError |

## Offscreen / Headless Testing

```python
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # BEFORE PyQt imports

from PyQt5.QtCore import Qt
Qt.AA_ShareOpenGLContexts = True

from PyQt5.QtWidgets import QApplication
app = QApplication([''])
```

## Verification

```python
# 1. Check flag is set
from PyQt5.QtCore import Qt
print(f"AA_ShareOpenGLContexts: {Qt.AA_ShareOpenGLContexts}")  # Should be True

# 2. Test window creation
from desktop_app import WebBuilderApp
from PyQt5.QtWidgets import QApplication
app = QApplication([''])
window = WebBuilderApp()
print(f"Window: {window.windowTitle()}")
print(f"Tabs: {window.tabs.count()}")
```
