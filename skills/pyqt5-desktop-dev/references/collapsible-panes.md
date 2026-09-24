# Collapsible Pane System

## CollapsiblePane (QWidget)

A widget with a header (title + toggle button) and collapsible content area.

### Layout
```
┌─────────────────────────────────┐
│ [◀] Title              [Actions] │  ← Header (_header_height=36)
├─────────────────────────────────┤
│                                 │
│         Content Area            │  ← Content (hidden when collapsed)
│                                 │
└─────────────────────────────────┘
```

### API

```python
pane = CollapsiblePane(title="Sections")
pane.set_content_widget(widget)           # Set content
pane.set_expanded_width(300)               # Normal width
pane.set_collapsed_width(40)               # Width when collapsed
pane.toggle()                              # Toggle collapse/expand
pane.collapse()
pane.expand()
pane.is_expanded() -> bool
pane.add_action("+", callback)             # Add button to header
pane.get_content_layout() -> QVBoxLayout   # Access content layout

pane.state_changed.connect(on_state_changed)  # Signal: bool (expanded)
```

### Behavior

- Collapsed: content hidden, width = `_collapse_width` (40px), toggle shows ▶
- Expanded: content visible, width = `_expanded_width` (300px), toggle shows ◀
- Header always visible
- No animation (instant show/hide)

## PaneContainer (QSplitter)

Manages multiple `CollapsiblePane` widgets with size redistribution.

```python
container = PaneContainer(orientation=Qt.Horizontal)
container.add_pane(pane1, stretch=1)
container.add_pane(pane2, stretch=2)
container.save_state() -> dict
container.restore_state(state: dict)
```

## Pitfall: Qt Widget Verification

When verifying GUI state via `computer_use`:
- `capture(mode='som', pid=<pid>, window_id=<window_id>)` — needs BOTH
- Element bounds are in native desktop coordinates (~1.97x screenshot pixels)
- Click by element index with `delivery_mode='background'`
- `list_windows()` returns current PIDs and window IDs — re-capture after changes
