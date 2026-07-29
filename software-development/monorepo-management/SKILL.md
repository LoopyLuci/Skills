---
name: monorepo-management
description: "Use when managing monorepo structures and tooling."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [monorepo, nx, turborepo, lerna, pnpm, workspace, build-system]
    related_skills: [git-for-windows, ci-cd-pipeline-setup, project-scaffolding, dependency-management]
---

# Monorepo Management

Managing monorepo structures — from choosing tools (Nx, Turborepo, Lerna, pnpm workspaces) through dependency management, build caching, and CI optimization.

## When to Use

- Multiple packages/applications sharing code
- Building a design system with shared components
- Managing microservices in a single repository
- Sharing TypeScript types, utilities, or configs across projects

## Tool Comparison

```python
MONOREPO_TOOLS = {
    'nx': {
        'features': 'Build caching, dependency graph, distributed execution, generators',
        'best_for': 'Large enterprises, multiple apps, complex dependency graphs',
        'learning_curve': 'Medium',
    },
    'turborepo': {
        'features': 'Remote caching, parallel builds, task orchestration',
        'best_for': 'Medium-sized monorepos, Vercel ecosystem',
        'learning_curve': 'Low',
    },
    'pnpm_workspaces': {
        'features': 'Efficient disk usage, strict isolation, workspace protocol',
        'best_for': 'Simple monorepos, npm ecosystem compatibility',
        'learning_curve': 'Low',
    },
}

def mono_repo_structure() -> str:
    return """
my-mono-repo/
├── apps/
│   ├── web/        # Next.js app
│   └── api/        # Express API
├── packages/
│   ├── shared/     # Shared types and utilities
│   ├── ui/         # Design system components
│   └── config/     # Shared ESLint, TS configs
├── tools/
│   └── scripts/    # Build and CI scripts
├── pnpm-workspace.yaml
├── nx.json
└── package.json
"""
```

## Common Pitfalls

1. **No build caching** — rebuilding all packages wastes CI time; invest in caching
2. **Circular dependencies** — packages depending on each other; enforce with tooling
3. **Slow git operations** — large monorepos have slow clone/fetch; use sparse checkout
4. **No code ownership** — unclear who can modify which packages; use CODEOWNERS
5. **Over-sharing** — packages coupling to internal packages too tightly; define public APIs

## Verification Checklist

- [ ] Package dependency graph visualized and acyclic
- [ ] Build caching configured (local + remote)
- [ ] Affected command works for selective builds
- [ ] Test execution scoped to affected packages
- [ ] Code ownership defined per package
- [ ] Linting/formatting consistent across all packages
