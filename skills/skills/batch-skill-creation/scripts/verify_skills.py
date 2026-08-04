#!/usr/bin/env python3
"""Verify skill library after batch creation.
Usage: python verify_skills.py [skills_dir]
"""
import os
import re
import sys
import yaml

SKILLS_DIR = sys.argv[1] if len(sys.argv) > 1 else "C:/Users/dubem/AppData/Local/hermes/skills"

def verify_skill(skill_dir: str) -> dict:
    """Verify a single skill's SKILL.md. Returns dict with results."""
    skill_path = os.path.join(SKILLS_DIR, skill_dir, "SKILL.md")
    if not os.path.exists(skill_path):
        return {"skill": skill_dir, "valid": False, "errors": ["SKILL.md not found"]}
    
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    errors = []
    warnings = []
    
    # Check YAML frontmatter
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter (---)")
    else:
        try:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                yaml_content = parts[1].strip()
                meta = yaml.safe_load(yaml_content)
                
                # Required fields
                for field in ["name", "description", "version", "author", "license", "platforms", "metadata"]:
                    if field not in meta:
                        errors.append(f"Missing required field: {field}")
                
                # Description validation
                if "description" in meta:
                    desc = meta["description"]
                    if len(desc) > 59:
                        errors.append(f"Description too long ({len(desc)} chars): {desc[:80]}...")
                    if not desc.startswith("Use when"):
                        errors.append(f"Description doesn't start with 'Use when': {desc[:80]}...")
                    if not desc.endswith("."):
                        errors.append(f"Description doesn't end with period: {desc[:80]}...")
                
                # Metadata structure
                if "metadata" in meta and "hermes" in meta["metadata"]:
                    hermes = meta["metadata"]["hermes"]
                    if "tags" not in hermes:
                        warnings.append("Missing 'tags' in metadata.hermes")
                    if "related_skills" not in hermes:
                        warnings.append("Missing 'related_skills' in metadata.hermes")
                        
        except yaml.YAMLError as e:
            errors.append(f"YAML parse error: {e}")
    
    # Check required sections
    required_sections = ["## Overview", "## When to Use", "## Key Approaches", "## Common Pitfalls", "## Verification Checklist"]
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")
    
    # Check for placeholder content
    if "example-domain" in content.lower() or "example domain" in content.lower():
        warnings.append("Contains placeholder 'example-domain'")
    
    return {
        "skill": skill_dir,
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def main():
    print("=" * 60)
    print("SKILL LIBRARY VERIFICATION")
    print("=" * 60)
    
    skill_dirs = [d for d in os.listdir(SKILLS_DIR) 
                  if os.path.isdir(os.path.join(SKILLS_DIR, d)) and not d.startswith('.')]
    
    print(f"Found {len(skill_dirs)} skill directories")
    
    valid = 0
    invalid = 0
    total_errors = 0
    total_warnings = 0
    
    for skill_dir in skill_dirs:
        result = verify_skill(skill_dir)
        if result["valid"]:
            valid += 1
        else:
            invalid += 1
            print(f"\n❌ {skill_dir}:")
            for err in result["errors"]:
                print(f"  ERROR: {err}")
                total_errors += 1
        
        if result["warnings"]:
            for warn in result["warnings"]:
                print(f"  ⚠️  {skill_dir}: {warn}")
                total_warnings += 1
        
        if invalid % 100 == 0 and invalid > 0:
            print(f"  ... {invalid} invalid so far")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY:")
    print(f"  Total skills:    {len(skill_dirs)}")
    print(f"  Valid:           {valid}")
    print(f"  Invalid:         {invalid}")
    print(f"  Total errors:    {total_errors}")
    print(f"  Total warnings:  {total_warnings}")
    print(f"  Success rate:    {valid/len(skill_dirs)*100:.1f}%")
    print("=" * 60)
    
    # Check total count
    total_skills = sum(
        1 for d in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, d))
        and os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md"))
        and not d.startswith('.')
    )
    print(f"\nTotal SKILL.md files: {total_skills}")
    print(f"Progress to 50,000: {total_skills/50000*100:.1f}%")

if __name__ == "__main__":
    main()