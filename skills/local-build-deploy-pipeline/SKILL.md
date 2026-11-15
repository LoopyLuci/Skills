---
name: local-build-deploy-pipeline
description: local on-device CI/CD pipeline builder, preflight to verify.
category: devops
version: 1.0.0
author: hermes
license: MIT
tags: [ci-cd, pipeline, android, devops, on-device]
related_skills: []
---

# Local build & deploy pipeline (on-device CI/CD)

Build a self-contained, local, on-device CI/CD pipeline for a project like SpendingSaver: preflight env checks, unit tests, APK assembly, device install/launch, crash watch, and aggregate reporting. This is a **local** pipeline (runs on the developer's machine), NOT external CI.

## When to Use

Use this skill whenever you are asked to (a) stand up a **new, fully custom, local, on-device CI/CD pipeline** for an Android or desktop app, (b) add robustness/stability/performance features to an existing pipeline (retries, bounded timeouts, machine-readable results, crash watch, APK verification), or (c) structure the pipeline's stages, exit codes, and report format.

## Standing rules (always on)

- **Verified artifacts, not analysis.** Every stage must actually RUN and produce real output: the APK path, the unit test count/pass/fail, the crash-watch verdict. Never claim a stage succeeded without the tool reporting exit 0.
- **Immediate action.** "Proceed" means act now — build and run the pipeline, don't ask for confirmation.
- **Exhaustive scope.** Build every stage that applies (preflight, test, build, verify, report); never strip them down to a minimal version. Add all relevant checks (preflight, tests, build, install, crash watch, report).
- **Evidence, not analysis.** If a step fails, the pipeline reports the real command output and exit code — don't paper over failures or replace them with plausible summaries.
- **English only.** All output is in English.
- **No tool loops.** If a step fails, diagnose the root cause and change strategy — don't re-run the same failing command in a loop.

## Procedure (in order)

1. **Inventory** — read the project manifest: gradle wrapper, `local.properties` (`sdk.dir`), Android package/activity, connected devices. Do not assume the SDK path, package name, or activity.
2. **Design** — lay out the stages: preflight (env checks) → test (unit tests) → build (assemble APK) → verify (install + launch + crash-watch) → report (aggregate).
3. **Preflight** — check JDK 17+, gradle wrapper executable, `sdk.dir` in `local.properties`, Android SDK root, adb binary, at least one attached device in `device` state, and wait for the device to report `boot_completed=1`.
4. **Test** — run `./gradlew :app:testDebugUnitTest --console=plain --no-daemon --info` under a bounded timeout; parse the XML results (root `tests/failures/errors/skipped` attributes + `testcase` count); write a JUnit-like report to `$WORK_DIR/test-results.xml`; copy to `$REPORTS_DIR`.
5. **Build** — run `./gradlew assembleDebug` (+ optional AndroidTest) under a bounded timeout; verify the APK exists and is non-empty; copy the log.
6. **Verify (on-device)** — uninstall, install (`adb install -r`), wait for package visibility, launch (`am start -n <pkg>/.MainActivity`), wait for `Resumed`, poll `pidof com.spendingsaver` to confirm the process stays alive, then bound logcat capture and grep for crash markers (`FATAL EXCEPTION`, `has died`, `UnsatisfiedLinkError`, `SIGSEGV`, `SIGBUS`, `SIGABRT`, `NativeGetStackTrace`, `Process .* has died`) restricted to `com.spendingsaver`.
7. **Report** — aggregate TEST_RC / BUILD_RC / VERIFY_RC into `ci/artifacts/report.txt`, archive the APK, exit 0 only if every stage passed.

## Commands (concrete)

- Gradlew test: `./gradlew :app:testDebugUnitTest --console=plain --no-daemon --info`
- Gradlew assemble: `./gradlew :app:assembleDebug`
- Install: `adb install -r app-debug.apk`
- Launch: `adb shell am start -n com.spendingsaver/.MainActivity`
- Wait for package: `adb shell pm list packages | grep "^package:com.spendingsaver$"`
- Wait for resumed: `adb shell dumpsys activity activities | grep "Resumed activity .*com.spendingsaver/.*"`
- Crash watch: `adb logcat -v time` (bounded); grep for markers; restrict to our package.
- Log capture: `adb logcat -v time > file & sleep DURATION; kill %1` (bounded).

## Pitfalls (generalizable)

- `local.properties`' `sdk.dir` is the single source of truth for the SDK — never hardcode an SDK path inside a script. Prefer `CI_SDK_DIR`/`CI_ANDROID_HOME`/`ANDROID_SDK_ROOT` overrides.
- Verify the APK exists and is non-empty before installing; a stale or missing build makes `adb install` falsely fail.
- Wait for device boot (`boot_completed=1`) and activity `Resumed` before crash-watching. The app can take 30–60 s to start; a too-short window produces false negatives.
- Restrict crash markers to `com.spendingsaver` (the app's package). Otherwise system UI spam (e.g. a Fire launcher `AppsGrid` app) pollutes the log and masks real failures.
- Capture logcat with a bounded duration (`-v time` + `sleep` + `kill`). Never capture unbounded logcat.
- The driver (`run.sh`) must set per-stage exit-code env vars (`TEST_RC`, `BUILD_RC`, `VERIFY_RC`) so `report.sh` aggregates without re-running stages.
- `timeout_shell` handles bounded commands on Windows git-bash (which lacks GNU `timeout`): use a background-job + `sleep` + `kill` fallback, and prefer GNU `timeout` when present.
- Always verify a file write landed before reading it back (the `write_file`/`read_file` stale-read tracking blocks `write_file`; re-read with `read_file` to refresh, then patch or write).
- Always quote globs when passing multiple files to a command (`*.xml` expanded by the shell, not left quoted). Quoting a glob treats the literal directory as a file and produces TOTAL=0.

## Pitfalls learned (generalized)

- The `local` builtin in the `retry` wrapper cannot absorb a bare command: `local attempts=$1 wait=$2 shift 2` errors and the command never shifts. Write `local attempts=$1 wait=$2` then `shift 2` on the next line.
- `$(VAR)` runs the text of `VAR` as a **command**; use `$VAR` (no parens) to expand a variable's value. Use the parens form only for command substitution.
- Variables assigned **inside** `$(...)` are scoped to that command substitution and never reach the parent shell (a pipeline run exposed empty Gradle counts). Capture text output and re-parse, or set variables before the substitution and have the child print them.
- Android's `/system/bin` may lack `pidof`; use `ps -A | grep <package>` to confirm a process is alive.
- Quoting a glob (`"*.xml"`) passes the literal directory path to a command; **unquote** it so the shell expands the files. A non-matching quoted glob produces `TOTAL=0`. Globs must expand before the command receives them.
- Gradle writes test-results XML to `$PROJECT_ROOT/$APP_MODULE/app/build/test-results/testDebugUnitTest/` (inside the app module's build output), not under the CI `work/` directory. A wrong path silently yields TOTAL=0.
- `write_file` refuses to overwrite a file the session has not fully read; re-read with `read_file` (every page) before a stale-write, or use `patch` for a targeted edit.

## Supporting files

- `references/android-ci-recipes.md` — concrete commands for each Android pipeline stage.
- `references/pipeline-architecture.md` — stage contracts, exit-code table, report format.
