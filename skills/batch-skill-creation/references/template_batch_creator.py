# Reusable Batch Skill Creator Template
# Copy this file, edit the DOMAINS list, and run via execute_code or terminal
# Each domain produces 4 skills: fundamentals, implementation, best-practices, troubleshooting

import os

SKILLS_DIR = "C:/Users/dubem/AppData/Local/hermes/skills"
existing = set(
    d for d in os.listdir(SKILLS_DIR)
    if os.path.isdir(os.path.join(SKILLS_DIR, d)) and not d.startswith('.')
)

def desc_ok(d: str) -> bool:
    """Validate description: ≤60 chars, starts 'Use when', ends with '.'"""
    return len(d) <= 59 and d.startswith("Use when") and d.endswith(".")

def make_skill(name: str, desc: str, tags: str, overview: str, related: str = "") -> bool:
    """Create a skill directory with SKILL.md. Returns True if created, False if skipped."""
    if name in existing:
        return False
    if not desc_ok(desc):
        return False
    
    related_str = "'{0}'".format(related.replace(",", "', '")) if related else "''"
    
    body = "## Overview\n" + overview + "\n\n## When to Use\n- Apply domain best practices\n\n## Key Approaches\n1. Define requirements\n2. Choose tools\n3. Implement\n4. Test\n5. Document\n6. Monitor\n\n## Common Pitfalls\n1. Ignoring constraints\n2. Skipping standards\n3. Poor alignment\n\n## Verification Checklist\n- [ ] Requirements validated\n- [ ] Standards applied\n- [ ] Design reviewed\n\n"
    
    md = "---\nname: {0}\ndescription: \"{1}\"\nversion: 1.0.0\nauthor: Hermes Agent\nlicense: MIT\nplatforms: [linux, macos, windows]\nmetadata:\n  hermes:\n    tags: [{2}]\n    related_skills: [{3}]\n---\n\n{4}".format(name, desc, tags, related_str, body)
    
    path = os.path.join(SKILLS_DIR, name)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(md)
    return True


# ============================================================
# EDIT THIS LIST: Each tuple = (prefix, label, overview, tags, related_skill)
# ============================================================
DOMAINS = [
    # Example entries - replace with your domains:
    ("supply-chain", "Supply Chain", "Manage supply chain operations.", "supply-chain, logistics, procurement", "supply-chain-management"),
    ("logistics", "Logistics", "Plan and execute logistics.", "logistics, delivery, shipping", "logistics-management"),
    ("procurement", "Procurement", "Manage purchasing and sourcing.", "procurement, purchasing, sourcing", "vendor-management"),
    # Add more domains here...
]

# ============================================================
# GENERATION LOOP (do not modify)
# ============================================================
SUFFIXES = [
    ("-fundamentals", "for {label.lower()} fundamentals."),
    ("-implementation", "for {label.lower()} implementation."),
    ("-best-practices", "for {label.lower()} best practices."),
    ("-troubleshooting", "for {label.lower()} troubleshooting."),
]

created = 0
skipped = 0

for prefix, label, overview, tags, related in DOMAINS:
    for suffix, desc_suffix in SUFFIXES:
        name = prefix + suffix
        desc = "Use when applying " + desc_suffix.format(label=label)
        if len(desc) > 59:
            desc = desc[:56] + "."
        
        if make_skill(name, desc, tags, overview, related):
            created += 1
        else:
            skipped += 1

print(f"Created: {created}")
print(f"Skipped: {skipped}")

# ============================================================
# VERIFICATION
# ============================================================
total = sum(
    1 for d in os.listdir(SKILLS_DIR)
    if os.path.isdir(os.path.join(SKILLS_DIR, d))
    and os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md"))
    and not d.startswith('.')
)
print(f"Total skills in library: {total}")
print(f"Progress to 50,000: {total/50000*100:.1f}%")