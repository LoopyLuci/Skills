---
name: verification-before-completion
description: Use when verifying work is complete before merging or deploying
tags: [verification, testing, quality, completion]
related_skills: [finishing-a-development-branch, test-driven-development]
---

# Verification Before Completion

## Overview

Before declaring work complete, run through a systematic verification checklist. Never skip this step — it catches issues that tests alone miss.

## Verification Checklist

### 1. Code Quality
- [ ] All tests pass (including new ones)
- [ ] Linting passes with zero warnings
- [ ] Type checking passes
- [ ] No dead code, commented-out code, or debug logging
- [ ] No TODO/FIXME/HACK comments left behind
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] Error handling is appropriate (not swallowing errors)
- [ ] Edge cases considered (empty states, errors, boundary values)

### 2. Architecture & Design
- [ ] Changes follow existing patterns and conventions
- [ ] No unnecessary abstractions or over-engineering
- [ ] Separation of concerns maintained
- [ ] public/API surface is intentional (not accidentally exposed)
- [ ] Dependencies are necessary (no new deps without reason)

### 3. Documentation
- [ ] README updated if behavior changed
- [ ] Inline comments explain WHY, not WHAT
- [ ] API docs updated if interfaces changed
- [ ] Changelog updated if relevant

### 4. Security
- [ ] Input validation present where needed
- [ ] No injection vulnerabilities
- [ ] Authentication/authorization checks in place
- [ ] Sensitive data not logged or exposed

### 5. Performance
- [ ] No N+1 queries introduced
- [ ] No unnecessarily expensive operations
- [ ] Assets optimized (if applicable)

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Trusting tests alone | Tests don't catch all issues — run the full checklist |
| Skipping "minor" checks | Small issues compound — fix everything |
| Rushing through verification | Take time — verification prevents production incidents |
| Ignoring warnings | Every warning has meaning — address them |
| Not checking edge cases | Happy path isn't enough — test boundaries and errors |

## Verification Checklist (Quick Reference)

```
□ All tests pass
□ Lint/type checking clean
□ No TODOs or debug code
□ Error handling complete
□ Follows project conventions
□ Documentation updated
□ Security review done
□ Performance impact assessed
```
