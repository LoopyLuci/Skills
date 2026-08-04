---
name: migrate-to-shoehorn
description: Use when migrating test files from 'as' assertions to @total-typescript/shoehorn
tags: [TypeScript, testing, migration, shoehorn, type-safety]
related_skills: [migrate-to-shoehorn, code-review]
---

# Migrate To Shoehorn

Migrate test files from `as` type assertions to @total-typescript/shoehorn for type-safe partial test data.

## Why shoehorn?
`shoehorn` lets you pass partial data in tests while keeping TypeScript happy. It replaces `as` assertions with type-safe alternatives.

**Test code only.** Never use shoehorn in production code.

## Migration patterns
- Large objects with few needed properties: `as Type` -> `fromPartial()`
- Intentionally wrong types: `as unknown as Type` -> `fromAny()`

### Install
```bash
npm install @total-typescript/shoehorn
```

## Common Pitfalls

- **Shoehorn in production code**: Never use shoehorn (fromPartial, fromAny) in production code. It is for test files only.
- **Not installing the package first**: Run npm install @total-typescript/shoehorn before attempting migration.
- **fromAny where fromPartial would work**: Use fromPartial when you have a valid partial object, fromAny only when intentionally providing wrong types.

## Code Examples

```typescript
// BEFORE: Using as assertions
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
};

getUser({ body: { id: "123" } } as Request);

// AFTER: Using fromPartial
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));

// Intentionally wrong types
// BEFORE:
getUser({ body: { id: 123 } } as unknown as Request);

// AFTER:
import { fromAny } from "@total-typescript/shoehorn";
getUser(fromAny({ body: { id: 123 } }));
```

## Verification Checklist

- [ ] @total-typescript/shoehorn installed (npm)
- [ ] All `as Type` assertions in tests migrated to fromPartial()
- [ ] All `as unknown as Type` migrated to fromAny()
- [ ] Production code checked for shoehorn usage (should be none)
- [ ] Tests still passing after migration
