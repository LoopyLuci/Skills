# Chat Window Pattern

## CRITICAL PITFALL: QDockWidget Does NOT Work in QSplitter

`QDockWidget` is designed to be used with `QMainWindow.addDockWidget()` ONLY. Embedding a `QDockWidget` inside a `QSplitter` causes:
- Overlapping widgets (both QDockWidgets render on top of each other)
- Layout conflicts (QDockWidget tries to be a standalone window)
- Visual glitches and crashes

**The fix:** Use plain `QWidget` subclasses for panels that go into `QSplitter`. Use `QMainWindow` subclasses for standalone windows. Never wrap a `QDockWidget` in a `QSplitter`.

**If the user wants a panel to be both embedded AND floatable:** Create TWO classes:
1. `XxxWidget(QWidget)` — embeds in splitter
2. `XxxWindow(QMainWindow)` — standalone window with `setCentralWidget(XxxWidget())`

## Separation Pattern: Dedicated Windows vs Embedded Panels

When the user says "I want X and Y to be completely separate" or "don't put them together":

1. **Do NOT embed them in the same splitter** — even as QWidget subclasses
2. **Create standalone QMainWindow for each** — each is a separate window
3. **Provide access via menu/shortcut** — e.g., View > Open X Window (Ctrl+Alt+X)
4. **Keep only non-conflicting panels in main splitter** — e.g., DOM, Snippets, Commands

```python
# Main window __init__
# DON'T: self.properties_dock = PropertiesDockWidget(self)
# DON'T: self.right_splitter.addWidget(self.properties_dock)

# DO: Properties is standalone, opened via menu
# Right splitter only has:
self.right_splitter.addWidget(self.dom_panel)
self.right_splitter.addWidget(self.snippets_panel)
self.right_splitter.addWidget(self.command_panel)

# View menu:
open_props_action = QAction("Open Properties Window...", self)
open_props_action.setShortcut("Ctrl+Alt+P")
open_props_action.triggered.connect(self._open_properties_window)
```

## ChatWindow (QMainWindow)

A dedicated AI chat window with professional layout.

### Components

1. **Toolbar** (`QToolBar`)
   - New Chat action (`Ctrl+N`)
   - Session selector (`QComboBox`)
   - Model selector (`QComboBox`)
   - Temperature slider (`QSlider` 0-200, display as 0.00-2.00)
   - Export/Clear actions

2. **Chat Display** (`QTextBrowser`)
   - User messages: right-aligned, blue background (`#3b82f6`)
   - AI messages: left-aligned, dark background (`#1e293b`), colored avatar label
   - System messages: centered, muted text
   - Auto-scroll to bottom on new messages

3. **Typing Indicator** (`QLabel`)
   - Animated dots via `QTimer` (500ms interval)
   - Hidden by default, shown during AI generation

4. **Input Area** (`QTextEdit` + `QPushButton`)
   - Multi-line input with placeholder text
   - Send button with keyboard shortcut (Enter)
   - Token counter display

5. **Conversation Sidebar** (`QDockWidget`)
   - Dockable/floatable
   - Conversation list (`QListWidget`)
   - Click to load previous conversations

### Key Signals

```python
sections_generated = pyqtSignal(list)  # Generated sections from AI
```

### Integration Pattern

```python
# To show standalone window:
self.chat_window = ChatWindow(self)
self.chat_window.sections_generated.connect(self._on_ai_sections_generated)
self.chat_window.show()
self.chat_window.raise_()
self.chat_window.activateWindow()
```

### Close Behavior

Override `closeEvent` to minimize instead of close:
```python
def closeEvent(self, event):
    event.ignore()
    self.showMinimized()
```

### Singleton Pattern

```python
_chat_window: Optional[ChatWindow] = None

def get_chat_window(parent=None) -> ChatWindow:
    global _chat_window
    if _chat_window is None:
        _chat_window = ChatWindow(parent)
    return _chat_window
```

## PropertiesWindow (QMainWindow)

A dedicated properties/section editing window.

### Components

1. **Text Content Group** — Text editor for section content
2. **Layout Group** — Padding, margin spinboxes
3. **Styling Group** — Background color, border radius, opacity
4. **Animation Group** — Animation type combo, delay spinbox
5. **Custom CSS Group** — Free-form CSS editor

### Integration

```python
# Standalone window (Ctrl+Alt+P)
_props_window: Optional[PropertiesWindow] = None

def get_properties_window(parent=None) -> PropertiesWindow:
    global _props_window
    if _props_window is None:
        _props_window = PropertiesWindow(parent)
    return _props_window
```

## Panel Toggle Pattern

For panels that ARE embedded in the main window (DOM, Snippets, Commands):

```python
# View menu
toggle_dom_action = QAction("Toggle DOM Panel", self)
toggle_dom_action.triggered.connect(self._toggle_dom_panel)
view_menu.addAction(toggle_dom_action)

# Handler
def _toggle_dom_panel(self):
    if hasattr(self, 'dom_panel'):
        self.dom_panel.setVisible(not self.dom_panel.isVisible())
```

For standalone windows (Properties, Chat), use "Open X Window" actions instead of toggles.