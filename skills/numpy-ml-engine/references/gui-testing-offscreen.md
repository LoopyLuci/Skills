# GUI Testing Without Display Server

On headless environments (no X server, CI/CD), use Qt's offscreen platform:

```python
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
app = QApplication([])

# Create and verify widgets
window = WebBuilderWindow()
assert window.windowTitle() == "WebBuilder Desktop — Professional Web Builder"
```

## What Works Offscreen

- Widget creation and layout
- Signal/slot connections
- Method calls (no visual verification)
- ML model predictions

## What Doesn't Work

- Visual layout verification
- Screenshot capture
- Actual user interaction

## QWebEngineView Fallback

```python
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    self.web_view = QWebEngineView()
except Exception:
    self.web_view = QTextBrowser()  # Fallback
```

Use `setHtml()` instead of `setUrl()` to avoid network service crashes.

## Verification Pattern

```python
def test_ml_models():
    import os
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    
    from webbuilder.ml_engine.models import MLModelFactory
    factory = MLModelFactory()
    
    palette = factory.get('color_harmony').generate('#3b82f6')
    assert 'primary' in palette
    assert 'secondary' in palette
```

## Pitfalls

1. **setUrl crashes**: Use `setHtml()` for QWebEngineView
2. **WebEngine not available**: Import inside try/except with QTextBrowser fallback
3. **exec_() blocks**: Don't call `app.exec_()` in tests
4. **$DISPLAY not set**: Always set `QT_QPA_PLATFORM=offscreen` before QApplication creation
