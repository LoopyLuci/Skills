"""
Robust frontmatter dedup: scans every SKILL.md in skills/, finds frontmatter
with duplicate keys (e.g. two `name:` or two `metadata:` lines), and rewrites
to keep the FIRST occurrence of each top-level key (preserving all sub-fields).

Uses a line-based parser that respects indentation (top-level keys start at
column 0). Nested keys under `metadata:` / `  hermes:` are preserved as-is
with the first `metadata:` block. Code fences within frontmatter are
preserved (they're part of frontmatter lines, not stripped).
"""
import pathlib
import yaml

ROOT = pathlib.Path(r"D:\Projects\Skills\skills")


def dedupe_frontmatter(text: str) -> str | None:
    """Return rewritten content if duplicates found, else None."""
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    fm_text = text[3:end]
    body = text[end + 3:]

    fm_lines = fm_text.split("\n")

    # Find top-level keys (col 0, key:) and track first occurrence index.
    top_keys = {}  # key -> first line index
    for i, line in enumerate(fm_lines):
        s = line.rstrip()
        if s and not s.startswith(" ") and not s.startswith("\t") and not s.startswith("#") and ":" in s:
            key = s.split(":", 1)[0].strip()
            if key not in top_keys:
                top_keys[key] = i

    # Check if there are any duplicates (more occurrences than first)
    has_dup = False
    for key, first_idx in top_keys.items():
        count = 0
        for line in fm_lines:
            s = line.rstrip()
            if s and not s.startswith(" ") and ":" in s and s.split(":",1)[0].strip() == key:
                count += 1
        if count > 1:
            has_dup = True

    if not has_dup:
        return None

    # Rewrite: keep first occurrence of each top-level key and its sub-lines.
    # Walk lines; when we hit a top-level key for the first time, keep it and
    # all following indented lines; when we hit it again, skip until next
    # top-level key.
    kept = []
    seen = set()
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        s = line.rstrip()
        is_top = (s and not s.startswith(" ") and not s.startswith("\t") and ":" in s and not s.startswith("#"))
        if is_top:
            key = s.split(":", 1)[0].strip()
            if key in seen:
                # Skip this key and all its indented sub-lines
                i += 1
                while i < len(fm_lines):
                    nl = fm_lines[i]
                    if nl.rstrip() and not nl.startswith(" ") and not nl.startswith("\t") and ":" in nl and not nl.startswith("#"):
                        break # next top-level key
                    i += 1
                continue
            else:
                seen.add(key)
        kept.append(line)
        i += 1

    new_fm = "\n".join(kept)
    result = "---\n" + new_fm + "\n---\n\n" + body.strip() + "\n"
    return result


def main():
    fixed = 0
    checked = 0
    parse_errors = []
    for f in sorted(ROOT.rglob("SKILL.md")):
        checked += 1
        orig = f.read_text(encoding="utf-8")
        result = dedupe_frontmatter(orig)
        if result is None:
            # Still verify it parses as valid YAML
            if orig.startswith("---"):
                end = orig.find("---", 3)
                if end > 0:
                    fm = orig[3:end]
                    try:
                        yaml.safe_load(fm)
                    except yaml.YAMLError:
                        parse_errors.append(str(f.relative_to(f.parents[2])))
            continue
        f.write_text(result, encoding="utf-8")
        fixed += 1
        # Verify it now parses
        end = result.find("---", 3)
        try:
            yaml.safe_load(result[3:end])
        except yaml.YAMLError as e:
            print(f"  WARN still-broken: {f.name}: {e}")
    print(f"\nChecked {checked} SKILL.md")
    print(f"Fixed {fixed} with duplicate frontmatter keys")
    print(f"Still unparseable: {len(parse_errors)}")
    for p in parse_errors[:10]:
        print(f"  - {p}")
    return 0


if __name__ == "__main__":
    main()
