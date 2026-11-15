# Pipeline architecture

## Stage contract

Every stage is a self-contained script under `ci/stages/`. It sources `lib.sh` (logging helpers: `log_step`, `log_ok`, `log_error`, `log_warn`) and `config.sh` (env overrides), and it must:

1. Set its own exit code explicitly (`exit 0` / `exit 1`); do not rely on `set -e`.
2. Print a one-line header with `log_step`.
3. Write its own logs to `$WORK_DIR/<stage>.log`.
4. Be idempotent — re-running a stage after a partial run is safe.

## Exit-code table

| Env var | Stage | Meaning |
|---|---|---|
| `TEST_RC` | `test.sh` | `0` = all unit tests passed; `1` = one or more failed |
| `BUILD_RC` | `build.sh` | `0` = APK assembled and non-empty; `1` = assemble or verification failed |
| `VERIFY_RC` | `verify.sh` | `0` = installed, launched, alive, no crash; `1` = crash or launch failure |
| `PREFALL_RC` | `preflight.sh` | `0` = toolchain + device ready |

The driver (`run.sh`) writes these into the environment so `report.sh` can aggregate without re-running stages.

## Report format

`ci/artifacts/report.txt` (written by `report.sh`), machine-readable:

```
# SpendingSaver CI/CD report
Generated: <UTC ISO8601>
Device: <serial>

| Stage | Result |
|---|---|
| preflight | PASS |
| test | PASS |
| build | PASS |
| verify | PASS |

Gradle test exit: 0
Gradle assemble exit: 0
Verify exit: 0
Artifact APK: ci/artifacts/app-debug.apk
Test report: ci/work/test-results.xml
Build log: ci/work/build.log
Verify logcat: ci/work/verify.logcat
```

Each stage also writes a progress marker to `$WORK_DIR/.stages` as `stage=exitcode` lines so the driver and report can verify ordering and catch premature re-runs.

## Robustness / stability / performance features

- **Bounded timeouts** — every gradle/adb/logcat command is wrapped in `timeout_shell` (GNU `timeout` preferred; background-job + `sleep` + `kill` fallback for Windows git-bash).
- **Retries** — `retry N DELAY CMD` re-runs flaky adb commands up to N times.
- **Machine-readable results** — JUnit-like XML under `app/build/test-results/`; the pipeline aggregates counters rather than parsing prose.
- **Crash watch** — bounded `adb logcat -v time` capture followed by grep for `FATAL EXCEPTION`, `has died`, `UnsatisfiedLinkError`, `SIGSEGV/SIGBUS/SIGABRT`, `NativeGetStackTrace`, `Process .* has died` — restricted to `com.spendingsaver` to avoid system-UI noise.
- **APK verification** — `[[ -s file ]]` before `adb install`; a stale or missing build is a hard failure with a real path in the error.
- **Process-alive polling** — `pidof com.spendingsaver` over a bounded window, so a slow app start (30–60 s) does not produce a false crash.
- **Incremental gradle** — `--no-build-cache` + `--max-workers 2` in CI to avoid cache-induced false passes; local dev reuses the build cache.

## Pipeline layout

```
ci/
  config.sh
  lib.sh
  run.sh
  stages/
    preflight.sh
    test.sh
    build.sh
    verify.sh
    report.sh
```