---
name: service-console-desktop-app
description: "Use when building a desktop GUI that manages a local daemon."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [pyqt5, gui, dashboard, telemetry, monitoring, daemon, service-management, sqlite]
    related_skills: [pyqt5-desktop-dev, hermes-gateway-messaging-operations]
---

# Service console desktop app

A GUI that watches and drives a locally-running background service. The
distinguishing property is not the widgets — it is that the app reads another
live process's state store, controls its lifecycle, and edits its config while
the service keeps running.

`pyqt5-desktop-dev` (user-owned) covers general PyQt5 mechanics. This skill
covers the class of work where the GUI is a *second client* to a running daemon.

## When to use

- "a dashboard/console/GUI for &lt;service&gt;" where the service is already running
  or can be started on demand.
- Telemetry needs to come from the service's own state (SQLite/JSON/logs), not
  from polling its API on every frame.
- The user wants start/stop/restart buttons and a health verdict, not just charts.

## Order of work

1. **Enumerate the real data sources before designing a single widget.** Read the
   schema, not the docs: list the service's tables/columns, its state file, its
   config, and its log files. Most dashboards fail because they were designed
   around an imagined API instead of the store that actually exists.
   ```python
   for n, in conn.execute("select name from sqlite_master where type='table'"):
       cols = [r[1] for r in conn.execute(f"PRAGMA table_info({n})")]
       print(n, conn.execute(f"select count(*) from {n}").fetchone()[0], cols)
   ```
   Print row counts too — a table with 40k rows needs a different query plan
   than one with 4.

2. **Normalise every clock at the boundary.** Services mix epoch seconds,
   epoch milliseconds, monotonic clocks, and ISO strings in one payload, and the
   mismatched ones fail silently rather than raising. Route all of them through
   one guarded helper that rejects implausible values instead of formatting them:
   ```python
   def as_epoch(value):
       try: v = float(value)
       except (TypeError, ValueError): return 0.0
       if v > 1e11: v /= 1000.0          # milliseconds
       return v if 1e9 <= v <= 9.99e9 else 0.0   # reject monotonic/garbage
   ```
   Derive uptime from the OS process (`psutil.Process(pid).create_time()`), not
   from a monotonic start field. Show a dash when a value is unusable — never a
   fabricated number.

3. **Open the state store read-only, per query.** A viewer must never be able to
   lock or corrupt the writer:
   ```python
   conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True, timeout=5)
   ```
   Short-lived connection per query. Build filter clauses from a condition list so
   a source-only filter still emits a valid `WHERE`.

4. **Put every control action on a worker thread.** CLI invocations and HTTP both
   block; the window must never. Give each action a busy flag, disable the button
   row while it runs, and report the result in an on-screen console strip rather
   than a modal dialog. For "restart", re-read state on a delayed timer instead of
   immediately — the new process needs seconds to connect.

5. **Build a diagnostic step chain, not a single boolean.** The most useful
   control-panel widget is a left-to-right strip of individual verdicts (token
   present → API reachable → process alive → transport connected → allowlist →
   default target → starts at login), each rendered from its own cheap check.
   A user can act on "allowlist empty" but not on "unhealthy".

6. **Mask secrets by default, and make destructive edits recoverable.** Show
   `prefix…••••(46 chars)`, keep secret input fields empty on load so saving an
   unrelated field cannot overwrite the value, and take a timestamped backup
   before any config write.

## Verification

Test against the **live** service, headless, with no mocks — that is what caught
every real bug in this class of work. Construct the window, show it, call
`processEvents()`, and assert on rendered values (row counts, badge text, KPI
strings) rather than on "did not crash".

```
set QT_QPA_PLATFORM=offscreen && python -u test_gui.py > out.txt 2>&1
```

`python -u` plus file redirection is mandatory, not stylistic: when the process
aborts mid-paint, buffered or piped output is lost entirely and you cannot tell
how far the run got.

## Pitfalls

- **Custom `paintEvent` must use integer geometry.** A float passed to
  `QPainter.fillRect`/`drawRect` hard-aborts the Qt paint backend on first repaint —
  no traceback, no exception, often no output — so it presents as "the app is
  broken" rather than "this widget is wrong". Accumulate `x = 0` as an int and cast
  widths with `int(round(...))`. Guard the empty-data case too.
- **A widget that never paints in isolation is not verified.** Construction
  succeeding proves nothing; the fault lives in the paint path. See
  [references/offscreen-paint-crash-bisect.md](references/offscreen-paint-crash-bisect.md)
  for the bisect order when `show()` succeeds and `processEvents()` kills the process.
- **matplotlib artists are snake_case while Qt is camelCase, in the same file.**
  `legend_text.setColor(...)` raises `AttributeError`; it is `set_color`. Check the
  artist's API rather than matching the surrounding style.
- **Populate a view before filtering it.** A filter that reads the backing store
  before `load()` assigns it renders zero rows permanently — no error, and it looks
  like an empty data source. `table.load(rows)` first, then apply the filter.
- **Keep `format_duration(seconds)` and `time_ago(epoch)` separate.** One function
  that does both renders a 70-minute uptime as `20730d ago`. Test each against
  `None` and `0`.
- **Stale state files outlive their process.** A status file written by a separate
  writer can report "connected" long after the owning process died. Always
  cross-check PID liveness before presenting state as current.
- **Verify the render, not just the data.** Colour-sample the actual
  `widget.grab()` pixels (or the AX tree of the live window) to prove charts drew
  ink. Populated model objects still paint blank when layout collapses.
