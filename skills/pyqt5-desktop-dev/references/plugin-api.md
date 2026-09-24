# Plugin API Architecture

## When to Use

Use when building a plugin system for a PyQt5 desktop app that allows third-party extensions to add panels, dialogs, and bridges without modifying the core codebase.

## Architecture

```
plugin.py              — VMHarnessPlugin base class, PluginContext, PluginMetadata
plugin_manager.py      — PluginManager: discover, load, unload plugins
plugins/                — Plugin directory (example_panel.py)
```

## Base Class

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class PluginMetadata:
    name: str
    version: str
    description: str
    author: str = ""
    plugin_type: str = "panel"  # "panel", "dialog", "bridge"
    dependencies: List[str] = field(default_factory=list)

class PluginContext:
    def __init__(self):
        self.settings: Dict[str, Any] = {}
        self.event_loop: Optional[asyncio.AbstractEventLoop] = None
        self.bridge_registry: Any = None
        self.api_app: Any = None

class VMHarnessPlugin(ABC):
    @abstractmethod
    async def initialize(self, context: PluginContext) -> bool:
        """Initialize the plugin. Return True on success."""
        ...
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Clean up resources."""
        ...
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        ...

class PanelPlugin(VMHarnessPlugin):
    @abstractmethod
    def create_panel(self) -> QWidget:
        """Return a QWidget for the panel."""
        ...
```

## Plugin Manager

```python
import asyncio
import importlib.util
import inspect
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

class PluginManager:
    def __init__(self, plugin_dirs: List[Path]):
        self._plugin_dirs = plugin_dirs
        self._discovered: Dict[str, Type[VMHarnessPlugin]] = {}
        self._loaded: Dict[str, VMHarnessPlugin] = {}
        self._context = PluginContext()
    
    def discover_plugins(self) -> Dict[str, Type[VMHarnessPlugin]]:
        """Discover all plugins in plugin_dirs."""
        for plugin_dir in self._plugin_dirs:
            if not plugin_dir.exists():
                continue
            for py_file in plugin_dir.glob("*.py"):
                if py_file.name.startswith("_"):
                    continue
                try:
                    spec = importlib.util.spec_from_file_location(
                        f"plugin_{py_file.stem}", py_file
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        for name, obj in inspect.getmembers(module):
                            if (inspect.isclass(obj) and
                                issubclass(obj, VMHarnessPlugin) and
                                obj is not VMHarnessPlugin and
                                obj is not PanelPlugin):
                                instance = obj()
                                metadata = instance.get_metadata()
                                self._discovered[metadata.name] = obj
                except Exception as e:
                    logging.warning(f"Failed to load plugin from {py_file}: {e}")
        return self._discovered
    
    def load_plugin(self, name: str) -> Optional[VMHarnessPlugin]:
        """Load and initialize a plugin."""
        if name in self._loaded:
            return self._loaded[name]
        if name not in self._discovered:
            return None
        plugin_cls = self._discovered[name]
        instance = plugin_cls()
        loop = self._get_or_create_loop()
        loop.run_until_complete(instance.initialize(self._context))
        self._loaded[name] = instance
        return instance
    
    def load_all(self) -> List[VMHarnessPlugin]:
        """Load all discovered plugins."""
        return [self.load_plugin(name) for name in self._discovered]
    
    def unload_plugin(self, name: str) -> None:
        """Unload a plugin."""
        if name in self._loaded:
            instance = self._loaded.pop(name)
            try:
                loop = self._get_or_create_loop()
                loop.run_until_complete(instance.shutdown())
            except Exception:
                pass
    
    def unload_all(self) -> None:
        """Unload all plugins."""
        for name in list(self._loaded.keys()):
            self.unload_plugin(name)
    
    def get_panels(self) -> List[PanelPlugin]:
        """Return all loaded PanelPlugin instances."""
        return [p for p in self._loaded.values() if isinstance(p, PanelPlugin)]
    
    @staticmethod
    def _get_or_create_loop() -> asyncio.AbstractEventLoop:
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
```

## GUI Integration

```python
# In MainWindow.__init__:
self.plugin_manager = PluginManager(plugin_dirs=[Path("plugins")])
self.plugin_manager.discover_plugins()
self.plugin_manager.load_all()
self._load_plugin_panels()

def _load_plugin_panels(self):
    for plugin in self.plugin_manager.get_panels():
        panel = plugin.create_panel()
        if panel:
            name = plugin.get_metadata().name
            self.panels[name] = panel
            self.panel_stack.addWidget(panel)
            self.sidebar.add_panel_button(name, lambda n=name: self._switch_panel(n))
            # Wire bridges
            if hasattr(panel, "set_qmp_bridge"):
                panel.set_qmp_bridge(self.qmp_bridge)
            if hasattr(panel, "set_ssh_bridge"):
                panel.set_ssh_bridge(self.ssh_bridge)
```

## Example Plugin

```python
from gui.plugin import PluginContext, PluginMetadata, PanelPlugin
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class ExamplePanelPlugin(PanelPlugin):
    def __init__(self):
        self._panel = None
    
    async def initialize(self, context: PluginContext) -> bool:
        self._panel = QWidget()
        layout = QVBoxLayout(self._panel)
        label = QLabel("Example Plugin Panel")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return True
    
    async def shutdown(self) -> None:
        if self._panel:
            self._panel.deleteLater()
            self._panel = None
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="example-panel",
            version="1.0.0",
            description="Example panel plugin",
            plugin_type="panel",
        )
    
    def create_panel(self) -> QWidget:
        return self._panel
```

## Pitfalls

1. **Missing `import asyncio` in plugin_manager.py** — The manager uses `asyncio.get_event_loop()` and `asyncio.new_event_loop()` but if `asyncio` is not imported, the error is misleading: `name 'asyncio' is not defined` appears in the plugin's `initialize()` method, not in the manager. Always verify imports in the manager, not just the plugin.

2. **Plugin panel name collision** — If a plugin panel name matches a built-in panel, the plugin panel is silently skipped. Check for collisions in `_load_plugin_panels()`.

3. **Bridge wiring must be explicit** — Plugin panels don't automatically get bridges. The main window must check for `set_qmp_bridge`, `set_ssh_bridge`, etc. and wire them manually.

4. **Async `initialize()` requires event loop** — Plugin `initialize()` is async and requires a running event loop. The PluginManager must provide one via `_get_or_create_loop()`. If the loop is not running, `run_until_complete()` will fail.

5. **Plugin panel must be a QWidget** — `create_panel()` must return a valid QWidget. If it returns None or a non-QWidget, the panel stack will crash.

6. **Theme attributes must exist** — Plugin panels use theme attributes like `T.BG_TERTIARY`. Verify they exist with `grep -n 'BG_' gui/theme.py` before referencing them.

7. **Plugin discovery skips `_`-prefixed files** — Files starting with `_` (like `__init__.py`) are skipped during discovery. This is intentional to avoid loading utility modules.

8. **Plugin unloading must clean up resources** — `shutdown()` must call `deleteLater()` on all QWidgets to avoid memory leaks. The PluginManager calls `shutdown()` during `unload_plugin()`.
