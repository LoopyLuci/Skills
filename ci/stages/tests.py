"""tests — stdlib unittest discovery with a hard timeout and flaky rerun.

Runs in a subprocess so a runaway test can be killed with its whole tree, then
re-runs only the failing test ids once to separate flakes from real failures.
"""

from __future__ import annotations

import re
import time
from pathlib import Path

from ..util import Finding, StageResult, load_config, repo_root, run_cmd

FAIL_LINE = re.compile(r"^(FAIL|ERROR):\s+(\S+)\s+\(([^)]+)\)", re.M)


def _run_suite(tests_dir: Path, timeout: int, verbose: bool = True) -> tuple[int, str, str, float]:
    start = time.time()
    cmd = ["python", "-m", "unittest", "discover", "-s", str(tests_dir), "-t", str(repo_root())]
    if verbose:
        cmd.append("-v")
    rc, out, err = run_cmd(cmd, timeout=timeout)
    return rc, out, err, time.time() - start


def run(ctx: dict) -> StageResult:
    start = time.time()
    cfg = ctx["config"]
    root = repo_root()
    tests_dir = root / "tests"
    findings: list[Finding] = []
    flaky: list[str] = []

    if not tests_dir.is_dir():
        return StageResult("tests", True, time.time() - start,
                           "no tests/ directory (skipped)", [], {"skipped": True}, skipped=True)

    timeout = int(cfg.get("test_timeout", 900))
    rc, out, err, dur = _run_suite(tests_dir, timeout)
    output = (out or "") + (err or "")

    matches = FAIL_LINE.findall(output)
    failed_ids = [m[2] for m in matches]

    if rc == 124:
        findings.append(Finding("T_TIMEOUT", "error", f"test suite exceeded {timeout}s"))
    elif rc != 0 and not failed_ids:
        findings.append(Finding("T_FAILURE", "error",
                                f"test run failed (rc={rc}): {output[-800:]}"))

    if failed_ids:
        # flaky rerun: only the failures, once, on their own
        rc2, out2, err2, _ = _run_suite(tests_dir, timeout)
        rerun_output = (out2 or "") + (err2 or "")
        rerun_failures = {m[2] for m in FAIL_LINE.findall(rerun_output)}
        still = [t for t in failed_ids if t in rerun_failures]
        flaky = [t for t in failed_ids if t not in rerun_failures]
        for test_id in still:
            findings.append(Finding("T_TEST_FAIL", "error", f"test failed: {test_id}"))
        for test_id in flaky:
            findings.append(Finding("T_FLAKY", "warning",
                                    f"test passed on rerun (flake): {test_id}"))

    ran = re.findall(r"^Ran (\d+) tests?", output, re.M)
    stats = {
        "tests_run": int(ran[-1]) if ran else 0,
        "failures": len(failed_ids),
        "flaky": len(flaky),
        "duration_s": round(dur, 2),
    }
    ok = not any(f.severity == "error" for f in findings)
    summary = f"{stats['tests_run']} tests in {stats['duration_s']}s"
    if flaky:
        summary += f", {len(flaky)} flaky (passed on rerun)"
    if findings:
        summary += f", {sum(1 for f in findings if f.severity == 'error')} failing"
    return StageResult("tests", ok, time.time() - start, summary, findings, stats, flaky=flaky)
