# Visual Editor Patterns for WebBuilder Desktop
## 2026-08-22

### Drag-and-Drop Canvas

Use `QDrag` and `QMimeData` for drag-and-drop. QPushButton has NO `setDragEnabled()` method.

```python
class SectionWidget(QFrame):
    """Visual section with drag support"""
    clicked = pyqtSignal(str)
    
    def __init__(self, section_data, parent=None):
        super().__init__(parent)
        self.section_id = section_data['id']
        self._drag_start = None
        self.setAcceptDrops(True)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.pos()
            self.clicked.emit(self.section_id)
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self._drag_start and (event.pos() - self._drag_start).manhattanLength() > 10:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.section_id)
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)
        super().mouseMoveEvent(event)
```

### Canvas Widget

```python
class CanvasWidget(QScrollArea):
    section_selected = pyqtSignal(dict)
    section_added = pyqtSignal(dict)
    section_deleted = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sections = []
        self.selected_id = None
        self.setWidgetResizable(True)
        self.setAcceptDrops(True)
        
        self.container = QWidget()
        self.container.setAcceptDrops(True)
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignTop)
        self.setWidget(self.container)
    
    def load_sections(self, sections):
        self.sections = sections
        # Clear existing
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        if not sections:
            self.show_empty_state()
            return
        
        for section in sections:
            widget = self.create_section_widget(section)
            self.layout.addWidget(widget)
        self.layout.addStretch()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        if event.mimeData().hasText():
            # Handle drop logic
            event.acceptProposedAction()
```

### Properties Panel with Live Editing

```python
class PropertiesPanel(QWidget):
    property_changed = pyqtSignal(str, object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_section = None
        self.scroll = QScrollArea()
        self.content = QWidget()
        self.form = QFormLayout(self.content)
        self.scroll.setWidget(self.content)
    
    def load_section(self, section):
        self.current_section = section
        self.clear_form()
        
        if not section:
            self.show_placeholder()
            return
        
        props = section.get('props', {})
        for key, value in props.items():
            if isinstance(value, str):
                line_edit = QLineEdit(value)
                line_edit.textChanged.connect(lambda v, k=key: self.on_text_changed(k, v))
                self.form.addRow(f"{key}:", line_edit)
            elif isinstance(value, (int, float)):
                spin = QDoubleSpinBox()
                spin.setValue(value)
                spin.valueChanged.connect(lambda v, k=key: self.on_number_changed(k, v))
                self.form.addRow(f"{key}:", spin)
            elif isinstance(value, bool):
                check = QCheckBox()
                check.setChecked(value)
                check.stateChanged.connect(lambda v, k=key: self.on_bool_changed(k, v))
                self.form.addRow(f"{key}:", check)
    
    def on_text_changed(self, key, value):
        if self.current_section:
            self.current_section['props'][key] = value
            self.property_changed.emit(key, value)
```

### Dockable Chat Panel

```python
class ChatPanel(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.history = []
        
        # Header with provider selector
        header = QWidget()
        self.provider_label = QLabel("🤖 Agent")
        self.status_label = QLabel("⚪")
        
        # Messages area
        self.chat_area = QScrollArea()
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_area.setWidget(self.chat_content)
        
        # Input
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send)
    
    def add_message(self, role, content):
        bubble = QLabel(content)
        bubble.setWordWrap(True)
        if role == "user":
            bubble.setStyleSheet("background: #3b82f6; color: white; padding: 8px 12px; border-radius: 12px 12px 4px 12px;")
        else:
            bubble.setStyleSheet("background: #334155; color: #f8fafc; padding: 8px 12px; border-radius: 12px 12px 12px 4px;")
        self.chat_layout.addWidget(bubble)

# In main window:
self.chat_dock = QDockWidget("🤖 Agent Chat", self)
self.chat_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea | Qt.BottomDockWidgetArea)
self.dock_chat = ChatPanel(self.config)
self.chat_dock.setWidget(self.dock_chat)
self.addDockWidget(Qt.RightDockWidgetArea, self.chat_dock)
```

### Flask Backend Integration

```python
class FlaskManager(QObject):
    status_changed = pyqtSignal(str, bool)
    
    def __init__(self):
        super().__init__()
        self.process = None
        self.port = 5000
        self.base_url = f"http://localhost:{self.port}"
    
    def start(self):
        if self.process and self.process.poll() is None:
            return
        
        app_path = Path(__file__).parent / "app.py"
        self.process = subprocess.Popen(
            [sys.executable, str(app_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        
        # Poll health endpoint - Flask takes 0.5-2s to start
        import time
        for i in range(10):
            time.sleep(0.5)
            try:
                r = requests.get(f"{self.base_url}/api/v1/health", timeout=1)
                if r.status_code == 200:
                    self.status_changed.emit("running", True)
                    return
            except:
                pass
        
        self.status_changed.emit("failed", False)
    
    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
            self.process = None
            self.status_changed.emit("stopped", False)
    
    def is_running(self):
        return self.process and self.process.poll() is None
```

### API Key Management

```python
class ConfigManager:
    CONFIG_DIR = Path.home() / ".webbuilder"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    def __init__(self):
        self.keys = {}
        self.settings = {}
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.load()
    
    def load(self):
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, 'r') as f:
                data = json.load(f)
                self.settings = data.get('settings', {})
                self.keys = data.get('keys', {})
    
    def save(self):
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump({'settings': self.settings, 'keys': self.keys}, f, indent=2)
    
    def get_key(self, provider):
        return self.keys.get(provider, '')
    
    def set_key(self, provider, key):
        self.keys[provider] = key
        self.save()
```

### Export System

```python
class HTMLExporter:
    """Export project to static HTML/CSS/JS"""
    
    def __init__(self, project: Dict):
        self.project = project
        self.design = project.get('design', {})
    
    def export(self, output_path: str) -> str:
        html = self.generate_html()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path
    
    def generate_html(self) -> str:
        sections = self.project['pages'][0]['sections']
        html = '<!DOCTYPE html><html><head>...</head><body>'
        for section in sections:
            html += self.render_section(section)
        html += '</body></html>'
        return html

class ReactExporter:
    """Export project to React components"""
    
    def export(self, output_dir: str) -> str:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        # Generate package.json, App.jsx, components, styles
        return output_dir

class ExportManager:
    def __init__(self, project: Dict):
        self.exporters = {
            'html': HTMLExporter(project),
            'react': ReactExporter(project),
        }
    
    def export_all(self, output_dir: str) -> Dict[str, str]:
        results = {}
        for name, exporter in self.exporters.items():
            results[name] = exporter.export(os.path.join(output_dir, name))
        return results
```

### Plugin Architecture

```python
class PluginInterface(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass
    
    @property
    @abstractmethod
    def version(self) -> str: pass
    
    @abstractmethod
    def initialize(self, config: Dict) -> bool: pass

class ComponentPlugin(PluginInterface):
    @abstractmethod
    def render(self, props: Dict) -> str: pass
    
    @abstractmethod
    def get_default_props(self) -> Dict: pass

class PluginRegistry:
    def __init__(self):
        self._components = {}
        self._exporters = {}
    
    def register(self, plugin: PluginInterface):
        if isinstance(plugin, ComponentPlugin):
            self._components[plugin.name] = plugin

class PluginLoader:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.registry = PluginRegistry()
    
    def load_all(self):
        for plugin_path in self.plugin_dir.iterdir():
            if plugin_path.is_dir():
                self._load_plugin(plugin_path)
```

### Critical Pitfalls

1. **QPushButton.setDragEnabled doesn't exist**: Must implement drag manually in `mouseMoveEvent`
2. **Flask startup race**: Always poll health endpoint in a loop (0.5-2s startup)
3. **Lambda capture in loops**: Use `lambda checked, t=cid: func(t)` not `lambda: func(cid)`
4. **Layout clearing**: Call `widget.deleteLater()` before removing from layout
5. **Config directory**: Create `~/.webbuilder/` before writing config files
6. **Widget parenting**: Always set parent widget or layout to avoid memory leaks
7. **f-string syntax**: In Python, f-strings with dict access need careful quoting: `f'{p["key"]}'` not `f'{p['key']}'`
