# Generative UI Implementation — September 2026

Complete implementation of a self-modifying interface engine for WebBuilder Desktop.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    GENERATIVE UI SYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   SCHEMA     │  │   ENGINE     │  │   AGENT      │         │
│  │   LAYER      │  │   LAYER      │  │   LAYER      │         │
│  │              │  │              │  │              │         │
│  │ Declarative  │  │ Mutation     │  │ Natural      │         │
│  │ UI           │  │ Engine       │  │ Language     │         │
│  │ Description  │  │ State Mgmt   │  │ Command      │         │
│  │              │  │ Rendering    │  │ Parser       │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
│                            │                                   │
│                    ┌───────┴───────┐                           │
│                    │   QT WIDGETS  │                           │
│                    │   RENDERING   │                           │
│                    └───────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

## Module Structure

```
webbuilder/generative_ui/
├── __init__.py           # UINode, UIStyle, UIBinding, UIEvent, StateManager
│                         # MutationEngine, Mutation, MutationType
│                         # AgentCommandParser
├── themes.py             # Theme, ThemeManager, 6 pre-built themes
│                         # generate_stylesheet()
├── widget_factory.py     # WidgetFactory with 25+ creators
│                         # create_widget(), apply_properties(), apply_style()
├── virtual_list.py       # VirtualList, LazyLoader, RenderOptimizer
└── code_generator.py     # CodeGenerator (HTML/React/Vue/Python output)
```

## Key Components

### 1. UINode (Declarative UI Schema)

```python
@dataclass
class UINode:
    """A single node in the UI tree."""
    id: str
    type: str
    props: dict[str, Any] = field(default_factory=dict)
    style: UIStyle = field(default_factory=UIStyle)
    children: list['UINode'] = field(default_factory=list)
    bindings: list[UIBinding] = field(default_factory=list)
    events: list[UIEvent] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
```

**30+ node types**: label, button, input, text_area, combo, spin, slider, check, radio, progress, group, tabs, panel, divider, spacer, table, list, tree, scroll, splitter, stack, image, markdown, code_editor, canvas, window, dialog, layout_v, layout_h, layout_form.

### 2. MutationEngine

```python
class MutationType(Enum):
    ADD = 'add'           # Add new node
    REMOVE = 'remove'     # Remove node
    UPDATE = 'update'     # Update properties
    MOVE = 'move'         # Move node
    REPLACE = 'replace'   # Replace node
    STYLE = 'style'       # Change style
    BIND = 'bind'         # Add binding
    EVENT = 'event'       # Add event handler

@dataclass
class Mutation:
    type: str
    target_id: str
    payload: dict[str, Any] = field(default_factory=dict)

class MutationEngine:
    def apply(self, mutation: Mutation) -> bool: ...
    def undo(self) -> Optional[Mutation]: ...
    def redo(self) -> Optional[Mutation]: ...
```

### 3. WidgetFactory (Schema → Qt Widget)

```python
class WidgetFactory:
    _creators: dict[str, Callable] = {
        'label': _create_label,
        'button': _create_button,
        'input': _create_input,
        # ... 25+ more types
    }
    
    @classmethod
    def create_widget(cls, node: UINode, parent: QWidget = None) -> QWidget:
        """Create a Qt widget from a UINode."""
        creator = cls._creators.get(node.type)
        if creator:
            widget = creator(node, parent)
            cls.apply_properties(widget, node)
            cls.apply_style(widget, node)
            cls.apply_events(widget, node)
            return widget
        return cls._create_label(node, parent)
```

**IMPORTANT**: Creator functions MUST be `@staticmethod`, not `@classmethod`. Using `@classmethod` causes `TypeError: 'classmethod' object is not callable` when stored in a dict and retrieved.

### 4. AgentCommandParser (Natural Language → Mutations)

```python
class AgentCommandParser:
    def parse(self, command: str) -> list[Mutation]:
        """Parse natural language into mutations."""
        patterns = {
            r'add button\s+"?([^"]+)"?': self._add_button,
            r'add label\s+"?([^"]+)"?': self._add_label,
            r'add input\s+(?:with placeholder\s+)?"?([^"]+)"?': self._add_input,
            r'remove\s+(?:element\s+)?(\w+)': self._remove_element,
            r'change text\s+(?:of\s+)?(\w+)\s+(?:to\s+)?"?([^"]+)"?': self._change_text,
            r'change color\s+(?:of\s+)?(\w+)\s+(?:to\s+)?(\w+)': self._change_color,
        }
        for pattern, handler in patterns.items():
            match = re.search(pattern, command)
            if match:
                return handler(match)
        return []
```

### 5. Theme System

```python
@dataclass
class Theme:
    """A complete visual theme."""
    id: str
    name: str
    colors: dict[str, str] = field(default_factory=dict)
    font_family: str = "'Inter', 'Segoe UI', sans-serif"
    font_mono: str = "'Fira Code', 'Consolas', monospace"
    font_sizes: dict[str, int] = field(default_factory=lambda: {
        'xs': 10, 'sm': 11, 'base': 12, 'md': 14, 'lg': 16, 'xl': 20
    })
    spacing: dict[str, int] = field(default_factory=lambda: {
        '0': 0, '1': 4, '2': 8, '3': 12, '4': 16, '5': 20
    })
    radius: dict[str, int] = field(default_factory=lambda: {
        'none': 0, 'sm': 4, 'md': 6, 'lg': 8, 'xl': 12
    })

class ThemeManager:
    def set_theme(self, theme_id: str) -> bool: ...
    def generate_stylesheet(self, theme: Theme = None) -> str: ...
```

**Pre-built themes**: Dark, Light, Midnight, Forest, Sunset, Ocean.

### 6. VirtualList (High-Performance Rendering)

```python
class VirtualList(QWidget):
    """Virtualized list that only renders visible items.
    Handles 100,000+ items efficiently."""
    
    def __init__(self, item_height: int = 40, parent: QWidget = None):
        self._item_height = item_height
        self._items: list[Any] = []
        self._visible_range: tuple[int, int] = (0, 0)
        self._render_cache: dict[int, QWidget] = {}
    
    def set_items(self, items: list[Any]): ...
    def _update_visible_range(self): ...
    def _render_visible_items(self): ...
```

### 7. CodeGenerator (Canvas → Code)

```python
class CodeGenerator:
    def generate_html(self) -> str: ...
    def generate_react(self) -> dict[str, str]: ...
    def generate_vue(self) -> dict[str, str]: ...
    def generate_python(self) -> str: ...
    def save(self, output_dir: Path, format: str = 'html'): ...
```

## Integration with WebBuilder Desktop

### CommandPanel (GUI Component)

```python
class CommandPanel(QWidget):
    """Panel for executing natural language commands to modify the UI."""
    command_executed = pyqtSignal(str, bool, str)  # command, success, message
    
    def _setup_ui(self):
        # Command input with placeholder
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Type command...")
        self.command_input.returnPressed.connect(self._execute_command)
        
        # Quick command buttons: +Btn, +Label, +Input, Undo
        # Status label for feedback
```

### Canvas Integration

```python
class Canvas(QWidget):
    def add_generative_widget(self, widget: QWidget, node: Any):
        """Add a generative widget to the canvas."""
        self._generative_widgets[node.id] = widget
        self._generative_nodes[node.id] = node
        
        # Create wrapper frame with type label + remove button
        wrapper = QFrame()
        wrapper.setStyleSheet(
            "QFrame { background: rgba(30, 41, 59, 0.3); "
            "border: 1px dashed rgba(59, 130, 246, 0.5); "
            "border-radius: 6px; padding: 4px; margin: 2px 0; }"
        )
        # ... add header with type label and remove button
        # ... add widget to wrapper
        # ... insert before stretch in canvas layout
    
    def remove_generative_widget(self, node_id: str): ...
    def update_generative_widget(self, node_id: str, props: dict): ...
```

### Main Window Integration

```python
class WebBuilderWindow(QMainWindow):
    def _on_command_executed(self, command: str, success: bool, message: str):
        """Handle generative UI command execution."""
        if success:
            self._apply_generative_command(command)
    
    def _apply_generative_command(self, command: str):
        """Apply a generative UI command to the canvas."""
        parser = AgentCommandParser(None)
        mutations = parser.parse(command)
        mutation = mutations[0]
        
        if mutation.type == MutationType.ADD.value:
            node = UINode.from_dict(mutation.payload.get('node', {}))
            widget = create_widget(node)
            self.canvas.add_generative_widget(widget, node)
        elif mutation.type == MutationType.REMOVE.value:
            self.canvas.remove_generative_widget(mutation.target_id)
        elif mutation.type == MutationType.UPDATE.value:
            self.canvas.update_generative_widget(mutation.target_id, props)
    
    def _switch_theme(self, theme_id: str):
        """Switch the application theme."""
        manager = get_theme_manager()
        if manager.set_theme(theme_id):
            stylesheet = manager.generate_stylesheet()
            self.setStyleSheet(stylesheet)
```

## Pitfalls Encountered

### 1. Widget Factory @classmethod vs @staticmethod

**Error:** `TypeError: 'classmethod' object is not callable`

**Cause:** Creator functions defined as `@classmethod` but called via dict lookup.

**Fix:** Always use `@staticmethod` for widget factory creators.

### 2. Stale __pycache__ After Class Modifications

**Error:** `AttributeError: 'ChatPanel' object has no attribute 'refresh_btn'`

**Cause:** After modifying PyQt class definitions, stale `.pyc` files caused old code to run.

**Fix:** `find . -type d -name "__pycache__" -exec rm -rf {} +`

### 3. Canvas Generative Widgets Need Wrapper

**Problem:** Adding widgets directly to canvas layout caused display issues.

**Fix:** Wrap each generative widget in a styled QFrame with type label and remove button.

### 4. Theme Stylesheet Application

**Problem:** Applying stylesheet to individual widgets didn't propagate.

**Fix:** Apply to main window: `self.setStyleSheet(stylesheet)` on `QMainWindow`.

### 5. Command Parser Returns List

**Problem:** Accessing `mutations[0]` without checking if list is empty.

**Fix:** Always check `if mutations:` before accessing elements.

## Testing

```python
# Test command parsing
parser = AgentCommandParser(None)
mutations = parser.parse('add button "Submit"')
assert len(mutations) == 1
assert mutations[0].type == 'add'

# Test widget factory
node = UINode(id='btn1', type='button', props={'text': 'Submit'})
widget = create_widget(node)
assert type(widget).__name__ == 'QPushButton'
assert widget.text() == 'Submit'

# Test theme manager
manager = get_theme_manager()
assert manager.set_theme('dark')
stylesheet = manager.generate_stylesheet()
assert 'QMainWindow' in stylesheet
```

## File Locations

- `webbuilder/generative_ui/__init__.py` — Core schema, mutations, parser
- `webbuilder/generative_ui/themes.py` — Theme system
- `webbuilder/generative_ui/widget_factory.py` — Widget creators
- `webbuilder/generative_ui/virtual_list.py` — High-performance lists
- `webbuilder/generative_ui/code_generator.py` — Code output
- `webbuilder/gui/__init__.py` — CommandPanel, Canvas integration, Main window wiring
- `GENERATIVE_UI_GUIDE.md` — Comprehensive design guide (24KB, 14 sections)