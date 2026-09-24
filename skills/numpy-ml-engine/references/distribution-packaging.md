# Distribution Packaging for NumPy ML Apps

## PyInstaller Hidden Imports

When packaging apps with custom ML modules, all submodules must be listed:

```python
# build.py
cmd = [
    '--hidden-import=webbuilder.ml_engine',
    '--hidden-import=webbuilder.ml_engine.models',
    '--hidden-import=webbuilder.ml_engine.data',
    '--hidden-import=webbuilder.ml_engine.persistence',
    '--hidden-import=webbuilder.gui.chat_panel',
    '--hidden-import=webbuilder.gui.form_builder_dialog',
]
```

## Import Path Fixes

All cross-package imports MUST use full paths:
- `from webbuilder.cms` → `from webbuilder.contrib.cms`
- `from webbuilder.agentic` → `from webbuilder.contrib.agentic`

## Verification Script

```python
# test_build.py
import importlib
modules = ['webbuilder', 'webbuilder.core', 'webbuilder.ml_engine', ...]
for mod in modules:
    importlib.import_module(mod)
```

## Pitfalls

1. **QWebEngineView crashes in headless**: Use `setHtml()` not `setUrl()`. Provide QTextBrowser fallback.
2. **PyQt5 imports for PyInstaller**: Wrap in try/except with stub classes.
3. **.npz weight files**: Ship separately or train on first launch — PyInstaller won't bundle them automatically.
