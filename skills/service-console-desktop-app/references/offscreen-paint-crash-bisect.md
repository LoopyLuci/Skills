# Bisecting an offscreen paint crash

Signature: the app constructs, `show()` returns, and the first `processEvents()`
kills the process with **no traceback, no exception, and often no output**. Exit
status alone is misleading — a Python hard abort surfaces as a shell status that
looks like "command not found", so do not read it as a missing binary.

`QT_QPA_PLATFORM=offscreen` reproduces it reliably. Software rendering
(`QT_OPENGL=software`, `QT_OPENGL_TYPE=software`) removes GPU drivers as a
variable.

## Always run probes this way

```
QT_QPA_PLATFORM=offscreen python -u probe.py > probe.txt 2>&1; echo "exit=$?"; cat probe.txt
```

`-u` unbuffers and the redirect survives the abort. Without both, output written
before the crash is lost and you cannot tell which step failed.

## Bisect order

1. **One panel at a time** in a bare window. This localises the fault to a panel
   in a single run per panel:
   ```python
   win = QMainWindow(); win.setCentralWidget(SomePanel(paths, telemetry))
   win.resize(1440, 940); win.show(); app.processEvents(); print('OK', flush=True)
   ```
   If every panel passes alone, the fault is in the shell (sidebar, menus,
   status bar) or in interaction between panels.

2. **Hide children one at a time** inside the failing panel, calling
   `processEvents()` after each. `widget.hide()` before the window is shown is
   cheapest and usually sufficient.

3. **All children together at real window size.** If they pass individually but
   fail as a group, the fault is count- or size-dependent (canvas allocation,
   layout collapse), not per-widget.

4. **Reduce to a ~30-line standalone script** that builds only the suspect
   widget. Confirm the fix there before touching the app — this is where the
   real cause becomes visible, because the surrounding shell is gone.

## Frequent causes found this way

| Cause | Mechanism | Fix |
|---|---|---|
| Float geometry in `paintEvent` | `QPainter.fillRect` takes ints; a float aborts the paint backend with no Python-level error | accumulate `x = 0` as int, `int(round(w * ratio))` |
| Unpopulated custom widget painting | division by zero inside `paintEvent` | early-return on empty data |
| matplotlib `tight_layout` vs external legend | axes collapse to zero size, canvas paints nothing | reserve margin with `ax.set_position(...)`, or `constrained` alone |
| Wrong backend import | `backend_qt` gone since matplotlib 3.8 | `matplotlib.backends.backend_qtagg` → `FigureCanvasQtAgg` |

## Confirming the fix

Do not stop at "the probe survived". Re-render and prove ink exists:

```python
img = win.grab().toImage()
img.pixelColor(x, y).name()          # or count pixels matching a series colour
```

Data populated in the model still paints blank when layout collapses, so a pixel
check or an AX-tree read of the live window is the only real proof of rendering.
