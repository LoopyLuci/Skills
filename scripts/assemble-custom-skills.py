"""
Assemble the customized skills.

Reads the condensed/rewritten bodies from scripts/adapted_bodies/<name>.md and
rebuilds each skills/<name>/SKILL.md in this repo's canonical layout, adding:

  - canonical frontmatter (description rewritten into trigger form)
  - ## Trigger                      (derived from the upstream description)
  - ## When NOT to Use              (extracted from upstream anti-patterns)
  - <rewritten body>
  - ## Related Skills in This Repo (computed cross-links)
  - ## Adaptation Notes             (what was changed)
  - ## Source & Attribution         (upstream repo, path, license, date)
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
BODIES = ROOT / "scripts" / "adapted_bodies"
WORKLIST = ROOT / "scripts" / "customization-worklist.json"
TAG_INDEX = ROOT / "scripts" / "repo-tag-index.json"
OUT_MANIFEST = ROOT / "scripts" / "customization-manifest.json"

RETRIEVED = "2026-11-14"

LICENSES = {
    "addyosmani/agent-skills": ("MIT", "Addy Osmani", "2025"),
    "cloudflare/security-audit-skill": ("MIT", "Cloudflare, Inc.", "2025-2026"),
    "Forward-Future/loopy": ("MIT", "Forward Future", "2026"),
    "mattpocock/skills": ("MIT", "Matt Pocock", "2026"),
    "obsidianmd/obsidian-skills": ("MIT", "Steph Ango (@kepano)", "2026"),
    "oracle/skills": ("UPL-1.0", "Oracle and/or its affiliates", "2025"),
}

VERBS = {
    "extract", "create", "build", "test", "interact", "sync", "provide",
    "discover", "generate", "deploy", "diagnose", "manage", "automate",
    "conduct", "guide", "render", "harden", "drive", "establish", "subject",
    "record", "optimize", "optimise", "simplify", "review", "implement",
    "refactor", "audit", "analyse", "analyze", "find", "compare", "repair",
    "adapt", "craft", "run", "debrief", "save", "prepare", "search",
    "monitor", "instrument", "structure", "document", "refine", "deliver",
    "plan", "break", "launch", "ship", "reduce", "migrate", "deprecate",
    "explore", "troubleshoot", "configure", "scaffold", "teach", "grill",
    "hand", "write", "publish", "validate", "verify", "inspect", "check",
}


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


def gerund(word):
    w = word.lower()
    if w.endswith("ies"):
        return word[:-3] + "ying"
    if w.endswith("es") and not w.endswith(("ses", "sses")):
        return word[:-1] + "ing"
    if w.endswith("e") and not w.endswith("ee"):
        return word[:-1] + "ing"
    if w.endswith("s") and not w.endswith("ss"):
        return word[:-1] + "ing"
    return word + "ing"


def trigger_description(desc):
    """Rewrite the upstream description into the repo's 'Use when ...' form."""
    clauses = []
    for sent in re.split(r"(?<=[.!?])\s+", desc):
        m = re.search(r"(?i)\buse (?:this skill )?when\b[:]?\s*(.+)", sent)
        if not m:
            m = re.search(r"(?i)\buse (?:this skill )?for\b[:]?\s*(.+)", sent)
        if m:
            c = m.group(1).strip().rstrip(".")
            if c:
                clauses.append(c[0].lower() + c[1:])
    if clauses:
        return "Use when " + "; ".join(clauses) + "."
    first = desc.strip().split(". ")[0].rstrip(".")
    word = first.split(" ")[0].strip(",")
    if word.lower() in VERBS:
        rest = first[len(word):]
        return f"Use when {gerund(word).lower()}{rest}."
    return f"Use when working with {first[0].lower()}{first[1:]}."


def trigger_bullets(desc):
    clauses = []
    for sent in re.split(r"(?<=[.!?])\s+", desc):
        m = re.search(r"(?i)\buse (?:this skill )?when\b[:]?\s*(.+)", sent)
        if not m:
            m = re.search(r"(?i)\buse (?:this skill )?for\b[:]?\s*(.+)", sent)
        if m:
            c = m.group(1).strip().rstrip(".")
            if c:
                clauses.append(c[0].upper() + c[1:])
    if not clauses:
        clauses = [desc.strip().rstrip(".")]
    return clauses


def extract_when_not(body):
    """Pull bullets out of upstream anti-pattern sections."""
    lines = body.splitlines()
    out = []
    i = 0
    while i < len(lines):
        m = re.match(r"^(#{2,4})\s*(.+?)\s*$", lines[i])
        if m:
            level = len(m.group(1))
            title = m.group(2).lower()
            if re.search(r"when not to use|when not to|red flags|common rationalizations|anti-?patterns|common pitfalls|pitfalls", title):
                i += 1
                while i < len(lines):
                    nxt = re.match(r"^(#{1,4})\s+", lines[i])
                    if nxt and len(nxt.group(1)) <= level:
                        break
                    b = re.match(r"^\s*[-*]\s+(.+)", lines[i])
                    if b:
                        item = b.group(1).strip()
                        item = re.sub(r"\*\*", "", item)
                        if item:
                            out.append(item)
                    i += 1
                continue
        i += 1
    # de-dup, keep order
    seen = set()
    uniq = []
    for x in out:
        k = x.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(x)
    return uniq


def load_repo_meta():
    """name -> (description, tags) for existing repo skills."""
    meta = {}
    for d in SKILLS.iterdir():
        f = d / "SKILL.md"
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        fm, _ = parse_fm(text)
        tags = []
        mt = re.search(r"tags:\s*\[([^\]]*)\]", text)
        if mt:
            tags = [t.strip() for t in mt.group(1).split(",") if t.strip()]
        meta[d.name] = (fm.get("description", ""), tags)
    return meta


GENERIC_TAGS = {
    "productivity", "engineering", "software-development", "automation",
    "agent-skills", "agent-workflow", "ai-agents", "general", "tools",
}


def related_skills(name, source, tags, worklist, repo_meta, imported_names):
    peers = [e["name"] for e in worklist
             if e["source"] == source and e["name"] != name]
    peers = peers[:4]
    tag_set = set(tags) - GENERIC_TAGS
    scored = []
    for rname, (_, rtags) in repo_meta.items():
        if rname == name or rname in imported_names:
            continue
        overlap = tag_set & (set(rtags) - GENERIC_TAGS)
        if overlap:
            scored.append((len(overlap), rname))
    scored.sort(reverse=True)
    matches = [r for _, r in scored[:3]]
    return peers, matches


def build(entry, worklist, repo_meta, tag_index, imported_names):
    name = entry["name"]
    body_path = BODIES / f"{name}.md"
    if not body_path.exists():
        return None, "missing body"
    body = body_path.read_text(encoding="utf-8").strip()
    # strip accidental frontmatter
    if body.startswith("---"):
        _, body = parse_fm(body)
        body = body.strip()

    up_fields, up_body = parse_fm(
        (ROOT / entry["upstream_path"]).read_text(encoding="utf-8", errors="replace"))
    up_desc = up_fields.get("description", "")
    desc = trigger_description(up_desc)
    bullets = trigger_bullets(up_desc)
    when_not = extract_when_not(up_body)

    license_name, copyright_holder, year = LICENSES.get(
        entry["source"], ("MIT", "the upstream authors", "2026"))

    peers, matches = related_skills(name, entry["source"], entry["tags"],
                                    worklist, repo_meta, imported_names)

    lines = []
    lines.append("---")
    lines.append(f"name: {name}")
    lines.append(f"description: {desc}")
    lines.append("version: 2.0.0")
    lines.append("author: LoopyLuci Community")
    lines.append(f"license: {license_name}")
    lines.append("platforms: [any]")
    lines.append("metadata:")
    lines.append("  hermes:")
    lines.append(f"    tags: [{', '.join(entry['tags'])}]")
    lines.append(f"    source: {entry['source']}")
    lines.append("    adapted: true")
    lines.append("---")
    lines.append("")
    lines.append(f"# {entry['title']}")
    lines.append("")
    lines.append(f"> **Adapted for the LoopyLuci Skills collection** from "
                 f"[{entry['source']}](https://github.com/{entry['source']}). "
                 "The guidance below is rewritten and condensed for this repo; "
                 "commands, paths, and reference tables are preserved.")
    lines.append("")
    lines.append("## Trigger")
    lines.append("")
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("## When NOT to Use")
    lines.append("")
    if when_not:
        for w in when_not:
            lines.append(f"- {w}")
    else:
        lines.append("- Outside the trigger above; keep the task in the skill that owns it.")
    lines.append("")
    lines.append(body)
    lines.append("")
    lines.append("## Related Skills in This Repo")
    lines.append("")
    for p in peers:
        pd = repo_meta.get(p, ("", []))[0]
        pd = (pd[:90] + "...") if len(pd) > 90 else pd
        lines.append(f"- [{p}](../{p}/SKILL.md) — {pd}" if pd else f"- [{p}](../{p}/SKILL.md)")
    for mname in matches:
        md = repo_meta.get(mname, ("", []))[0]
        md = (md[:90] + "...") if len(md) > 90 else md
        lines.append(f"- [{mname}](../{mname}/SKILL.md) — {md}" if md else f"- [{mname}](../{mname}/SKILL.md)")
    lines.append("")
    lines.append("## Adaptation Notes")
    lines.append("")
    lines.append("- Description rewritten into this repo's trigger form.")
    lines.append("- Trigger and When-NOT-to-Use sections derived from the upstream guidance.")
    lines.append("- Body condensed and restructured; commands, file paths, and tables preserved.")
    if when_not:
        lines.append("- Upstream anti-patterns retained as the When-NOT-to-Use list.")
    lines.append("- Related skills linked from this repo.")
    lines.append("- Upstream branding and attribution lines removed (attribution below).")
    lines.append("")
    lines.append("## Source & Attribution")
    lines.append("")
    lines.append(f"- Upstream: [{entry['source']}](https://github.com/{entry['source']})")
    lines.append(f"- Path: `{entry['upstream_path']}`")
    lines.append(f"- License: {license_name} — Copyright (c) {year} {copyright_holder}")
    lines.append(f"- Retrieved: {RETRIEVED}; rewritten and condensed by LoopyLuci Community.")
    lines.append("")
    return "\n".join(lines), None


def main():
    work = json.loads(WORKLIST.read_text(encoding="utf-8"))
    entries = work["skills"]
    imported_names = {e["name"] for e in entries}
    repo_meta = load_repo_meta()
    print(f"repo skills indexed: {len(repo_meta)}")
    ok, failed = 0, []
    manifest = {}
    for e in entries:
        content, err = build(e, entries, repo_meta, None, imported_names)
        if err:
            failed.append((e["name"], err))
            continue
        (SKILLS / e["name"] / "SKILL.md").write_text(content, encoding="utf-8")
        manifest[e["name"]] = {"source": e["source"], "title": e["title"],
                               "description": trigger_description(
                                   parse_fm((ROOT / e["upstream_path"]).read_text(
                                       encoding="utf-8", errors="replace"))[0].get("description", ""))}
        ok += 1
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"assembled: {ok}  failed: {len(failed)}")
    for n, err in failed:
        print(f"  !! {n}: {err}")


if __name__ == "__main__":
    main()
