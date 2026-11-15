"""File watcher: run the fast pipeline when repo sources change.

Poll-based (stdlib only), so it works on Windows without watchdog. Debounces
bursts of writes, then runs `python -m ci --fast`.

Usage:  python -m ci.watch [--interval 2.0] [--once]
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WATCHED = ("skills", "ci", "scripts", "tests", "generate_skills.py", "README.md")
SKIP_DIRS = {".git", "__pycache__", "reports", "logs", "dist", "_sources"}


def snapshot() -> dict[str, tuple[int, int]]:
    state: dict[str, tuple[int, int]] = {}
    for entry in WATCHED:
        base = ROOT / entry
        if base.is_file():
            st = base.stat()
            state[str(base)] = (st.st_mtime_ns, st.st_size)
            continue
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.is_file():
                try:
                    st = path.stat()
                except OSError:
                    continue
                state[str(path)] = (st.st_mtime_ns, st.st_size)
    return state


def digest_state(state: dict[str, tuple[int, int]]) -> str:
    joined = "\n".join(f"{k}:{v[0]}:{v[1]}" for k, v in sorted(state.items()))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def run_pipeline() -> int:
    proc = subprocess.run([sys.executable, "-m", "ci", "--fast"], cwd=str(ROOT))
    return proc.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ci.watch")
    parser.add_argument("--interval", type=float, default=2.0, help="poll interval seconds")
    parser.add_argument("--once", action="store_true", help="run once and exit")
    args = parser.parse_args(argv)

    print(f"watching {', '.join(WATCHED)} every {args.interval}s (Ctrl+C to stop)")
    last = digest_state(snapshot())
    if args.once:
        return run_pipeline()

    while True:
        time.sleep(args.interval)
        current = snapshot()
        now = digest_state(current)
        if now == last:
            continue
        # debounce: wait for the tree to settle
        time.sleep(args.interval)
        settled = digest_state(snapshot())
        if settled != now:
            continue
        last = settled
        print(f"change detected ({len(current)} files tracked) — running fast pipeline")
        rc = run_pipeline()
        print(f"pipeline {'GREEN' if rc == 0 else 'RED'} (rc={rc})")
        last = digest_state(snapshot())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
