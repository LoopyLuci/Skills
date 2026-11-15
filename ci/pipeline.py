"""Pipeline orchestrator: locking, change detection, stage execution, reports.

Run with:  python -m ci --full      (all stages)
           python -m ci --fast      (preflight, static, skills, tests)
           python -m ci --only skills tests
           python -m ci --list
           python -m ci --full --push
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from .stages import FAST_STAGES, STAGES
from .util import (DIST_DIR, LOGS_DIR, LOCK_PATH, REPORTS_DIR, Finding, StageResult,
                   changed_files, ensure_dirs, git_out, load_config, repo_root)

RULES: dict[str, set[str]] = {
    "skills": {"skills"},
    "static": {"ci", "scripts", "tests"},
    "tests": {"ci", "scripts", "tests"},
    "build": {"skills"},
    "smoke": {"skills", "ci"},
    "deploy": {"ci", "scripts"},
    "preflight": {"ci"},
}


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        import subprocess

        try:
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"],
                                 capture_output=True, text=True, timeout=20)
            return str(pid) in (out.stdout or "")
        except Exception:
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


class Lock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.acquired = False

    def acquire(self) -> tuple[bool, str]:
        ensure_dirs()
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text(encoding="utf-8"))
                pid = int(data.get("pid", 0))
            except Exception:
                pid = 0
            if pid and _pid_alive(pid):
                return False, f"pipeline already running (pid {pid})"
        self.path.write_text(json.dumps({"pid": os.getpid(),
                                         "started": time.time(),
                                         "host": os.environ.get("COMPUTERNAME", "")}),
                             encoding="utf-8")
        self.acquired = True
        return True, "acquired"

    def release(self) -> None:
        if self.acquired and self.path.exists():
            try:
                self.path.unlink()
            except OSError:
                pass


class Logger:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = path.open("w", encoding="utf-8")

    def __call__(self, message: str) -> None:
        line = f"[{time.strftime('%H:%M:%S')}] {message}"
        print(line, flush=True)
        self.fh.write(line + "\n")
        self.fh.flush()

    def close(self) -> None:
        self.fh.close()


def plan_stages(args, cfg: dict, log) -> list[str]:
    if args.only:
        wanted = [s.strip() for s in args.only.split(",") if s.strip()]
        unknown = [s for s in wanted if s not in dict(STAGES)]
        if unknown:
            raise SystemExit(f"unknown stage(s): {', '.join(unknown)}")
        return wanted
    if args.fast:
        return list(FAST_STAGES)
    return [name for name, _ in STAGES]


def select_by_changes(changed: list[str], stages: list[str], log) -> list[str]:
    if not changed:
        return stages
    selected: set[str] = set()
    for stage in stages:
        prefixes = RULES.get(stage, set())
        for path in changed:
            top = path.split("/", 1)[0]
            if top in prefixes:
                selected.add(stage)
                break
    # a skills change must also refresh build/smoke; a code change must test
    if "skills" in selected:
        selected.update({"build", "smoke"})
    if "static" in selected or "tests" in selected:
        selected.add("tests")
    selected.add("preflight")
    ordered = [s for s in stages if s in selected]
    log(f"change-aware selection: {len(changed)} changed file(s) -> {', '.join(ordered)}")
    return ordered


def _prune(directory: Path, limit: int, suffix: str) -> None:
    files = sorted(directory.glob(f"*{suffix}"), key=lambda p: p.stat().st_mtime)
    for old in files[:-limit] if len(files) > limit else []:
        try:
            old.unlink()
        except OSError:
            pass


def write_reports(cfg: dict, run: dict, log) -> dict:
    ensure_dirs()
    ts = run["timestamp"]
    report_path = REPORTS_DIR / f"{ts}.json"
    report_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    (REPORTS_DIR / "latest.json").write_text(json.dumps(run, indent=2), encoding="utf-8")

    history = REPORTS_DIR / "history.jsonl"
    with history.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "timestamp": ts,
            "ok": run["ok"],
            "duration_s": run["duration_s"],
            "stages": {s["name"]: {"ok": s["ok"], "duration_s": s["duration_s"]}
                       for s in run["stages"]},
        }) + "\n")

    _prune(REPORTS_DIR, int(cfg.get("history_limit", 50)), ".json")
    _prune(LOGS_DIR, int(cfg.get("log_limit", 50)), ".log")
    log(f"report: {report_path.relative_to(repo_root())}")
    return {"report": str(report_path)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ci", description="Local on-device CI/CD pipeline")
    parser.add_argument("--full", action="store_true", help="run every stage")
    parser.add_argument("--fast", action="store_true", help="preflight, static, skills, tests")
    parser.add_argument("--only", help="comma-separated stage names")
    parser.add_argument("--list", action="store_true", help="show the plan and exit")
    parser.add_argument("--push", action="store_true", help="push after a green deploy stage")
    parser.add_argument("--jobs", type=int, help="worker count override")
    parser.add_argument("--no-deploy", action="store_true", help="skip the deploy stage")
    parser.add_argument("--changed-only", action="store_true",
                        help="restrict the skills stage to changed skill dirs")
    args = parser.parse_args(argv)

    cfg = load_config()
    if args.jobs:
        cfg["jobs"] = args.jobs
    ensure_dirs()

    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    log = Logger(LOGS_DIR / f"{stamp}.log")
    run_started = time.time()

    lock = Lock(LOCK_PATH)
    ok, message = lock.acquire()
    if not ok:
        log(f"REFUSED: {message}")
        log.close()
        return 2
    log(f"pipeline start pid={os.getpid()} args={' '.join(sys.argv[1:]) or '(none)'}")

    try:
        stages = plan_stages(args, cfg, log)
        if args.no_deploy and "deploy" in stages:
            stages = [s for s in stages if s != "deploy"]

        changed = changed_files()
        if args.fast or args.only or args.changed_only:
            pass  # explicit selection wins
        else:
            stages = select_by_changes(changed, stages, log)

        if args.list:
            log("plan:")
            for name in stages:
                log(f"  - {name}")
            log.close()
            lock.release()
            return 0

        only_changed = None
        if args.changed_only:
            only_changed = sorted({p.split("/", 1)[1].split("/", 1)[0]
                                   for p in changed if p.startswith("skills/")})
            log(f"changed-only skills: {len(only_changed)}")

        ctx = {"config": cfg, "log": log, "push": args.push,
               "only_changed_skills": only_changed, "results": []}
        results: list[StageResult] = []
        for name, func in STAGES:
            if name not in stages:
                continue
            log(f"=== stage: {name} ===")
            try:
                result = func(ctx)
            except Exception as exc:  # a stage crash must not abort the run silently
                import traceback

                log(f"stage {name} crashed: {exc}")
                log(traceback.format_exc())
                result = StageResult(name, False, 0.0, f"crashed: {exc}",
                                     [Finding("STAGE_CRASH", "error", str(exc))])
            ctx["results"].append(result)
            results.append(result)
            status = "PASS" if result.ok else "FAIL"
            log(f"--- {name}: {status} in {result.duration:.2f}s | {result.summary}")
            for f in result.findings:
                if f.severity == "error":
                    log(f"    [{f.code}] {f.path} {f.message}")

        run = {
            "timestamp": stamp,
            "ok": all(r.ok for r in results) if results else False,
            "duration_s": round(time.time() - run_started, 3),
            "branch": git_out(["rev-parse", "--abbrev-ref", "HEAD"]),
            "commit": git_out(["rev-parse", "HEAD"]),
            "python": sys.version.split()[0],
            "changed_files": len(changed),
            "stages": [r.as_dict() for r in results],
        }
        write_reports(cfg, run, log)
        log(f"pipeline {'GREEN' if run['ok'] else 'RED'} in {run['duration_s']}s")
        return 0 if run["ok"] else 1
    finally:
        lock.release()
        log.close()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
