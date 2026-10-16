# Troubleshooting Guide

## Pipeline fails at preflight: "project or its test tools do not import"

**Cause**: The package is not installed in the venv.
**Fix**: Run `.venv/Scripts/python.exe -m pip install -e .`

## Pipeline fails at static: "files over 5 MB in this push"

**Cause**: The big-file check is scanning the full historical diff range, which includes old commits that tracked build artifacts (e.g., `target/`) later removed.
**Fix**: Change the check to scan only the working tree (uncommitted + untracked + staged files) against HEAD.

## Pipeline fails at static: "bare except:"

**Cause**: Code uses bare `except:` which catches KeyboardInterrupt and SystemExit.
**Fix**: Replace with `except Exception:`.

## Pipeline fails at android: "What went wrong: 25.0.2"

**Cause**: The error parsing uses `tail(out)` which grabs a version number from Gradle output instead of the real error.
**Fix**: Parse for `FAILURE:` and `What went wrong:` blocks in the output.

## Pipeline fails at tests: "ModuleNotFoundError: No module named 'vm_harness'"

**Cause**: The package is not installed in the venv.
**Fix**: Run `.venv/Scripts/python.exe -m pip install -e .`

## Pipeline fails at tests: "Grip x=1004 out of bounds (w=826)"

**Cause**: DPI scaling is scaling the main window's own layout margins, shifting resize grips outside the window bounds.
**Fix**: Exclude `self` from layout margin/spacing scaling in the DPI scaling code.

## Pipeline fails at tests: "SSH connection failed: [WinError 1225]"

**Cause**: Integration tests trying to connect to a remote host that's not available.
**Fix**: These are environment-scoped failures. Skip integration tests or ensure the remote host is available.

## Pipeline fails at smoke: "the hub did not write control.json in 90s"

**Cause**: The hub takes too long to start.
**Fix**: Increase the timeout or check if the hub is failing to start (check the log file).

## Pipeline fails at deploy: "the hub did not come back within 60s"

**Cause**: The hub is not restarting properly.
**Fix**: Check if the hub process is running and if the port is available.

## Stale pipeline reports

**Cause**: Background pipeline processes from before a fix was applied are still completing and reporting failures.
**Fix**: Check the timestamp on the report. If it's from before the fix was committed, it's stale. Re-run the pipeline for a fresh result.
