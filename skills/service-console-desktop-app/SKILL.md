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

4b. **Hold every moved worker in an attribute.** `moveToThread()` transfers C++
   ownership to the thread, but Python still owns the wrapper. If the only
   reference is a local variable the wrapper is collected before the thread runs
   it, so `run()` never fires and the result callback is silently never called —
   no exception, no traceback, and `thread.isRunning()` still True. Store both
   halves and clear both on completion:
   ```python
   self._thread, self._worker = thread, worker   # worker MUST be an attribute
   ```
   Confirm by printing as the first line of `run()`: if the print never appears it
   is collection, not signal wiring. This is distinct from preferring
   `threading.Thread` for asyncio bridges — it bites plain `QObject` workers too.

5. **Time every query before wiring it into a refresh.** A full-scan integrity
   check (`PRAGMA quick_check` is ~5s on a 500 MB store) or a dozen sequential
   queries inside a timer handler freezes the window for the whole duration, on
   every tick. Measure each in isolation, then:
   - batch the dashboard's queries into ONE `snapshot()` method sharing a single
     connection, executed on a worker;
   - give genuinely slow one-offs their own worker, then cache the result and
     share it with other panels instead of recomputing per view;
   - lengthen the poll interval once the payload is no longer a cheap file read.
   Keep a `blocking=True` path on the refresh method so headless tests stay
   deterministic, and give tests a `pump(app, predicate)` helper that spins the
   event loop until async results land.

6. **Build a diagnostic step chain, not a single boolean.** The most useful
   control-panel widget is a left-to-right strip of individual verdicts (token
   present → API reachable → process alive → transport connected → allowlist →
   default target → starts at login), each rendered from its own cheap check.
   A user can act on "allowlist empty" but not on "unhealthy".

7. **Mask secrets by default, and make destructive edits recoverable.** Show
   `prefix…••••(46 chars)`, keep secret input fields empty on load so saving an
   unrelated field cannot overwrite the value, and take a timestamped backup
   before any config write.

8. **Use the store's full-text index; never `LIKE` over a big table.** If the
   service maintains an FTS index (check `sqlite_master` for an `*_fts` table),
   prefer `MATCH` with `bm25()` ranking — typically 10ms vs 400ms on a 100k-row
   table, and it finds strictly more matches. Two mandatory guards:
   - Quote every user token into the MATCH expression (`"tok1" AND "tok2"`);
     raw input makes `"`, `-`, `*`, `(` syntax errors because they are FTS
     operators. Strip them from each token, and fall back to `LIKE` on
     `sqlite3.Error` rather than surfacing the failure.
   - Filter out rows the store itself has superseded. Compaction-style tables
     carry `active`/`compacted` flags; without them a feed shows the same turn
     twice and empty bodies render as blank rows.

9. **Never render a nested config value raw.** Schedules, intervals, and
   conditions are stored as nested dicts, so `str(schedule)` puts a Python repr in
   a table cell. Write one formatter per shape and fall back to a dash for
   anything unrecognised, so a new schema never leaks internals into the UI.
   Check the real stored shape before assuming flat keys:
   ```python
   print(sorted(read_jobs(path)[0].keys()))          # schedule is often a dict
   ```
   Surface the fields operators act on (`enabled`, `state`, `last_status`,
   `failure_streak`, `next_run_at`) alongside the human label.

10. **Exports must honour the active filter.** Build CSV from the rows the table
   is currently showing, not the unfiltered backing store — track the rendered
   set explicitly, because indexing into the full list drifts once a filter is
   active. Write `utf-8-sig` so Excel reads non-ASCII content correctly.

11. **Type-check every field you read from a file another process writes.** A
   status file is written concurrently and can be truncated mid-write,
   hand-edited, or hold any JSON value, so `data.get(...)` on a list or a
   `"pid": "notanint"` raises `AttributeError`/`TypeError` and takes the window
   down on the next refresh. Check the container is a mapping, then each field's
   type, and degrade to "unknown" instead. Probe it deliberately rather than
   assuming — see
   [references/malformed-state-hardening.md](references/malformed-state-hardening.md).

12. **Say what is missing, and never show a bare empty grid.** When a required
   setting is absent, put a banner above the panels naming exactly which one and
   where to set it, and hide it once configured — the empty-tables-no-explanation
   state is the worst first impression a console can give. Give every table an
   explicit placeholder row when it has nothing to show; an empty `QTableWidget`
   reads as a crash. Flag the placeholder (a custom item-data role) so it is
   excluded from exports and row counts.

13. **Persist the window and the filters.** Save geometry, active panel, and each
   panel's own filters via `QSettings`, restore them on launch, and offer a reset
   action — a monitoring tool that forgets its size and scope every launch is
   tedious to live with. Wrap reads so a corrupt value falls back to its default
   instead of raising at construction time.

## Always-on rules

- This user's expectation for a console like this is a **measured audit pass, not
  a green test run**. "It works" is the starting line. Once the happy path passes,
  go looking for the next class of defect deliberately: time every query, feed
  the readers deliberately malformed input, uncheck every filter, empty every
  table, point the app at a missing install, and reopen it to check what persisted.
  Report what you measured, not that it "seems solid".

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
- **Surface health on the dashboard, not only in the logs.** If the service has
  no error-rate metric, derive one from the log tail (counts per level, error
  rate, latest offenders) and show it as a card. A user should not have to know
  which panel holds the failures.
- **QListWidget/EchoMode constant names drop the suffix.** `QLineEdit.Password`,
  not `QLineEdit.PasswordEchoMode`. When the constant sits far from its use site,
  alias the class import (`from PyQt5.QtWidgets import QLineEdit as _QLineEdit`)
  so the instance attribute still resolves.
- **Clipboard access needs `QApplication` imported in that module** —
  `QApplication.clipboard()` raises `NameError` when the module imported only
  specific widgets.
- **An empty filter set means "match nothing", not "ignore the filter".** Writing
  `if not levels or e.level in levels` makes unchecking every checkbox show every
  row — the exact opposite of the request, and it looks correct until a user tries
  it. Match on membership alone.
- **A new side effect added to a method with early returns may never run.** A
  first-run "what's missing" banner placed after a `return` never appeared on the
  missing-install path — the one case it exists for. After adding work to a
  refresh method, walk each early return and confirm it also performs the update.
- **A placeholder row will leak into exports and counts** unless it is flagged
  and excluded; an exported CSV that starts with "No rows match the current
  filters." is a data file full of UI text.
- **`isVisible()` is False on a widget that was never shown**, so an offscreen
  test asserting a banner appears fails for a reason unrelated to the banner.
  `show()` the widget (or assert on the state you set) before testing visibility.
- **Rendering a chart into a fixed-position axes box is not enough** — a donut
  with an external legend needs the axes box shrunk (`set_position`) rather than a
  `tight_layout` that fights the reserved margin; otherwise layout collapses to
  zero and matplotlib warns instead of drawing.

## References

- [references/exit-diag-interpretation.md](references/exit-diag-interpretation.md) — verdict classes for the gateway exit-diag log, attribution rules, supervisor gap explanation.
- [references/hot-backup-pattern.md](references/hot-backup-pattern.md) — SQLite native `backup()` verification, rotation, restoration via rollback.
- [references/isolation-pattern.md](references/isolation-pattern.md) — stripping Hermes PYTHONPATH and live `sys.path` from project entry points; preventing silent import contamination.
- [references/exit-diag-parsing.md](references/exit-diag-parsing.md) — `gateway.previous_unclean_exit` attribution (index by `prior_pid`, let a process's own exit record outrank an observer), verdict mapping for the exit-diag log.
- Module: `hermes_manager/watchdog.py` — background gateway watchdog (`Watchdog.start()` / `.stop()`), 60-second tick, respects `watchdog.pause`, logs to `watchdog.log`.
