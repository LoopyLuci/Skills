# WebBuilder Desktop GUI Features (September 2026)

This document covers the comprehensive GUI features built for WebBuilder Desktop in September 2026.

## Features Implemented

### 1. Visual Form Builder (`form_builder_dialog.py`)

A drag-and-drop form designer with three-panel layout:

- **Left Panel**: Draggable field palette (10 types: Text, Email, Select, Textarea, Number, Checkbox, Radio, File, Date, Tel)
- **Center Panel**: Form canvas with visual field previews, selection, reordering (▲/▼), deletion
- **Right Panel**: Property editor for selected field (label, placeholder, required checkbox, options editor for select/radio)
- **Toolbar**: Form name input, Quick Add buttons, Clear, Preview, Save Form
- **Bottom Tabs**: Live HTML preview and JSON data preview

**Integration**: Connected to canvas as Form section type. Uses `form_saved` signal to emit form data.

### 2. Project Browser (`ProjectBrowserDialog`)

Visual project management with card-based UI:

- Grid of project cards (3 columns) with hover effects
- Project name, date modified, section count per card
- Preview thumbnail showing first 3 section types (e.g., "Hero → Features → CTA +5 more")
- Search bar filtering projects by name
- Sort options: Date (newest/oldest), Name (A-Z/Z-A), Size (sections)
- Open, Duplicate, Delete buttons per card
- New Project button creates blank project
- Delete confirmation dialog

**Menu**: "Project Browser" action with Ctrl+O shortcut replaces basic File → Open dialog.

### 3. Enhanced AI Chat (`chat_enhanced.py`)

Comprehensive chat improvements:

- **Conversation History**: Timestamped messages with session persistence
- **Model Info Display**: Current model name, provider, context length in header
- **Markdown Renderer**: Code blocks (``` fenced), inline code, bold, italic, headers, lists, links
- **Chat Bubbles**: User messages (right, blue), AI responses (left, gray), avatars
- **Session Manager**: Create, save, load, rename, delete chat sessions
- **Export**: Save conversation as JSON or text
- **Temperature Slider**: Adjustable in chat toolbar
- **Clear Chat**: Reset conversation
- **Typing Indicator**: Animated dots while generating

### 4. SEO Dashboard (`SEODashboardDialog`)

Visual SEO analysis with custom QPainter charts:

- Circular SEO score gauge (0-100) with color coding
- Issues grouped by severity (Critical/Warning/Info) with icons
- Keyword density bar chart
- Google search meta preview
- Sitemap/robots.txt status
- Recommendations tab

### 5. Analytics Dashboard (`AnalyticsDashboardDialog`)

Usage analytics visualization:

- Event timeline bar chart (daily events)
- Pie chart for event type breakdown
- Stats cards: total events, last 24h, last 7d, last 30d
- Most common events list

### 6. Comprehensive Settings (`SettingsDialog`)

Production-grade settings with 5 tabs:

- **Providers**: API key fields (show/hide), test connection, model checkboxes (free first), status indicators
- **General**: Default model dropdown, temperature slider, max tokens, theme/language selectors, auto-save interval
- **Export**: Format selector, path browser, CSS/JS/minify options
- **Hardware**: CPU cores/frequency, GPU detection, thread slider, memory bar
- **Security**: Upload limits, file extensions, rate limiting

### 7. Modules Menu

Access to all contrib modules from the GUI:

- CMS Manager
- E-Commerce
- Publishing
- Collaboration
- Plugin Manager
- Analytics Dashboard
- Search Index

### 8. Code Generator Export

File → Export Generated Code menu with 4 formats:

- HTML (standalone files)
- React (multi-file components)
- Python (PyQt5 code)
- Vue (single-file components)

## Architecture Notes

### Verification Without Display Server

To verify GUI without a display:

```python
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
app = QApplication([])

# Now create and test windows
```

### Stale `__pycache__` Issue

When imports fail with `ImportError` despite code being correct:

```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Widget Factory Style Mapping

Declarative `UIStyle` uses `border_color`, `border_width`, `border_radius` (not `border`). The WidgetFactory maps these to CSS properties individually.

### Form Builder Signal Pattern

```python
class FormBuilderDialog(QDialog):
    form_saved = pyqtSignal(object, str, list)  # form, html, fields
```

Connect to this signal to receive form data when user saves.

## Menu Structure

```
File
├── New Project (Ctrl+N)
├── New from Template... (Ctrl+Shift+N)
├── Project Browser (Ctrl+O)
├── Open File... (Ctrl+Shift+O)
├── Save Project (Ctrl+S)
├── Export HTML (Ctrl+E)
└── Export Generated Code
    ├── HTML
    ├── REACT
    ├── VUE
    └── PYTHON

Tools
├── SEO Analysis...
├── SEO Dashboard...
├── Analytics Dashboard...
├── Settings
└── Form Builder...

Modules
├── CMS Manager
├── E-Commerce
├── Publishing
├── Collaboration
├── Plugin Manager
├── Analytics Dashboard
└── Search Index
```

### 9. Terminal CLI Widget (`terminal_cli.py`)

Standalone terminal widget embeddable in the main window or dockable as a floating panel:

- **Command execution**: Runs shell commands via `subprocess.run` in a QThread (non-blocking UI)
- **Color-coded output**: ANSI escape codes rendered as HTML spans (red=error, green=success, yellow=warning, gray=debug)
- **Command history**: ↑/↓ arrows navigate previous commands
- **Minimize**: Collapses to header bar (▼ button toggles)
- **Drag-resize**: Grab bottom edge (8px handle) to resize height between 80px–500px
- **Copy button**: Copies all output to clipboard
- **Save button**: Saves output to timestamped `.txt` file via file dialog
- **API**: `log()`, `log_success()`, `log_error()`, `log_warning()`, `log_debug()`, `execute_command()`, `get_output_text()`, `clear_output()`

### 10. Activity Log Tab (`activity_log.py`)

Dedicated tab showing all activity, errors, and debugging with filtering and export:

- **Color-coded levels**: Info (gray), Success (green), Warning (amber), Error (red), Debug (dim)
- **Filter dropdown**: Filter by log level (all/info/success/warning/error/debug)
- **Search**: Real-time text filter across message and source fields
- **Auto-scroll**: Toggle-able, scrolls to latest entry
- **Copy button**: Copies filtered log text to clipboard
- **Save button**: Saves to `.txt` or `.json` via file dialog
- **Export JSON**: Structured JSON export with timestamp, level, source, message per entry
- **Clear**: Confirmation dialog before clearing all entries
- **Entry count**: Shows total entries and filtered count
- **API**: `add_log()`, `info()`, `success()`, `warning()`, `error()`, `debug()`, `get_logs()`, `save_to_file()`, `copy_to_clipboard()`, `clear()`

### 11. `_TerminalActivityHandler` — Logging Router

Routes Python `logging` records to both TerminalCLI and ActivityTab:

```python
class _TerminalActivityHandler(logging.Handler):
    """Logging handler that routes messages to TerminalCLI and ActivityTab."""
    
    def emit(self, record: logging.LogRecord) -> None:
        level = self._level_map.get(record.levelno, "info")
        source = record.name.replace("webbuilder.", "")
        message = self.format(record)
        if self._terminal:
            self._terminal.append_line(message, level)
        if self._activity:
            self._activity.add_log(message, level, source)
```

**Integration**: Added to `webbuilder.gui.__init__.py` main window `__init__`, deferred via `QTimer.singleShot(100, self._setup_logging_handler)` to avoid initialization segfault.

**Wiring**: Routes all `webbuilder.*` logger output to both the Terminal CLI and Activity Log tab automatically.

### 12. Chat/Properties Snap-to-Main-Window

Both ChatWindow and PropertiesWindow can now snap into the main window's right splitter:

- **Snap button**: Toolbar button toggles between "📌 Snap to Main" and "📌 Unsnap from Main"
- **Keyboard shortcut**: Ctrl+Alt+S toggles snap state
- **State tracking**: `_is_snapped` flag tracks docked vs. floating state
- **Dock widget**: `_chat_dock` / `_props_dock` created on snap, removed on unsnap
- **Main window handlers**: `handle_chat_snap_request()` / `handle_properties_snap_request()` manage the dock integration
- **Auto-open**: Both windows auto-open on launch with `QTimer.singleShot(500, self._auto_open_windows)`

**Initialization order pitfall**: `_is_snapped` must be initialized BEFORE `setup_ui()` is called (since `_update_snap_button()` references it). `snap_btn` must be created BEFORE `_update_snap_button()` is called.
