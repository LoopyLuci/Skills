# Snap-In/Snap-Out Pattern — Full Implementation Reference

Complete reference for snapping Chat and Properties windows into and out of the main WebBuilder window.

## State Variables (both ChatWindow and PropertiesWindow)

```python
self._is_snapped: bool = False
self._dock_widget: Optional[QDockWidget] = None  # ChatDockWidget or PropertiesDockWidget
self._main_window_ref: Optional[QMainWindow] = None
```

## Shortcuts

| Shortcut | Scope | Action |
|----------|-------|--------|
| `Ctrl+Alt+C` | Main window | Open Chat window |
| `Ctrl+Alt+P` | Main window | Open Properties window |
| `Ctrl+Alt+S` | Floating window (Chat or Properties) | Toggle snap in/out |

## Toolbar Snap Button

Both windows get a toolbar button reflecting current state. Call `_update_snap_button()` at the end of `_toggle_snap()`, `_snap_to_main()`, and `_unsnap_from_main()`:

```python
self.snap_btn = QPushButton("📌 Snap to Main")
self.snap_btn.clicked.connect(self._toggle_snap)
toolbar.addWidget(self.snap_btn)

def _update_snap_button(self):
    if self._is_snapped:
        self.snap_btn.setText("📌 Unsnap from Main")
        self.snap_btn.setStyleSheet("background: #10b981; color: white; border: none; border-radius: 4px; padding: 4px 12px; font-size: 12px;")
    else:
        self.snap_btn.setText("📌 Snap to Main")
        self.snap_btn.setStyleSheet("background: #334155; color: #e2e8f0; border: none; border-radius: 4px; padding: 4px 12px; font-size: 12px;")
```

## _snap_to_main()

Walk parent chain to find QMainWindow, create dock wrapper, transfer central widget into it, add to main window:

```python
def _snap_to_main(self):
    window = self
    while window and not hasattr(window, 'addDockWidget'):
        window = window.parent()
    if not window:
        logger.debug("Cannot snap: no main window found")
        return

    if not self._dock_widget:
        self._dock_widget = ChatDockWidget(window)  # or PropertiesDockWidget(window)
        self._dock_widget.chat_window = self  # or .properties_widget = self.properties_widget
        central = self.centralWidget()
        self._dock_widget.setWidget(central)

    self._dock_widget.setFeatures(
        QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable
    )
    self._dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
    window.addDockWidget(Qt.RightDockWidgetArea, self._dock_widget)
    self._is_snapped = True
```

## _unsnap_from_main()

```python
def _unsnap_from_main(self):
    if self._dock_widget:
        window = self
        while window and not hasattr(window, 'removeDockWidget'):
            window = window.parent()
        if window:
            window.removeDockWidget(self._dock_widget)
        self._dock_widget.setParent(None)
        self._dock_widget = None
        self._is_snapped = False
        self.show()
        self.raise_()
        self.activateWindow()
```

## Main Window Handlers

```python
def handle_chat_snap_request(self, chat_window, snap: bool | None = None):
    from webbuilder.gui.chat_window import ChatDockWidget
    if snap is None:
        snap = not chat_window._is_snapped
    if snap:
        if not chat_window._chat_dock:
            chat_window._chat_dock = ChatDockWidget(self)
            chat_window._chat_dock.chat_window = chat_window
            central = chat_window.centralWidget()
            if central:
                chat_window._chat_dock.setWidget(central)
        chat_window._chat_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)
        chat_window._chat_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, chat_window._chat_dock)
        chat_window._is_snapped = True
    else:
        if chat_window._chat_dock:
            self.removeDockWidget(chat_window._chat_dock)
            chat_window._chat_dock.setParent(None)
            chat_window._chat_dock = None
            chat_window._is_snapped = False
            chat_window.show()
            chat_window.raise_()
            chat_window.activateWindow()
```

Properties handler is structurally identical using `PropertiesDockWidget`.

## Common Pitfalls

1. **Stale button state**: Forgetting `_update_snap_button()` after state changes leaves the toolbar button showing wrong label/color. Always update at the end of every state-changing method.
2. **Losing dock reference**: Not storing `_dock_widget` as instance variable causes unsnap to find `None` — either fails silently or creates a duplicate dock.
3. **Parent chain breakage**: Floating window created with `parent=None` cannot walk to `QMainWindow`. Ensure `get_chat_window(self)` passes the main window as parent.
4. **Central widget transfer**: Must use `self.centralWidget()` and `dock.setWidget(central)` — creating a new widget loses all chat/properties state.
5. **removeDockWidget without `setParent(None)`**: Dock retains reference preventing cleanup; always call `dock.setParent(None)` after removing.
6. **Singleton factory drops on rewrite**: Rewriting the tail of `chat_window.py` must preserve `get_chat_window()` and the `_chat_window` global singleton — dropping them causes `ImportError: cannot import name 'get_chat_window'` in any test or call site that imports it. Always grep for `def get_` and the singleton name before and after a rewrite, and run `py_compile` on all three GUI files before rebuilding.
7. **SnapState centralized management**: Use `SnapState` class in `snap_system.py` for centralized snap state management. Both `ChatWindow` and `PropertiesWindow` use `_snap_state` instead of `_is_snapped`. Main window delegates snap/unsnap to `SnapState`. This avoids stale `_is_snapped` attributes and ensures state synchronization between windows.
