"""Build what Claude Code needs from the skills folder: the skill library's catalogue and the plugin marketplace.

  skills/skill-library/catalog.jsonl   one line per skill: name, description, tags, category (searched on demand)
  .claude-plugin/marketplace.json       the marketplace: "core" (claude-router and skill-library, small enough to
                                        keep on) and one plugin per category (install from the app when wanted)

Categories come from docs/skills-index.md (regenerate it first: scripts/generate-docs-index.py). Standard library
only. Run from the repository root: python scripts/build-claude-marketplace.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CORE = ["claude-router", "skill-library"]
MARKETPLACE = "loopyluci-skills"
FRONT = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def frontmatter(path: Path) -> dict:
    m = FRONT.match(path.read_text(encoding="utf-8", errors="replace"))
    out: dict = {}
    if not m:
        return out
    for key in ("name", "description"):
        km = re.search(rf"^{key}:\s*(.+)$", m.group(1), re.M)
        if km:
            out[key] = km.group(1).strip().strip("'\"")
    tm = re.search(r"tags:\s*\[([^\]]*)\]", m.group(1))
    out["tags"] = [t.strip().strip("'\"") for t in tm.group(1).split(",") if t.strip()] if tm else []
    return out


def categories() -> dict[str, str]:
    cat, out = "", {}
    for line in (ROOT / "docs" / "skills-index.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") and line[3:] != "Contents":
            cat = line[3:].strip()
        elif (m := re.search(r"\(\.\./skills/([^/]+)/SKILL\.md\)", line)) and cat:
            out[m.group(1)] = cat
    return out


def main() -> int:
    cats = categories()
    catalog, by_cat = [], {}
    for d in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()):
        fm = frontmatter(d / "SKILL.md")
        cat = "Core" if d.name in CORE else cats.get(d.name, "General & Other")
        catalog.append({"name": d.name, "description": fm.get("description", ""), "tags": fm.get("tags", []), "category": cat})
        if d.name not in CORE:
            by_cat.setdefault(cat, []).append(d.name)
    out = SKILLS / "skill-library" / "catalog.jsonl"
    out.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in catalog), encoding="utf-8")

    plugins = [{
        "name": "core",
        "source": "./",
        "strict": False,
        "description": "claude-router (pick Haiku, Sonnet or Opus for delegated work and orchestrate it) and "
                       f"skill-library (search all {len(catalog):,} skills and load one only when it's needed).",
        "skills": [f"./skills/{n}" for n in CORE],
    }]
    for cat, names in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        plugins.append({
            "name": slug(cat),
            "source": "./",
            "strict": False,
            "description": f"{cat}: {len(names):,} skills, all switched on together. Each one adds its description "
                           "to every conversation, so the skill-library in 'core' is usually the better way to use them.",
            "skills": [f"./skills/{n}" for n in names],
        })
    market = {"name": MARKETPLACE, "owner": {"name": "LoopyLuci"},
              "metadata": {"description": f"LoopyLuci's {len(catalog):,} skills for Claude Code"},
              "plugins": plugins}
    (ROOT / ".claude-plugin").mkdir(exist_ok=True)
    (ROOT / ".claude-plugin" / "marketplace.json").write_text(json.dumps(market, indent=2) + "\n", encoding="utf-8")
    print(f"catalog: {len(catalog)} skills; marketplace: {len(plugins)} plugins "
          + ", ".join(f"{p['name']} ({len(p['skills'])})" for p in plugins))
    return 0


if __name__ == "__main__":
    sys.exit(main())
