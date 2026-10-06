# Exit-diag interpretation

A single JSON line from `gateway-exit-diag.log` describes a lifecycle event, not a full lifecycle. The lifetime of one gateway run is reconstructed by grouping by `pid`.

Tags and their meaning:

| Tag | Meaning for the pid that carries it |
|---|---|
| `gateway.start` | Process came up (`replace`, `breakaway`, `detached`, `console_attached`). |
| `gateway.exit_clean` | That process shut down cleanly. Authoritative for its own pid. |
| `asyncio.run.returned` | Event loop finished (`success` flag). Authoritative when `True` (clean); `False` = unclean. |
| `asyncio.run.SystemExit` | Exit code (`code`) + traceback. 75 = supervisor restart (`GATEWAY_SERVICE_RESTART_EXIT_CODE`); 78 = fatal config (`GATEWAY_FATAL_CONFIG_EXIT_CODE`). |
| `gateway.previous_unclean_exit` | A LATER process found the `prior_pid` dead without a clean exit. The DEAD pid is described by `prior_pid`, not the writer.

Attribution rules (verified by real log analysis):
1. A process with its own `gateway.exit_clean` keeps `clean` regardless of a later `previous_unclean_exit` that names it. Its own record outranks an outside observer.
2. A process with no terminal event (`start` only) gets `vanished` — no exit record was written, consistent with external kill (Windows Job Object, logout, taskkill, or power loss).
3. A `vanished` process that also has a `previous_unclean_exit` naming it is promoted to `unclean` — confirmed dead by a later observer.
4. `breakaway` and `console_window_attached` describe how the start was spawned; they do not predict failure, but `breakaway=True` + no exit record is the exact Job-Object-kill profile observed in `hermes gateway status` warnings.
