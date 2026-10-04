# Hardening reads of files another process writes

A console reads its daemon's state file, config, and job store while the daemon
is running. Any of those can be truncated mid-write, hand-edited, or replaced
outright, so the reader must assume every field is the wrong type.

The failure is silent until it isn't: `.get()` on a list raises `AttributeError`
inside a timer callback, and the window dies on the next tick with no traceback
the user can act on.

## Probe before you trust

Generate the shapes, don't reason about them. Ten lines finds more than an hour
of guessing:

```python
import tempfile, pathlib
from myapp.data import read_state
from myapp.paths import Paths

d = pathlib.Path(tempfile.mkdtemp())
bodies = [
    "{not json",                                   # truncated write
    "",                                            # empty file
    "[1, 2, 3]", "null", "42", '"hello"',          # valid JSON, wrong shape
    '{"platforms": null}',                         # right shape, null container
    '{"platforms": {"telegram": null}}',           # null child
    '{"pid": "notanint", "start_time": "abc"}',    # wrong scalar types
]
crashes = []
for body in bodies:
    (d / "state.json").write_text(body, encoding="utf-8")
    try:
        read_state(Paths(d))
    except Exception as exc:
        crashes.append(f"{body[:24]}: {type(exc).__name__}")
print(crashes)          # target: []
```

Do the same for every sibling file the app parses (job store, channel
directory). Assert `crashes == []` in the test suite — the count is the metric.

## Check the container, then each field

The order matters: a type error on the container makes field access meaningless.

```python
def read_state(paths):
    p = paths.state_file
    if not p.exists():
        return State(present=False)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return State(present=False)
    # Any JSON value can be stored, not just an object.
    if not isinstance(data, dict):
        return State(present=False)

    pid = data.get("pid")
    if not isinstance(pid, int):
        pid = None                      # a string PID is not a PID

    platforms = data.get("platforms")
    plats = [
        Platform(name, info.get("state", "unknown"))
        for name, info in (platforms if isinstance(platforms, dict) else {}).items()
        if isinstance(info, dict)       # skip null children rather than crash
    ]
    ...
```

Apply the same shape to list-shaped files: a job store can be a dict of jobs, a
list of jobs, or one scalar.

```python
jobs = data.get("jobs", data) if isinstance(data, dict) else data
if isinstance(jobs, dict):
    return [{"id": k, **(v if isinstance(v, dict) else {})} for k, v in jobs.items()]
if not isinstance(jobs, list):
    return []
return [j for j in jobs if isinstance(j, dict)]
```

## Degrade, never fabricate

An unusable field renders as an explicit dash or "unknown", not a plausible
number. A dash reads as "the service did not tell us"; a fabricated 55-year
uptime reads as a data bug the user will try to chase.

## Point the whole app at a missing install

The empty-directory case exercises different branches than malformed content and
is what a first-time user actually sees:

```python
missing = Paths(pathlib.Path(tempfile.mkdtemp()))
assert missing.exists() is False
snap = Telemetry(missing).snapshot()
assert snap["error"]                  # an explicit error, not an exception
assert Telemetry(missing).totals()["sessions"] == 0
panel = DashboardPanel(missing, Telemetry(missing))
panel.show(); panel.refresh()         # show() before asserting isVisible()
```

Every panel must construct and render against that path. If any of them raises,
the first-run experience is a crash instead of the guided setup state.
