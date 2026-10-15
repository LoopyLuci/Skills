# Live verification against a counterparty's real runtime

When a wire-level probe is not enough — the pattern must be proven end-to-end,
not just at the handshake — stand the counterparty up for real and drive its
actual endpoint. Recipe for a Python counterparty on this Windows host:

1. **Create its venv on the Python its lock targets.** Check the counterparty's
   `requirements.lock` header (or CI config) for the pinned version — the shell
   default python is often newer than what its dependencies support.
   `uv venv .venv --python 3.11 && uv pip install --python .venv/Scripts/python.exe -r requirements.txt`.
2. **Get its real auth token through its own tooling.** Many server projects
   persist a generated token on first boot (e.g. a `--print-token` CLI entry
   point). Setting your own token in the environment does not override a token
   the counterparty already generated and validates against — read the
   persisted one, or restart the counterparty with your token after killing
   every stale instance of it.
3. **Launch it with an explicit port and token, output to a log file.**
   `DASHBOARD_TOKEN=... DASHBOARD_PORT=8787 .venv/Scripts/python.exe -m pkg.main > /tmp/x.log 2>&1`.
   Verify readiness with a real request (`curl -s -o /dev/null -w "%{http_code}"`),
   never a blind sleep.
4. **Create the minimum instances the seam needs.** A headless/app-platform
   bot that needs no credentials is the cheapest target; some seams also need
   a source instance to exist before the call resolves (a 404 naming the
   instance is a missing-instance problem, not a routing failure).
5. **Drive the real endpoint and record code, latency, and body** for each
   direction of the seam separately.
6. **Verify the build under test contains the new code before blaming the
   seam.** `grep -a "NewSymbol" target/release/app.exe` — the `strings` binary
   is not installed on this host.

## Managing the processes you start

- **A background terminal call that dies at the tool's timeout cap often still
  launched its process.** Verify with `netstat -ano | grep <port>` or
  `tasklist` before re-running; re-launching stacks duplicate servers fighting
  over one port, and the symptom (connection refused while something listens)
  looks like the opposite of what happened.
- **Identify a port's owner before killing anything.** `netstat -ano` gives the
  PID; `powershell -Command "Get-CimInstance Win32_Process -Filter 'ProcessId=<pid>' | Select-Object Name,CreationDate"` (and the same with `CommandLine`) tells you which instance and how old it is — a same-named process from an earlier session is a zombie, not the one you just started.
- **Kill stale build/test processes before rebuilding.** Zombie `cargo test`
  runs from earlier sessions hold the build directory lock; new cargo commands
  then hang with no output, which reads as a broken toolchain. Match on
  CommandLine (`... | Where-Object { $_.CommandLine -like '*pkg.main*' } |
  Stop-Process -Force`) rather than killing by image name.
- **cargo test appearing to "hang" at the tool timeout on a loaded machine is
  often just slow.** Run it to a log file and poll the file — cargo buffers
  test output until the run completes, so a piped command shows nothing even
  while tests pass.
- **When a running app holds its own binary, the release rebuild fails with
  "Access is denied"** — stop the app process first, rebuild, relaunch.
