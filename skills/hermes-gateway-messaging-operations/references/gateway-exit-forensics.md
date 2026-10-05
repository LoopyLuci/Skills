# Gateway exit forensics — reading `logs/gateway-exit-diag.log`

`gateway_state.json` answers *whether* the gateway is running. It never answers
*why it stopped*. The why lives in `logs/gateway-exit-diag.log`, a JSON-lines
file the gateway appends to at every lifecycle boundary. When the gateway is
down, read this file before theorising — the verdict is almost always written
down explicitly.

## Why a stopped gateway is usually NOT a gateway bug

The single most common confusing symptom: `hermes gateway status` reports a
previous start "reported success, but the process died without a clean shutdown
record". That wording points at the supervisor layer, not the gateway.

The gateway exits with **75 (`EX_TEMPFAIL`, `GATEWAY_SERVICE_RESTART_EXIT_CODE`)**
to hand restart ownership to a service supervisor. On Linux, systemd handles it
via `RestartForceExitStatus=75` + `RestartSec=5`. On Windows the supervisor is a
logon VBS in the Startup folder, which runs **once at logon and never again** —
so an exit-75 leaves the gateway down until the next logon, with nothing
complaining in between. The fix is a real supervisor or a re-start, not gateway
debugging.

**78 (`EX_CONFIG`, `GATEWAY_FATAL_CONFIG_EXIT_CODE`)** is the opposite intent: the
gateway deliberately stopped so a supervisor would *not* loop. Token collision or
no enabled platforms. Restarting in a loop is the wrong response; fix config.

## Event vocabulary

Group the lines by `pid` to reconstruct one lifecycle per process:

| tag | meaning |
|---|---|
| `gateway.start` | a process came up — carries `replace`, `breakaway`, `console_window_attached` |
| `gateway.exit_clean` | that process shut down without error |
| `asyncio.run.returned` | the event loop returned; `success` flags the verdict |
| `asyncio.run.SystemExit` | explicit exit — `code` plus a `traceback` string |
| `gateway.previous_unclean_exit` | a *later* start found the prior pid dead; carries `prior_pid`, `last_heartbeat_at`, `state_db_integrity` |

Classification rules:

- **start with no terminal event → the process vanished.** It never wrote a
  shutdown record, so something outside it killed it. On Windows that is nearly
  always a **Windows Job Object**: the gateway was spawned from a shell/session
  that was later torn down (an agent terminal, a CI job, a parent console) and
  the gateway died with the job. Hermes itself warns about this in its own
  status output. The remedy is to launch the gateway outside the invoking
  shell, or to supervise it — do not go looking for a crash in the gateway.
- **`asyncio.run.SystemExit` with code 75** → supervisor-gated restart (above).
- **`asyncio.run.returned` with `success: false`** → the runner asked to exit
  with a failure verdict; the gateway log carries an "exiting with failure"
  line naming the reason.
- **`gateway.previous_unclean_exit`** overrides a `clean` verdict: a later start
  found the pid dead, which outranks the process's own last word.
- **`replace: true`** means this start deliberately displaced a prior gateway —
  expected during a restart, and a useful signal when correlating with a
  `previous_unclean_exit` a few seconds earlier.

## Reconstructing incidents

Group by `pid`, take the `gateway.start` as the incident's beginning, and the
terminal event as its end. Derive duration from the two ISO-8601 `ts` values,
not from `gateway_state.json`'s `start_time` (monotonic — see the clock-domain
section in SKILL.md).

```python
from collections import OrderedDict
grouped = OrderedDict()
for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
    try:
        ev = json.loads(line)
    except json.JSONDecodeError:
        continue          # a torn final line from a kill is expected, not a fault
    if isinstance(ev, dict) and isinstance(ev.get('pid'), int):
        grouped.setdefault(ev['pid'], []).append(ev)
```

Then classify each group by its last event per the table above. Sort incidents
newest-first and surface the one matching the current `pid` from
`gateway_state.json`; that pair — "the state file claims this pid, and here is
how that pid died" — is the whole diagnosis.

## Verifying a supervisor actually exists

Do not assume the Startup entry implies supervision:

```bash
tasklist | grep -i hermes                      # is a gateway process alive?
cat "$APPDATA/Microsoft/Windows/Start Menu/Programs/Startup/Hermes_Gateway.vbs"
ls "$HERMES_HOME/gateway-service/"             # what does it actually launch?
```

A logon VBS proves the gateway starts *at logon*. It proves nothing about
afterwards, and that gap is the entire explanation for a gateway that dies
mid-day and stays dead.

## Building this into a dashboard

Derive per-process incidents in a **Qt-free, stdlib-only module** so it is
testable headlessly and cannot raise into the UI: swallow `json.JSONDecodeError`
per line (a kill truncates the last line), return `[]` on an unreadable file, and
degrade an unknown lifecycle to `verdict="unknown"` rather than a fabricated
failure. Aggregate a clean-rate over the last N incidents to show whether exits
are routine or chronic — on this host a 25% clean rate over 20 starts is itself
the finding.

Pair it with a schema contract: the app reads Hermes tables and files directly,
so an update that renames a field should surface as a reviewable diff, not as a
silently empty panel.
