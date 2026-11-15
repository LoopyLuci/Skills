"""Install the git hooks that run the local pipeline automatically.

Usage:  python -m ci.install_hooks [--force]
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS_SRC = ROOT / "ci" / "hooks"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="install_hooks")
    parser.add_argument("--force", action="store_true",
                        help="overwrite hooks that already exist")
    args = parser.parse_args(argv)

    git_dir = ROOT / ".git"
    if not git_dir.is_dir():
        print("not a git repository; hooks not installed", file=sys.stderr)
        return 1
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    installed = []
    for name in ("pre-commit", "pre-push"):
        src = HOOKS_SRC / name
        dst = hooks_dir / name
        if dst.exists() and not args.force:
            print(f"  skip {name} (exists; use --force to overwrite)")
            continue
        shutil.copy2(src, dst)
        mode = dst.stat().st_mode
        dst.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        installed.append(name)
        print(f"  installed {name}")

    if not installed:
        print("no changes")
    else:
        print(f"hooks installed into {hooks_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
