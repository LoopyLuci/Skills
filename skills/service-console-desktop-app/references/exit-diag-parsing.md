# Exit-diag parsing rules

`parse_exit_diag()` groups by the `pid` in each JSON line. The attribution of
`gateway.previous_unclean_exit` is the main subtlety.

- The record is written by the NEW process (its `pid` is the reporter).
- The DEAD process is the `prior_pid`.
- Index the obituary by `prior_pid`, not the reporter. Otherwise a clean
  shutdown (e.g. pid 6664 with `gateway.exit_clean`) is incorrectly marked
  `unclean` just because a later process (pid 800) reports 6664 as previous.
- The dead process's own exit record outranks the observer: `clean` stays
  `clean`; `vanished` (start only, no terminal event) is promoted to `unclean`
  when confirmed by an obituary.
- Duration: `clean` uses the `exit_clean` timestamp; `supervised-restart` uses
  the `SystemExit` timestamp (`code=75`); `unclean` uses the `previous_unclean_exit`
  timestamp (an upper bound on detection lag). `vanished` has no terminal event,
  so duration is `None`.
