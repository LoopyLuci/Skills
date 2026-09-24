# Design Token System and QSS Generation for PyQt5 Desktop Apps

A design-token class plus QSS generator functions give a PyQt5 app a single source
of truth for colors, spacing, typography, and border radii — and produce consistent
stylesheets across every widget without hardcoding hex values in widget code.

## Pattern Overview

```
gui/
  theme.py     # T token class + dark_palette() + <widget>_style() generators
  widgets.py   # All widgets import from theme; use T.<token> and <fn>() for QSS
```

## Token Class (`T`)

Define one class that holds every design constant. Import as `from gui.theme import T`.

```python
class T:
    # Colors — surface hierarchy
    BG_PRIMARY   = "#0f172a"   # main window / panel background
    BG_SECONDARY = "#1e293b"   # cards, inputs, secondary surfaces
    BG_TERTIARY  = "#334155"   # borders, dividers, hover states

    # Colors — text hierarchy
    TEXT_PRIMARY   = "#e2e8f0"   # values, labels
    TEXT_SECONDARY = "#94a3b8"   # descriptions, hints
    TEXT_MUTED     = "#64748b"   # placeholders, disabled

    # Colors — semantic / brand
    BRAND       = "#3b82f6"
    BRAND_HOVER = "#2563eb"
    SUCCESS     = "#22c55e"
    WARNING     = "#f59e0b"
    ERROR       = "#ef4444"
    INFO        = "#38bdf8"

    # Colors — status dots
    DOT_RUNNING_CONNECTED = "#22c55e"
    DOT_RUNNING           = "#eab308"
    DOT_CONNECTED         = "#3b82f6"
    DOT_OFFLINE           = "#555555"

    # Colors — chart series
    CHART_CPU    = "#38bdf8"
    CHART_RAM    = "#a78bfa"
    CHART_DISK   = "#22c55e"
    CHART_NET    = "#f59e0b"

    # Colors — credential types
    CRED_PASSWORD = "#f59e0b"
    CRED_SSH_KEY  = "#8b5cf6"
    CRED_API_KEY  = "#22c55e"
    CRED_QMP_PASS = "#3b82f6"

    # Spacing (4px base unit)
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 24
    XXL = 32

    # Border radii
    R_SM  = 4
    R_MD  = 6
    R_LG  = 8
    R_XL  = 12
    R_FULL = 9999

    # Typography scale
    FS_XS  = 10
    FS_SM  = 11
    FS_MD  = 12
    FS_LG  = 13
    FS_XL  = 14
    FS_XXL = 16

    # Shadows
    SHADOW_SM = "0 1px 3px rgba(0,0,0,0.3)"
    SHADOW_MD = "0 2px 8px rgba(0,0,0,0.4)"
    SHADOW_LG = "0 4px 16px rgba(0,0,0,0.5)"
```

**Rules:**
- One token class per theme. Do NOT scatter hex literals across widget files.
- Name tokens by role, not by hue (e.g. `TEXT_PRIMARY`, not `LIGHT_GRAY`).
- Keep the token class in `theme.py` only — widgets import `T`, they never define tokens.

## QSS Generator Functions

Each widget type gets a module-level function that returns a QSS string built from tokens.

```python
def card_style() -> str:
    return (
        "background: " + T.BG_SECONDARY + ";"
        "border: 1px solid " + T.BG_TERTIARY + ";"
        "border-radius: " + str(T.R_LG) + "px;"
        "box-shadow: " + T.SHADOW_SM + ";"
    )

def button_green_style() -> str:
    return (
        "background: " + T.SUCCESS + ";"
        "color: white;"
        "border: none;"
        "border-radius: " + str(T.R_SM) + "px;"
        "font-size: " + str(T.FS_LG) + "px;"
        "font-weight: 600;"
        "padding: 0 16px;"
        "min-height: 32px;"
        ""
        ":hover { background: #16a34a; }"
        ":disabled {"
        "  background: " + T.SUCCESS + "20;"
        "  color: " + T.TEXT_MUTED + ";"
        "}"
    )
```

**Rules:**
- Each generator is a pure function: same inputs → same QSS string, no side effects.
- Use string concatenation (`"background: " + T.BG_SECONDARY + ";"`) rather than f-strings
  when the line has no embedded expressions — it is more readable for long QSS blocks.
- When an f-string is needed (e.g. a widget-specific color passed in), double ALL literal
  CSS braces: `f"QPushButton:hover {{ background: {color}; }}"`.
- One generator per widget role, not per widget instance. Do NOT create a new function for
each panel's variant of the same widget type.

## Palette Function

```python
from PyQt5.QtGui import QColor, QPalette

def dark_palette() -> QPalette:
    p = QPalette()
    p.setColor(QPalette.Window, QColor(T.BG_PRIMARY))
    p.setColor(QPalette.WindowText, QColor(T.TEXT_PRIMARY))
    p.setColor(QPalette.Base, QColor(T.BG_PRIMARY))
    p.setColor(QPalette.AlternateBase, QColor(T.BG_SECONDARY))
    p.setColor(QPalette.Text, QColor(T.TEXT_PRIMARY))
    p.setColor(QPalette.Button, QColor(T.BG_SECONDARY))
    p.setColor(QPalette.ButtonText, QColor(T.TEXT_PRIMARY))
    p.setColor(QPalette.BrightText, QColor(T.ERROR))
    p.setColor(QPalette.Link, QColor(T.BRAND))
    p.setColor(QPalette.Highlight, QColor(T.BRAND))
    p.setColor(QPalette.HighlightedText, QColor(T.BG_PRIMARY))
    return p
```

Apply in the app entry point BEFORE showing any window:
```python
app = QApplication(sys.argv)
app.setStyle("Fusion")
app.setPalette(dark_palette())
```

## Widget Integration

Every widget in `widgets.py` imports tokens and generators from `theme.py`:

```python
from gui.theme import T, dark_palette, card_style, card_title_style, \
    primary_label_style, secondary_label_style, muted_label_style, \
    input_style, button_green_style, button_blue_style, button_ghost_style, \
    button_bordered_style, lifecycle_btn_style, sidebar_btn_style, \
    status_bar_style, tab_bar_style, tree_style, list_style, progress_style, \
    combo_style, spinbox_style, checkbox_style, text_browser_style, \
    dialog_style, splitter_style, title_bar_style, sidebar_style, panel_bg_style
```

Widget constructors use the generators directly:

```python
class Card(QFrame):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet(card_style())          # ← generator, not inline QSS
        ...
        if title:
            self.title_label = QLabel(title)
            self.title_label.setStyleSheet(card_title_style())
```

**Rules:**
- Widgets call the generator function at construction time and pass the result to
  `setStyleSheet()`. Do NOT store the QSS string as a class attribute.
- When a widget needs a per-instance color (e.g. a lifecycle button with a custom color),
  write a generator that takes the color as a parameter: `lifecycle_btn_style(color)`.
- Do NOT inline QSS strings in widget code. If you find yourself writing
  `"background: #0f172a;"` inside a widget file, stop — add a token or generator instead.

## New Widgets Added by This Pattern

Beyond the standard set, the token system makes it cheap to add small reusable
composite widgets:

| Widget | Purpose |
|--------|---------|
| `Toast` | Auto-dismissing notification with icon (success/warning/error/info) |
| `StatCard` | Compact label + value + optional trend indicator |
| `SectionHeader` | Panel section divider with title and optional subtitle |
| `Badge` | Small colored pill for status/category labels |
| `Timeline` | Vertical event timeline with colored dots |
| `ProgressBar` | Thin themed progress bar wrapped around QProgressBar |

## Pitfalls

### f-string CSS brace doubling

When building QSS inside an f-string, every literal `{` and `}` in the CSS must be
doubled. An unescaped `{` in an f-string starts an expression and produces a syntax
error or, worse, a wrong stylesheet.

```python
# WRONG — unescaped braces in f-string
f"IconButton:hover { background: {T.BG_TERTIARY}; }"

# RIGHT — doubled braces for literal CSS, single braces for tokens
f"IconButton:hover {{ background: {T.BG_TERTIARY}; }}"
```

Prefer string concatenation for QSS blocks that have no embedded expressions — it
avoids the brace-doubling tax entirely and is easier to read.

### Module docstring triple-quote closure

A module-level docstring that starts with `"""` on line 1 MUST have its closing
`"""` appear before the next `from __future__ import` or any other code. If the
closing `"""` is missing or sits on the same line as a `"""` that opens the next
docstring (e.g. a class docstring), Python absorbs the class docstring into the
module docstring and the class body becomes part of the string — producing cascading
syntax errors far from the real cause.

```python
# RIGHT
"""Module docstring."""
from __future__ import annotations

class Foo:
    """Class docstring."""
```

```python
# WRONG — class docstring absorbed into module docstring
"""Module docstring.

class Foo:
    """Class docstring."""
```

The fix is always to ensure the module docstring closes on its own line before any
code, including the next docstring opener.

### Import shape between theme and widgets

When `theme.py` exports token class `T` and generator functions, `widgets.py` must
import them explicitly:

```python
from gui.theme import T, card_style, button_green_style, ...
```

Do NOT write `from gui.theme import theme` expecting a `theme` object — the token
pattern does not create one unless you explicitly build it. If existing code references
`theme.xxx`, either add a module-level alias (`theme = T` is wrong; build a thin
namespace object if you must) or update the call sites.

### Backward compatibility when replacing widgets

When a `widgets.py` module is rewritten with new classes or signature changes, audit
every `from gui.widgets import ...` across the panel files before committing. New
classes (Toast, StatCard, etc.) are safe to add. Existing classes whose __init__
signatures change (parameter names, positional order, default values) will break
panel constructors and test instantiation. Run the GUI test suite after any widget
change: `pytest tests/test_gui.py -q`.

### Token naming consistency

A token referenced in widgets must exist in `T` with the exact name. A misspelling
like `T.STATUS_OFFLINE` when the token is named `T.DOT_OFFLINE` produces an
AttributeError at class-definition time (the default argument is evaluated when the
class body runs, before any instance exists). Always check both sides when a token
error appears: the definition in `theme.py` and the usage in `widgets.py`.
