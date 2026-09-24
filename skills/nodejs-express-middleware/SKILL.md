---
name: nodejs-express-middleware
description: Use when implementing Express middleware.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [express, middleware, auth, logging, error]
---

# Nodejs Express Middleware

"Use when implementing Express middleware."

## Trigger

Activate this skill when the user mentions:
- "express",  "middleware",  "auth",  "logging",  "error" workflows or issues
- Building, fixing, or optimizing nodejs express middleware
- Questions about "express" best practices

## Core Concepts

- Language-specific idioms and best practices
- Package/module organization
- Error handling and logging patterns
- Testing methodology (unit, integration, e2e)
- Build, lint, and format tooling

## Step-by-Step Workflow

1. **Setup** — Initialize project, install dependencies, configure tooling
   - Expected: Working dev environment
2. **Implement** — Write core logic following idiomatic patterns
   - Expected: Functional code with passing tests
3. **Test** — Write and run tests covering happy path and edge cases
   - Expected: All tests pass, >80% coverage
4. **Review** — Self-review for code quality, performance, security
   - Expected: Clean, documented production-ready code
5. **Deliver** — Commit, document, and verify end-to-end
   - Expected: Working feature with tests and docs

## Tools & Technologies

- Language-specific package manager
- Test framework
- Linter/Formatter
- Build system
- Debugging tools

## Best Practices

- Document decisions and rationale (ADRs, design docs, runbooks)
- Version everything - code, configs, data, and documentation
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethical standards
- Measure outcomes with meaningful metrics

## Common Pitfalls

- **Skipping error handling** → Silent failures → Always handle errors explicitly
- **Over-engineering** → Unnecessary complexity → Add abstraction only when needed
- **Missing tests** → Regression bugs → Write tests alongside code

## Tags

`"express", "middleware", "auth", "logging", "error"`

---

*LoopyLuci/Skills - 2026-09-24*
