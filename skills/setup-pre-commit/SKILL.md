---
name: setup-pre-commit
description: Use when setting up Husky pre-commit hooks with lint-staged and formatting
tags: [pre-commit, hooks, husky, lint-staged, prettier]
related_skills: [git-guardrails-claude-code, git-hooks-workflow]
---

# Setup Pre Commit

Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repository.

## What this sets up
- Husky pre-commit hook
- lint-staged running Prettier on all staged files
- Prettier config (if missing)
- Typecheck and test scripts in the pre-commit hook

## Steps
1. Detect package manager (npm, pnpm, yarn, bun)
2. Install: husky, lint-staged, prettier as devDependencies
3. Initialize Husky: npx husky init
4. Create .husky/pre-commit with lint-staged, typecheck, and test
5. Create .lintstagedrc with Prettier config
6. Create .prettierrc if missing
7. Verify everything is working

## Common Pitfalls

- **Missing package manager detection**: Check for package-lock.json, pnpm-lock.yaml, yarn.lock, bun.lockb before installing. Defaulting to npm may add the wrong lockfile.
- **Husky v9 does not need a shebang**: For Husky v9+, the .husky/pre-commit file does not need a shebang line. Adding one may cause issues.
- **Not checking for existing typecheck/test scripts**: If the repo has no typecheck or test script, omit those lines from the hook and tell the user.

## Verification Checklist

- [ ] Package manager detected correctly
- [ ] husky, lint-staged, prettier installed as devDependencies
- [ ] .husky/pre-commit exists and is executable
- [ ] .lintstagedrc exists with Prettier configuration
- [ ] .prettierrc exists (or Prettier config detected)
- [ ] prepare script in package.json is 'husky'
- [ ] Hook runs formatting, typecheck, and test on commit
