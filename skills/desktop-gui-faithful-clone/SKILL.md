---
name: "desktop-gui-faithful-clone"
title: "Desktop GUI Faithful Clone"
description: "Clone Tauri GUI into PyQt6 with exact fidelity."
triggers:
  - "make Python desktop GUI look exactly like rust/tamarin gui"
  - "clone a reference desktop app into PyQt6"
  - "work from X: drive"
  - "no backend/offline wording in GUI status"
---

# Desktop GUI Faithful Clone

## Trigger

Use when the user asks to make a Python desktop GUI (PyQt6/Tkinter) look **exactly** like an existing Rust/Tauri GUI, or clone a reference desktop app's layout, theme, colors, and navigation into a native Python window. Also use when working from the `X:` drive, or when a `frontend/static/js/app.js` and `backend/api/server.py` pair must stay product-rule compliant (no "backend"/"offline" wording in on-screen status text).

## Product Rule — Neutral Status UI (apply to every change)

GUI status pills, labels, tabs, and any on-screen status text must **never** contain the words `backend`, `Backend`, `offline`, `Offline`, `backend-ready`, `backend-status`, or any engine word. Use neutral, self-referential labels only:

| Status | Use |
|---|---|
| Start | `Starting...` |
| Running | `Ready` |
| Degraded | `Not ready` |
| Error | `Not ready` |

Never render `backend`, `Backend`, `backend offline`, `backend ready`, `backend PID`, `backend-status`, or any engine word in the GUI. This rule applies to the PyQt6 `QLabel` pill, status bar, log panel, toasts, and chart titles. The Rust sidecar may still emit raw events; the UI layer owns the neutralization.

### Pin the wording in the source

- PyQt6 text strings (pill, title bar, log) must be fixed literals, not interpolated from engine internals.
- Grep for `backend`, `Backend`, `offline`, `Offline` (case-insensitive) and remove every match from visible text.
- If the word appears only in code comments or internal state, that is acceptable.

## Workflow: Clone a Rust/Tauri GUI into a Python app

1. **Read the reference first.** Open `frontend/static/js/app.js` and `src-tauri/src/main.rs` (or equivalent) to capture the design system: window size, dark theme, sidebar, stat cards, charts, tabs/panels, nav items, and status pill text.
2. **Build the dark theme** in the Python GUI before any layout code. Use a `QPalette` with `#0f172a` (background), `#1e293b` (surface), `#334155` (border), `#94a3b8` (text), `#38bdf8` (accent/dot), `#34d399` (ready/green), `#f87171` (error/red). Do not skip the theme — a Python GUI with the browser CSS will look different.
3. **Match the layout hierarchy:** sidebar (left, dock) + main content (right). Inside main content, match the reference's page structure (metrics row → charts → tabs/Panels). Replace any tabs with sidebar `QAction` items if the reference shows sidebar navigation with no tabs.
4. **Clone the nav items** exactly: Dashboard, Fans, Curves, Sensors, Settings, Diagnostics. Each nav action must call `_nav_to(page)` and set the requested page `setVisible(True)` while the others are `setVisible(False)`.
5. **Build the pages** (`_build_dashboard`, `_build_fans_tab`, `_build_curves_tab`, `_build_sensors_tab`, `_build_settings_tab`, `_build_diagnostics_tab`) and return the `QWidget` page. Store each page on `self` (e.g. `self.dashboard_page = ...`).
6. **Apply the theme** to all widgets (buttons, labels, charts, charts axes) so no widget inherits a light browser color.
7. **Verify before removal.** After the Python GUI visually matches the reference, only then may the original Rust/Tauri code and web frontend be removed. Do not remove the reference implementation until the clone is verified.
8. **Run the product rule check** (see below).

## Backend Gap-Analysis Fixes (verify each before claiming done)

A backend change is not done until you have run the check for each item. These are the common gaps in this class of app:

1. **CUBIC curve interpolation** — the cubic (smoothstep) curve must use a proper Catmull-Rom/smoothstep: `ease = t^3 * (t^2 * (6t - 15) + 10)` and clamp the fraction to `[0,1]` before computing. Verify with a test that low/high temps return the exact control-point speeds.
2. **Monotonic event counters** — every `EventBus.emit()` call must atomically increment `_total_events` and `_counters[event_type]` (and any type-specific counters). Verify with a test that emits a known number of events and reads back the exact count.
3. **Curve-bounds clamping** — `CurveEngine.interpolate` must clamp `fraction` to `[0,1]` and handle out-of-range temps (below first point → return first speed; above last point → return last speed).
4. **Full `/tools/*` REST proxy** — the FastAPI server must expose `POST /tools/{tool_name}` and handle every tool name the Rust frontend invokes (`list_sensors`, `list_fans`, `set_fan_speed`, `set_fan_mode`, `list_curves`, `create_curve`, `reload_config`, `reload_plugins`, `reload_profiles`, `emergency_stop`, `health_check`). Each handler must route to the correct backend module using the existing `API` instance state, not lazy-import another module.
5. **Canonical `/settings` endpoints** — expose `GET /settings` (return merged config) and `POST /settings` (call `CONFIG.merge(payload)` then `CONFIG.save()` and emit `settings.updated`). Verify the merge preserves untouched sections.
6. **`CONFIG.merge`** — the `Config` class must have a `merge(data)` method that updates only the supplied keys (`server`, `polling`, `safety`, `enabled_plugins`, `groups`) and preserves every other section. Verify with a test that merges a partial payload and reads back the untouched keys.

### Verification commands (run these after any change)

- `python -c "import ast; ast.parse(open('backend/api/server.py').read()); print('Syntax OK')"`
- `python -m pytest tests/ -q --tb=short` (or the project test command)
- Start the server: `python -m uvicorn backend.api.server:fastapi_app --host 127.0.0.1 --port 8080`
- Probe `/health` and `/settings` with `curl`; confirm the product-rule wording does not appear in any visible UI text.
- Run the GUI headless driver: `python use_gui_driver.py` (canonical headless check).

## Verification Checklist

Run these before claiming completion:
1. GUI syntax: `python -m py_compile gui_app.py`
2. GUI dark theme: grep for `#0f172a`, `#1e293b`, `#334155`, `#38bdf8`, `#34d399`, `#f87171` in gui_app.py
3. Product rule: grep for `backend`, `offline` (case-insensitive) in gui_app.py visible text — must be zero matches
4. Layout: sidebar + main content + pages (no tabs) — visually diff against reference
5. Nav switching: click each nav item and confirm the correct page is `setVisible(True)`
6. Backend: `python -m uvicorn backend.api.server:fastapi_app --host 127.0.0.1 --port 8080` and probe `/health`, `/settings`, `/tools/*`
7. Headless driver: `python use_gui_driver.py` exits 0
8. Backend gap-analysis fixes: run the six checks above

## Pitfalls

- **PyQt6.QtCharts module is missing.** The `PyQt6.QtCharts` module is NOT installed in the fan-controller venv (package `PyQt6 6.11.0` is present, but no `QtCharts` submodule). Do not import it. Replace `QChart`, `QChartView`, `QLineSeries`, `QValueAxis` with a custom `ChartWidget` class that draws using `QPainter`, `QPen`, and `QBrush`. See the ChartWidget pattern in `references/chart-widget.md` and in `gui_app.py`: store points as a list of `(x, y)` tuples, override `paintEvent`, and use `set_points()` / `add_point()` to feed data.
- **`QAction` has no `setStyleSheet()` in PyQt6.** `QAction` inherits from `QObject`, not `QWidget`, so it cannot be styled with CSS. Wrap each `QAction` in a `QWidget` with a `QHBoxLayout`, call `widget.addAction(act)`, and add the widget to the layout instead.
- **`QAction` cannot be added to a layout directly.** `QVBoxLayout.addWidget(act)` fails for `QAction` because it is not a `QWidget`. Always wrap it first, then add the widget.
- **`setAccessibleName()` does not exist in PyQt6.** Use `setObjectName()` for all widget names (the old-code `setAccessibleName("Nav Dashboard")` → `setObjectName("NavDashboard")`).
- **Verify the GUI actually starts before claiming success.** A `py_compile` pass only checks syntax, not runtime imports. Run the GUI headless: `timeout 10 .venv/Scripts/python.exe gui_app.py 2>&1`. Exit code 124 means it ran 10 seconds and was killed by the timeout (success). Any non-zero exit with a traceback means it crashed. Check for `OSError: only one usage of each socket address` — this means a previous backend server is still holding port 8080; kill it with `taskkill /F /PID <pid>` before launching the GUI.
- **Verify the GUI starts before patching further.** After every chunked `patch` edit, run `python -m py_compile gui_app.py` and then launch the GUI briefly to confirm it starts. Do not add more edits on top of a file that won't import.
- **Dashboard page visibility.** After building all pages, explicitly show the dashboard page and hide all others: `self.dashboard_page.setVisible(True)` followed by `for w in (self.fans_page, self.curves_page, self.sensors_page, self.settings_page, self.diagnostics_page): w.setVisible(False)`. Without this, the main content area shows a blank screen — the page is built but never displayed.
- **Verify PollWorker is actually running and servicing the event loop.** A launched `QThread` may show `isRunning()` as `True` but still not emit signals if the `AsyncRunner`'s event loop is not servicing the callback. Verify by reading back sensors after start: `sensors = self._async_runner.run(self.sensors.read_all())`. If the list is empty, the polling pipeline is not flowing. Verify with `self.poll_worker.isRunning()` and by checking that `_on_readings()` is receiving data within the first few seconds of launch.

## Supported features

- Pure-PyQt6 desktop GUI (no WebView, no browser engine, no HTML/JS frontend, no Rust/Tauri shell) — use only when the user explicitly rejects browser/WebView.
- In-process imports of backend sensor/fan/curve modules (no HTTP sidecar for the Python GUI).
- Custom QPainter line-chart widget (no `PyQt6.QtCharts` — the module is not installed in the venv; see Pitfalls for the replacement pattern). QTableWidget for tables.
- Dark theme via QPalette + custom QSS stylesheets.
- PyInstaller packaging with `console=False`.
- Headless driver for verification without a display.

## Training rules (for the future)

- When the user says "look EXACTLY like the rust one", clone the design FIRST (theme, layout, colors, nav) before writing any code. Do not invent a new layout.
- "Proceed" = implement everything, never stop at a stub. If a step fails, diagnose and fix, do not report "blocked" without evidence.
- Work from the `X:` drive (`RUSTUP_HOME=X:/Dev/rustup`, `CARGO_HOME=X:/Dev/cargo`, `CARGO_TARGET_DIR=X:/cargo-target`, `PATH=/x/Dev/cargo/bin:$PATH`). Never work from `C:` for Rust toolchain commands.
- Never remove a reference implementation until the clone is verified. The reference (Rust/Tauri) is the source of truth for the design.
- The product rule is absolute: no `backend`, no `offline` in any visible GUI text.

A backend change is not done until you have run the check for each item. These are the common gaps in this class of app:

1. **CUBIC curve interpolation** — the cubic (smoothstep) curve must use a proper Catmull-Rom/smoothstep: `ease = t^3 * (t^2 * (6t - 15) + 10)` and clamp the fraction to `[0,1]` before computing. Verify with a test that low/high temps return the exact control-point speeds.
2. **Monotonic event counters** — every `EventBus.emit()` call must atomically increment `_total_events` and `_counters[event_type]` (and any type-specific counters). Verify with a test that emits a known number of events and reads back the exact count.
3. **Curve-bounds clamping** — `CurveEngine.interpolate` must clamp `fraction` to `[0,1]` and handle out-of-range temps (below first point → return first speed; above last point → return last speed).
4. **Full `/tools/*` REST proxy** — the FastAPI server must expose `POST /tools/{tool_name}` and handle every tool name the Rust frontend invokes (`list_sensors`, `list_fans`, `set_fan_speed`, `set_fan_mode`, `list_curves`, `create_curve`, `reload_config`, `reload_plugins`, `reload_profiles`, `emergency_stop`, `health_check`). Each handler must route to the correct backend module using the existing `API` instance state, not lazy-import another module.
5. **Canonical `/settings` endpoints** — expose `GET /settings` (return merged config) and `POST /settings` (call `CONFIG.merge(payload)` then `CONFIG.save()` and emit `settings.updated`). Verify the merge preserves untouched sections.
6. **`CONFIG.merge`** — the `Config` class must have a `merge(data)` method that updates only the supplied keys (`server`, `polling`, `safety`, `enabled_plugins`, `groups`) and preserves every other section. Verify with a test that merges a partial payload and reads back the untouched keys.

### Verification commands (run these after any change)

- `python -c "import ast; ast.parse(open('backend/api/server.py').read()); print('Syntax OK')"`
- `python -m pytest tests/ -q --tb=short` (or the project test command)
- Start the server: `python -m uvicorn backend.api.server:fastapi_app --host 127.0.0.1 --port 8080`
- Probe `/health` and `/settings` with `curl`; confirm the product-rule wording does not appear in any visible UI text.
- Run the GUI headless driver: `python use_gui_driver.py` (canonical headless check).

## Verification Checklist

Run these before claiming completion:
1. GUI syntax: `python -m py_compile gui_app.py`
2. GUI dark theme: grep for `#0f172a`, `#1e293b`, `#334155`, `#38bdf8`, `#34d399`, `#f87171` in gui_app.py
3. Product rule: grep for `backend`, `offline` (case-insensitive) in gui_app.py visible text — must be zero matches
4. Layout: sidebar + main content + pages (no tabs) — visually diff against reference
5. Nav switching: click each nav item and confirm the correct page is `setVisible(True)`
6. Backend: `python -m uvicorn backend.api.server:fastapi_app --host 127.0.0.1 --port 8080` and probe `/health`, `/settings`, `/tools/*`
7. Headless driver: `python use_gui_driver.py` exits 0
8. Backend gap-analysis fixes: run the six checks above

## Pitfalls

- **PyQt6.QtCharts module is missing.** The `PyQt6.QtCharts` module is NOT installed in the fan-controller venv (package `PyQt6 6.11.0` is present, but no `QtCharts` submodule). Do not import it. Replace `QChart`, `QChartView`, `QLineSeries`, `QValueAxis` with a custom `ChartWidget` class that draws using `QPainter`, `QPen`, and `QBrush`. See the ChartWidget pattern in `gui_app.py`: store points as a list of `(x, y)` tuples, override `paintEvent`, and use `set_points()` / `add_point()` to feed data.
- **`QAction` has no `setStyleSheet()` in PyQt6.** `QAction` inherits from `QObject`, not `QWidget`, so it cannot be styled with CSS. Wrap each `QAction` in a `QWidget` with a `QHBoxLayout`, call `widget.addAction(act)`, and add the widget to the layout instead.
- **`QAction` cannot be added to a layout directly.** `QVBoxLayout.addWidget(act)` fails for `QAction` because it is not a `QWidget`. Always wrap it first, then add the widget.
- **`setAccessibleName()` does not exist in PyQt6.** Use `setObjectName()` for all widget names (the old-code `setAccessibleName("Nav Dashboard")` → `setObjectName("NavDashboard")`).
- **Verify the GUI actually starts before claiming success.** A `py_compile` pass only checks syntax, not runtime imports. Run the GUI headless: `timeout 10 .venv/Scripts/python.exe gui_app.py 2>&1`. Exit code 124 means it ran 10 seconds and was killed by the timeout (success). Any non-zero exit with a traceback means it crashed. Check for `OSError: only one usage of each socket address` — this means a previous backend server is still holding port 8080; kill it with `taskkill /F /PID <pid>` before launching the GUI.
- **Verify the GUI starts before patching further.** After every chunked `patch` edit, run `python -m py_compile gui_app.py` and then launch the GUI briefly to confirm it starts. Do not add more edits on top of a file that won't import.
- **Dashboard page visibility.** After building all pages, explicitly show the dashboard page and hide all others: `self.dashboard_page.setVisible(True)` followed by `for w in (self.fans_page, self.curves_page, self.sensors_page, self.settings_page, self.diagnostics_page): w.setVisible(False)`. Without this, the main content area shows a blank screen — the page is built but never displayed.
- **Verify PollWorker is actually running and servicing the event loop.** A launched `QThread` may show `isRunning()` as `True` but still not emit signals if the `AsyncRunner`'s event loop is not servicing the callback. Verify by reading back sensors after start: `sensors = self._async_runner.run(self.sensors.read_all())`. If the list is empty, the polling pipeline is not flowing. Verify with `self.poll_worker.isRunning()` and by checking that `_on_readings()` is receiving data within the first few seconds of launch.

## Supported features

- Pure-PyQt6 desktop GUI (no WebView, no browser engine, no HTML/JS frontend, no Rust/Tauri shell) — use only when the user explicitly rejects browser/WebView.
- In-process imports of backend sensor/fan/curve modules (no HTTP sidecar for the Python GUI).
- Custom QPainter line-chart widget (no `PyQt6.QtCharts` — the module is not installed in the venv; see Pitfalls for the replacement pattern). QTableWidget for tables.
- Dark theme via QPalette + custom QSS stylesheets.
- PyInstaller packaging with `console=False`.
- Headless driver for verification without a display.

## Training rules (for the future)

- When the user says "look EXACTLY like the rust one", clone the design FIRST (theme, layout, colors, nav) before writing any code. Do not invent a new layout.
- "Proceed" = implement everything, never stop at a stub. If a step fails, diagnose and fix, do not report "blocked" without evidence.
- Work from the `X:` drive (`RUSTUP_HOME=X:/Dev/rustup`, `CARGO_HOME=X:/Dev/cargo`, `CARGO_TARGET_DIR=X:/cargo-target`, `PATH=/x/Dev/cargo/bin:$PATH`). Never work from `C:` for Rust toolchain commands.
- Never remove a reference implementation until the clone is verified. The reference (Rust/Tauri) is the source of truth for the design.
- The product rule is absolute: no `backend`, no `offline` in any visible GUI text.
