---
name: setup-ts-deep-modules
description: Use when setting up TypeScript deep modules with dependency-cruiser enforcement
tags: [TypeScript, modules, dependency-cruiser, architecture, encapsulation]
related_skills: [codebase-design, setup-matt-pocock-skills]
---

# Setup Ts Deep Modules

Make every package in a TypeScript monorepo a deep module using dependency-cruiser to enforce entry-point boundaries.

## The shape this enforces
```
src/packages/
  <name>/
    index.ts        - an entry point (public)
    client.ts       - another entry point (packages may expose several)
    lib/            - implementation: hidden from outside
    tests/          - co-located tests + fixtures (private)
```

## Four rules (all error level)
1. **Entry-point boundary** - code outside a package may import only root files
2. **Intra-package freedom** - a package's own files import each other freely
3. **Tests through entry points** - test files import entry points only
4. **No circular dependencies** between packages

## Setup
1. Install dependency-cruiser
2. Create the configuration with the four rules
3. Run initial lint to find violations
4. Fix or accept existing violations before enforcement

## Common Pitfalls

- **Not running the verification after setup**: The skill includes a verification step that proves the rules bite. Skipping it means you will not know if the setup worked.
- **Existing code that violates the new rules**: The initial lint run will likely catch existing violations. Decide whether to fix them before or after enforcing the rules.
- **Entry points that export too much**: A package's root files are its public API. Barrel files that re-export everything undermine the deep module pattern.

## Verification Checklist

- [ ] dependency-cruiser installed
- [ ] Configuration created with 4 rules
- [ ] Initial lint run completed
- [ ] Existing violations identified
- [ ] Entry point boundaries enforced
