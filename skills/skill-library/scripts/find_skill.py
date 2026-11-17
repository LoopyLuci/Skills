"""Search the skill library's catalogue (catalog.jsonl beside this script's folder) and print the best matches.

Standard library only. Scoring: whole-word matches in the name count most, then tags, then the description, with
a bonus when every query word matches somewhere.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CATALOG = HERE / "catalog.jsonl"
WORD = re.compile(r"[a-z0-9]+")


def words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def load() -> list[dict]:
    with CATALOG.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def score(skill: dict, query: list[str]) -> float:
    name, tags, desc = set(words(skill["name"])), set(words(" ".join(skill.get("tags", [])))), set(words(skill.get("description", "")))
    total, hit = 0.0, 0
    for q in query:
        s = 3.0 * (q in name) + 2.0 * (q in tags) + 1.0 * (q in desc)
        if not s and len(q) > 3:   # prefix match for plurals and variants ("containers" -> "container")
            s = 0.5 * any(w.startswith(q[:-1]) or q.startswith(w) for w in name | tags if len(w) > 3)
        total += s
        hit += s > 0
    return total + (2.0 if query and hit == len(query) else 0.0)


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Find a skill in the library")
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--category", default="")
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--categories", action="store_true", help="list the categories and stop")
    a = ap.parse_args(argv)
    skills = load()
    if a.categories:
        for cat, n in Counter(s.get("category", "") for s in skills).most_common():
            print(f"{n:6}  {cat}")
        return 0
    query = words(a.query)
    pool = [s for s in skills
            if (not a.category or s.get("category", "").lower().startswith(a.category.lower()))
            and all(t.lower() in [x.lower() for x in s.get("tags", [])] for t in a.tag)]
    ranked = sorted(((score(s, query), s) for s in pool), key=lambda p: (-p[0], p[1]["name"]))
    ranked = [p for p in ranked if p[0] > 0] if query else ranked
    if not ranked:
        print("no matching skill; carry on without one")
        return 0
    library = HERE.parent
    for sc, s in ranked[:a.limit]:
        print(f"{s['name']}  [{s.get('category', '')}]  score {sc:.1f}\n    {s.get('description', '')}\n"
              f"    {library / s['name'] / 'SKILL.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
