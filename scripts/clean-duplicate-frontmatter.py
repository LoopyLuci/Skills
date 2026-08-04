"""
One-pass cleaner: fixes SKILL.md files in D:\Projects\Skills\skills that have
duplicate 'name:' or 'metadata:' keys (produced by an earlier import run).
Rewrites frontmatter: keeps the FIRST name/source, drops duplicate metadata
blocks keeping only the hermes sub-block, and ensures exactly one metadata
key. Non-frontmatter content is left untouched.
"""
import pathlib

ROOT = pathlib.Path(r"D:\Projects\Skills\skills")


def clean_frontmatter(content: str) -> str | None:
    if not content.startswith("---"):
        return None
    end = content.find("---", 3)
    if end == -1:
        return None
    fm = content[3:end]
    body = content[end + 3:]

    lines = fm.split("\n")
    seen_name = False
    seen_source = False
    seen_metadata = False
    kept = []
    skip_metadata_block = False
    for line in lines:
        s = line.strip()
        if s.startswith("name:"):
            if seen_name:
                continue  # skip duplicate
            seen_name = True
            kept.append(line)
            continue
        if s.startswith("source:"):
            if seen_source:
                continue
            seen_source = True
            kept.append(line)
            continue
        if s.startswith("metadata:"):
            if seen_metadata:
                skip_metadata_block = True
                continue
            seen_metadata = True
            skip_metadata_block = False
            kept.append(line)
            continue
        if skip_metadata_block and (s.startswith("  hermes:") or s.startswith("    tags:") or s.startswith("    category:") or s.startswith("    ")):
            continue
        if not skip_metadata_block:
            kept.append(line)

    return "---\n" + "\n".join(kept) + "\n---\n\n" + body.strip() + "\n"


def main():
    fixed = 0
    checked = 0
    for f in ROOT.rglob("SKILL.md"):
        checked += 1
        orig = f.read_text(encoding="utf-8")
        name_count = orig.count("\nname:") + (1 if orig.startswith("name:") else 0)
        md_count = orig.count("\nmetadata:") + (1 if orig.startswith("metadata:") else 0)
        if name_count <= 1 and md_count <= 1:
            continue
        cleaned = clean_frontmatter(orig)
        if cleaned is not None:
            f.write_text(cleaned, encoding="utf-8")
            fixed += 1
            print(f"  fixed {f.relative_to(ROOT.parent)}")
    print(f"\nChecked {checked} SKILL.md, fixed {fixed} with duplicate frontmatter")
    return 0


if __name__ == "__main__":
    main()
