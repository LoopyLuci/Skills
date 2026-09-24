---
name: critical-thinking-framework
description: "Use when applying critical thinking frameworks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: ['c', 'r', 'i', 't', 'i', 'c', 'a', 'l', '-', 't', 'h', 'i', 'n', 'k', 'i', 'n', 'g', ',', ' ', 'r', 'e', 'a', 's', 'o', 'n', 'i', 'n', 'g']
    related_skills: [general]
---

# Critical Thinking Framework

"Use when applying critical thinking frameworks."

## Trigger

Activate this skill when the user mentions:
- 'c',  'r',  'i',  't',  'i',  'c',  'a',  'l',  '-',  't',  'h',  'i',  'n',  'k',  'i',  'n',  'g',  ',  ',  ' ',  'r',  'e',  'a',  's',  'o',  'n',  'i',  'n',  'g' workflows or issues
- Building, fixing, or optimizing critical thinking framework
- Questions about 'c' best practices

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

`'c', 'r', 'i', 't', 'i', 'c', 'a', 'l', '-', 't', 'h', 'i', 'n', 'k', 'i', 'n', 'g', ', ', ' ', 'r', 'e', 'a', 's', 'o', 'n', 'i', 'n', 'g'`

---

*LoopyLuci/Skills - 2026-09-24*
