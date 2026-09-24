# Modular PyQt5 Architecture Pattern

For production-grade PyQt5 apps, avoid monolithic single-file designs. Use a modular package structure.

## Recommended Layout

```
webbuilder/
  __init__.py
  core/
    __init__.py          # Config, Project, Page, Section, ProjectManager
    multi.py             # MultiPageProject, AssetManager, DeploymentManager
  gui/
    __init__.py          # Main window, chat panel, canvas, preview
  export/
    __init__.py          # HTML, React, Vue, JSON exporters
  ai/
    __init__.py          # Streaming AI client (OpenAI, Anthropic, Ollama)
  plugins/
    __init__.py          # Plugin base + built-in plugins
webbuilder_desktop.py    # Entry point (sets Qt attrs, then imports gui)
```

## Entry Point Pattern

The entry point sets Qt attributes BEFORE any gui imports:

```python
# webbuilder_desktop.py
import os
os.environ['QT_OPENGL_TYPE'] = 'software'
os.environ['QT_OPENGL'] = 'software'

from PyQt5.QtCore import QCoreApplication, Qt
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

from webbuilder.gui import main

if __name__ == "__main__":
    main()
```

## Key Architectural Decisions

1. **Dataclasses over dicts** — Use `@dataclass` for Project, Page, Section, Design. Provides type safety and clean serialization.

2. **Separate serialization** — `to_dict()` and `from_dict()` methods on each dataclass. Don't rely on `dataclasses.asdict()` — it doesn't handle nested dataclasses well.

3. **Singleton Config** — Use a class-level `INSTANCE` pattern for global config:
   ```python
   class Config:
       INSTANCE: Optional["Config"] = None
       @classmethod
       def get(cls) -> "Config":
           if cls.INSTANCE is None:
               cls.INSTANCE = cls()
           return cls.INSTANCE
   ```

4. **Avoid circular imports** — If module A imports from module B and vice versa, split into a third module or use lazy imports. The `core/__init__.py` should NOT import from `core/multi.py` at the top level; instead, import at the bottom of the file or use `from webbuilder.core.multi import ...` in the consuming module.

5. **QThread for background work** — AI streaming, file I/O, and heavy computation should happen in QThread subclasses, not asyncio loops. Use `pyqtSignal` to communicate results back to the GUI thread.

6. **QWebEngineView for live preview** — Use `setUrl(QUrl.fromLocalFile(temp_path))` to render HTML. Write to a temp file and refresh on canvas changes.

## Common Pitfalls

1. **Circular imports** — `core/__init__.py` importing `core/multi.py` which imports from `core/__init__.py`. Fix: import multi at the BOTTOM of core/__init__.py, not the top.

2. **f-string backslash in Python 3.11** — f-string expression parts cannot include backslashes. Use a variable instead:
   ```python
   # WRONG: f'{f"..." if x else ""}'
   # RIGHT: cta_html = f"..." if x else ""; f'{cta_html}'
   ```

3. **QWidget parenting** — Always set a parent widget or layout. Unparented widgets leak memory.

4. **Lambda capture in loops** — Use `lambda checked, t=cid: func(t)` to capture current value.

5. **Layout clearing** — When removing widgets from a layout, call `item.widget().deleteLater()` to avoid memory leaks.

6. **QWebEngineView temp files** — Write preview HTML to `tempfile.NamedTemporaryFile` and load via `QUrl.fromLocalFile()`. Clean up temp files on app exit.

## Streaming AI Integration Pattern

```python
class StreamThread(QThread):
    chunk_received = pyqtSignal(str)
    finished = pyqtSignal(object)

    def __init__(self, ai_client, messages, model_id, api_key):
        super().__init__()
        self.ai_client = ai_client
        self.messages = messages
        self.model_id = model_id
        self.api_key = api_key

    def run(self):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def stream():
            async for chunk in self.ai_client.stream_chat(
                self.messages, self.model_id, self.api_key
            ):
                if chunk.content:
                    self.chunk_received.emit(chunk.content)
                if chunk.done:
                    self.finished.emit(chunk.error)
                    return

        loop.run_until_complete(stream())
        loop.close()
```

## Testing Strategy

Since MCP `computer_use` clicks don't reliably reach Qt widgets:

1. **Integration tests** — Test Python logic directly (import modules, call methods, verify output)
2. **Headless GUI tests** — Use `QT_QPA_PLATFORM=offscreen` to launch the app and verify widget creation
3. **MCP capture** — Visual verification only (screenshot, element enumeration)

```python
# test_gui.py
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['QT_OPENGL'] = 'software'

from PyQt5.QtCore import Qt, QCoreApplication
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

from PyQt5.QtWidgets import QApplication
app = QApplication([''])

from webbuilder.gui import WebBuilderWindow
window = WebBuilderWindow()
print(f'Title: {window.windowTitle()}')
print(f'Tabs: {window.center_tabs.count()}')
```
