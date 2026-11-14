"""
Prepare the customization pass for imported upstream skills.

Outputs:
  scripts/repo-tag-index.json         tag -> [skill names] for the existing repo
  scripts/customization-worklist.json  per-skill metadata + rewrite batches
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
SOURCES = ROOT / "_sources"
MANIFEST = ROOT / "scripts" / "imported-upstream-skills.json"

N_BATCHES = 10


def parse_fm(text):
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}, text
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip().strip('"').strip("'")
    return fields, text[m.end():]


def title_of(body):
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def main():
    # ---- tag index over the existing repo ----
    tag_index = {}
    for d in SKILLS.iterdir():
        f = d / "SKILL.md"
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"tags:\s*\[([^\]]*)\]", text)
        if not m:
            continue
        for t in m.group(1).split(","):
            t = t.strip()
            if t:
                tag_index.setdefault(t, []).append(d.name)
    (ROOT / "scripts" / "repo-tag-index.json").write_text(
        json.dumps(tag_index, indent=1), encoding="utf-8")
    print(f"tag index: {len(tag_index)} tags")

    # ---- map upstream files ----
    upstream = {}
    for sd in SOURCES.iterdir():
        if not sd.is_dir():
            continue
        for f in sd.rglob("SKILL.md"):
            if ".git" in f.parts:
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            fm, _ = parse_fm(text)
            key = fm.get("name") or f.parent.name
            upstream.setdefault(key, f)
            upstream.setdefault(f.parent.name, f)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = []
    for src_name, items in manifest.items():
        for e in items:
            f = upstream.get(e["name"])
            if not f:
                print(f"  !! no upstream for {e['name']}")
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            fm, body = parse_fm(text)
            entries.append({
                "name": e["name"],
                "source": e["source"],
                "source_dir": src_name,
                "upstream_path": str(f.relative_to(ROOT)).replace("\\", "/"),
                "title": title_of(body) or e["name"].replace("-", " ").title(),
                "description": fm.get("description", ""),
                "tags": e["tags"],
                "lines": body.count("\n") + 1,
            })

    # ---- balance into batches by size (longest-first round robin) ----
    entries.sort(key=lambda x: -x["lines"])
    batches = [[] for _ in range(N_BATCHES)]
    loads = [0] * N_BATCHES
    for e in entries:
        i = loads.index(min(loads))
        batches[i].append(e)
        loads[i] += e["lines"]
    for i, b in enumerate(batches):
        for e in b:
            e["batch"] = i
    worklist = {
        "output_dir": "scripts/adapted_bodies",
        "n_batches": N_BATCHES,
        "skills": entries,
    }
    (ROOT / "scripts" / "customization-worklist.json").write_text(
        json.dumps(worklist, indent=2), encoding="utf-8")
    print(f"skills: {len(entries)}  batches: {N_BATCHES}")
    for i, b in enumerate(batches):
        print(f"  batch {i}: {len(b)} skills, {sum(x['lines'] for x in b)} lines")


if __name__ == "__main__":
    main()
