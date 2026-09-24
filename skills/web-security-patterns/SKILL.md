---
name: web-security-patterns
description: "Use when implementing web application security patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-security, OWASP, XSS, CSRF, SQL-injection, secure-coding]
    related_skills: [cryptography-implementation-patterns, api-design-rest-graphql, api-gateway-load-balancing, frontend-bootstrap]
---

# Web Security Patterns

"Use when implementing web application security patterns."

## Trigger

Activate this skill when the user mentions:
- web-security,  OWASP,  XSS,  CSRF,  SQL-injection,  secure-coding workflows or issues
- Building, fixing, or optimizing web security patterns
- Questions about web-security best practices

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

`web-security, OWASP, XSS, CSRF, SQL-injection, secure-coding`

---

*LoopyLuci/Skills - 2026-09-24*
