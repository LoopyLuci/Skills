#!/usr/bin/env python3
"""
Bulk Skill Generator — Generate hundreds of skills from a JSON/CSV specification.

JSON format (skills.json):
[
  {"name": "my-skill", "description": "Does X", "tags": ["python", "cli"]},
  {"name": "other-skill", "description": "Does Y", "tags": ["web", "react"]}
]

CSV format (skills.csv):
name,description,tags
my-skill,Does X,"python, cli"
other-skill,Does Y,"web, react"

Usage:
  python bulk_generate.py skills.json --apply
  python bulk_generate.py skills.csv --apply --format csv
  python bulk_generate.py skills.json --dry-run
"""
import argparse
import csv
import json
import sys
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from generate_skill import generate_skill, detect_category, REPO_SKILLS


def load_skills(input_path, fmt=None):
    """Load skill specifications from file."""
    path = Path(input_path)
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return []

    if fmt is None:
        fmt = path.suffix.lower().lstrip('.')

    skills = []
    if fmt == 'json':
        with open(path, encoding='utf-8') as f:
            skills = json.load(f)
    elif fmt in ('csv', 'tsv'):
        delimiter = '\t' if fmt == 'tsv' else ','
        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                tags = row.get('tags', '')
                if isinstance(tags, str):
                    tags = [t.strip() for t in tags.split(',') if t.strip()]
                skills.append({
                    'name': row['name'].strip(),
                    'description': row['description'].strip(),
                    'tags': tags,
                })
    else:
        print(f"ERROR: Unsupported format: {fmt}")
        return []

    return skills


def main():
    parser = argparse.ArgumentParser(description='Bulk generate skills')
    parser.add_argument('input', help='Input file (JSON/CSV)')
    parser.add_argument('--format', '-f', choices=['json', 'csv', 'tsv'], help='File format')
    parser.add_argument('--apply', action='store_true', help='Create skills (default: dry-run)')
    parser.add_argument('--offset', type=int, default=0, help='Start offset for batch processing')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of skills to process')
    args = parser.parse_args()

    skills = load_skills(args.input, args.format)
    if not skills:
        return

    if args.offset or args.limit:
        start = args.offset
        end = start + args.limit if args.limit else len(skills)
        skills = skills[start:end]

    print(f"=== Bulk Generation ===")
    print(f"  Total: {len(skills)}")
    print(f"  Mode: {'CREATE' if args.apply else 'DRY-RUN'}")
    print()

    created = 0
    exists = 0
    errors = 0

    for i, spec in enumerate(skills):
        name = spec.get('name', '').strip()
        description = spec.get('description', '').strip()
        tags = spec.get('tags', [])

        if not name:
            print(f"  [{i+1}] SKIP: Missing name")
            continue

        if not description:
            description = f"Skill for {name.replace('-', ' ')}"

        if not tags:
            tags = [name.split('-')[0], 'general']

        result = generate_skill(name, description, tags, apply=args.apply)
        status = result['status']

        if status == 'created':
            created += 1
        elif status == 'exists':
            exists += 1
        else:
            errors += 1

        if (i + 1) % 100 == 0:
            print(f"  Processed {i+1}/{len(skills)}...")

    print()
    print(f"=== Complete ===")
    print(f"  Created: {created}")
    print(f"  Exists (skipped): {exists}")
    print(f"  Errors: {errors}")


if __name__ == "__main__":
    main()
