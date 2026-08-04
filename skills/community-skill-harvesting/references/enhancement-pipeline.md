# Community Skill Harvesting — Enhancement Pipeline

After importing raw SKILL.md files from a community repo, run the enhancement
pipeline to add proper Hermes format: trigger conditions, numbered procedures,
pitfalls sections, verification steps, and `metadata.hermes.tags`.

## Enhancement Structure

Each imported skill should gain:

| Section | Purpose | Detection |
|---------|---------|-----------|
| **Trigger** (`**Trigger**: Use when...`) | Agent routing signal — when to load this skill | Check for `**Trigger` or `## When to Use` in body |
| **Procedure** (`## Procedure`) | Numbered steps the agent executes | Check for `## Procedure`, `## Instructions`, `## Steps`, `## Workflow`, `## Algorithm` |
| **Pitfalls** (`## Pitfalls`) | Known failure modes | Check for `## Pitfalls` or `## Cautions` |
| **Verification** (`## Verification`) | Concrete checks to confirm success | Check for `## Verification` |
| **hermes_tags** (`metadata.hermes.tags`) | System-prompt indexing | Check for real populated tags under `hermes:` |

## Enhancement Code Pattern

```python
def enhance_skill(skill_name, enh):
    content = skill_file.read_text()
    fm, body = parse_frontmatter(content)
    changes = []

    # 1. Add trigger (prepend to body)
    trigger = enh.get("trigger")
    if trigger and not has_section_with_detection(body, "Trigger"):
        body = f"{trigger}\n\n{body}"
        changes.append("added trigger")

    # 2. Add pitfalls (append to body)
    pitfalls = enh.get("pitfalls", [])
    if pitfalls and not has_section_with_detection(body, "Pitfalls"):
        pit_text = "\n".join(f"- {p}" for p in pitfalls)
        body = f"{body}\n\n## Pitfalls\n{pit_text}"

    # 3. Add verification (append to body)
    verification = enh.get("verification", [])
    if verification and not has_section_with_detection(body, "Verification"):
        ver_text = "\n".join(f"- {v}" for v in verification)
        body = f"{body}\n\n## Verification\n{ver_text}"

    # 4. Add procedure (append to body) — DO NOT check for broad "How to"
    steps = enh.get("procedure_steps", [])
    has_procedure = any(has_section_with_detection(body, s)
                        for s in ["Procedure", "Instructions", "Steps", "Workflow", "Algorithm"])
    if steps and not has_procedure:
        step_text = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        body = f"{body}\n\n## Procedure\n{step_text}"

    # 5. Add hermes_tags to frontmatter
    if enh.get("hermes_tags"):
        # Check if metadata.hermes.tags already has real values
        has_real_tags = False
        if "metadata:" in content[:600] and "hermes:" in content[:600]:
            fm_section = content[3:content.find("---", 3)]
            in_hermes = False
            for line in fm_section.split("\n"):
                s = line.strip()
                if s.startswith("hermes:"):
                    in_hermes = True
                elif in_hermes and s.startswith("tags:"):
                    val = s.split(":", 1)[1].strip()
                    if val and val not in ("", "[]"):
                        has_real_tags = True
                        break
                elif in_hermes and not s.startswith((" ", "\t")):
                    in_hermes = False

        if not has_real_tags:
            # Insert before closing ---
            tag_line = f"\nmetadata:\n  hermes:\n    tags: [{', '.join(hermes_tags)}]"
            # ... insert into content_lines before the closing ---

    # Write back — CRITICAL: use enhanced body, not original content
    if not updated_fm:
        content = f"---\n{fmt_fm}---\n\n{body}"
    else:
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = f"---{parts[1]}---\n\n{body}"

    skill_file.write_text(content.strip() + "\n")
```

## Known Pitfalls (Discovered in Production)

### 1. Body Changes Lost When Frontmatter Is Updated

**Impact**: Skills that got `metadata.hermes.tags` added (`updated_fm = True`) lost
all body modifications — trigger, pitfalls, procedure, verification — because the
reconstruction code used the STALE body variable instead of the enhanced body.

**Fix**: Always use the enhanced `body` variable in both branches:

```python
if not updated_fm:
    content = f"---\n{fm_lines}---\n\n{body}"      # body is enhanced
else:
    parts = content.split("---", 2)
    content = f"---{parts[1]}---\n\n{body}"          # body is enhanced
```

**Verification**: After enhancement, read the file and check that both
`metadata.hermes.tags` AND procedural sections (Trigger, Pitfalls, etc.) exist.

### 2. False-Positive "How to" Section Detection

**Impact**: `has_section(body, "How to")` matched `## How to use this` in
pick-ui-library, preventing the Procedure section from being added.

**Root Cause**: The section existence check was too broad — `"How to"` appeared
as a substring in a legitimate section heading (`## How to use this`), not as a
procedure-like section.

**Fix**: Never check for `"How to"` as a procedure signal. Instead, check for
explicit procedure-like headings:

```python
has_procedure = any(has_section(body, s) for s in
    ["Procedure", "Instructions", "Steps", "Workflow", "Algorithm"])
```

### 3. `has_section()` Pattern Matching

The `has_section(body, name)` function checks multiple patterns case-insensitively:

```python
def has_section(body, name):
    patterns = [f"## {name}", f"**{name}**", f"### {name}",
                f"## When to {name}", f"*{name}*:"]
    return any(p.lower() in body.lower() for p in patterns)
```

Be careful that patterns don't over-match:
- `f"**{name}**"` with `name="How to"` matches `**How to choose a library**`
- Use the narrowest patterns that still catch the target sections

## Frontmatter Parsing

```python
def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text.strip()
    end = text.find("---", 3)
    if end == -1:
        return {}, text.strip()
    fm_text = text[3:end].strip()
    body = text[end+3:].strip()
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm, body
```

## Generic Enhancement Generation

For skills without custom enhancement entries, generate generic triggers based
on the skill name pattern:

```python
def generate_generic_enhancements():
    # Agent Platform skills
    for name in ["agent-platform-deploy", ...]:
        topic = name.replace("agent-platform-", "").replace("-", " ").title()
        yield name, {"hermes_tags": ["gcp", "agent-platform"],
                      "trigger": f"**Trigger**: Use when managing {topic}..."}

    # GKE skills
    for name in ["gke-networking", ...]:
        topic = name.replace("gke-", "").replace("-", " ").title()
        yield name, {"hermes_tags": ["gcp", "gke", "kubernetes"],
                      "trigger": f"**Trigger**: Use when working with GKE {topic}..."}
    # ... etc
```

## Verification After Enhancement

```bash
# Check all entries map to existing skills
python3 -c "
from pathlib import Path
ns = {}; exec(open('scripts/enhance-skills.py').read(), ns)
missing = [n for n in ns['ENHANCEMENTS'] if not (Path('skills') / n / 'SKILL.md').exists()]
print(f'Missing: {missing}' if missing else 'All OK')
"

# Spot-check body sections are actually in files
for s in handoff codebase-design gke-basics; do
    for section in '## Procedure' '## Pitfalls' '## Verification'; do
        grep -q "$section" "skills/$s/SKILL.md" || echo "MISSING $section in $s"
    done
done

# Verify FM tags + body both persisted (bug-fix check)
for s in animation-vocabulary handoff pick-ui-library; do
    t=$(cat "skills/$s/SKILL.md")
    echo "$s: fm=$(echo \"$t\" | head -15 | grep -c 'hermes_tags' || true)"
    echo "$s: body=$(echo \"$t\" | grep -c '## Procedure' || true)"
done
```
