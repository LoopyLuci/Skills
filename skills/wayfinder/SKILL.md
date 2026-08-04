---
name: wayfinder
description: Use when navigating a codebase or project to understand its structure and conventions
tags: [navigation, exploration, onboarding, discovery, codebase]
related_skills: [ask-matt, codebase-design, codebase-onboarding]
---

# Wayfinder

Navigate and explore a new codebase to understand its structure, conventions, and domain terminology quickly.

## Process
1. **Read CONTEXT.md** (if it exists) for the domain model
2. **Map top-level directory structure** - identify entry points, modules, and config
3. **Find entry points** - main files, index files, public API surfaces
4. **Review README and docs** - understand conventions and patterns
5. **Read key tests** - tests reveal how the code is supposed to work
6. **Build a mental model** and document it for future reference

## Output
Document the codebase structure, key entry points, testing patterns, and module relationships so you and other skills can navigate efficiently.

## Common Pitfalls

- **Not reading CONTEXT.md or domain docs first**: Understanding the domain model before diving into code saves time. Skip the documents and you navigate blind.
- **Going too deep too fast**: Start with the directory structure and entry points. Do not dive into implementation details until you know the overall shape.
- **Not building a mental model incrementally**: Document what you learn as you go. Mental models fade; written notes persist and can be shared.

## Verification Checklist

- [ ] Directory structure mapped
- [ ] Entry points identified
- [ ] Domain documents read (CONTEXT.md, ADRs, etc.)
- [ ] Testing patterns understood
- [ ] Mental model documented
