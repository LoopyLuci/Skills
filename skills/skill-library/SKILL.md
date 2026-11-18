---
name: skill-library
description: Searches LoopyLuci's library of 10,000+ specialised skills (software, cloud, security, data/AI, science, business, engineering, design and more) and loads the one that fits, only when it's needed. Use it at the start of any specialised or domain-specific task (a framework, a cloud service, a scientific or business method, a file format, a security review, an industry workflow) to check whether a ready-made skill covers it, and whenever the user mentions their skills, the skill library, or asks "is there a skill for this".
version: 1.0.0
author: LoopyLuci
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [meta, skills, search, library]
---

# Skill library

LoopyLuci's library holds over 10,000 skills. Enabling them all would put every description into every conversation, so they stay on disk and this skill finds and loads the right one on demand.

## How to use it

1. **Search** with a few keywords from the task (the technology, the domain, the action):

   ```bash
   python <this skill's folder>/scripts/find_skill.py "terraform aws vpc" --limit 8
   ```

   Add `--category "Cybersecurity"` to narrow by category, or `--tag kubernetes` to require a tag. `--categories` lists the categories with their counts. The script prints each match's name, category, score, description and the path of its `SKILL.md`.

2. **Pick** the best match by its description, not just its score. If nothing fits well (all scores low, or the descriptions are about something else), say so and carry on without a skill: a poor match is worse than none.

3. **Load** it: read the chosen `SKILL.md` in full and follow it for the task, including any `references/`, `scripts/` or `templates/` it points to (they sit beside it). Load more than one only when the task clearly spans them.

4. **Tell the user** in one line which skill you loaded, so they can redirect you.

Searching is cheap, so search again when the task moves to a new area instead of stretching one skill to cover it.
