# Panel State Persistence & Crash Recovery

## StateManager

Saves and restores window/panel states to survive crashes.

```python
from webbuilder.gui.state_manager import get_state_manager

sm = get_state_manager()

# Save state
sm.save_state(window, project_path="my_project.webbuilder")

# Restore state
sm.restore_state(window)

# Schedule periodic save
sm.schedule_save(window, interval_ms=5000)

# Get recovery points
points = sm.get_recovery_points()
```

## WindowState / PanelState

Dataclasses for serialization:

```python
@dataclass
class PanelState:
    name: str
    visible: bool
    geometry: dict  # {x, y, width, height}
    data: dict      # Custom panel data

@dataclass
class WindowState:
    geometry: dict
    window_state: str  # hex-encoded QMainWindow.saveState()
    active_tab: int
    panels: list[PanelState]
    project_path: str
    timestamp: str
```

## AutoSaveManager

Periodic auto-save with dirty tracking.

```python
from webbuilder.gui.state_manager import AutoSaveManager

manager = AutoSaveManager(
    save_callback=lambda: print("Saving..."),
    interval_ms=30000,
)
manager.start()
manager.mark_dirty()  # Mark as needing save
manager.force_save()   # Save immediately
```

## Pitfall: Qt saveState() Returns Bytes

`QMainWindow.saveState()` returns `QByteArray`. Serialize to hex for JSON:
```python
bytes(window.saveState()).hex()  # Save
window.restoreState(bytes.fromhex(hex_string))  # Restore
```

## Backup Rotation

StateManager automatically keeps the last N backups (default 10). Backups are timestamped: `state_20260915_124549.json`.