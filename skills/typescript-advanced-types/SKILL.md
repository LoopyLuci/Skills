---
name: typescript-advanced-types
description: "Use when implementing advanced TypeScript type patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [typescript, generics, conditional-types, mapped-types, utility-types]
    related_skills: [python-typing-advanced, react-hooks-advanced, type-system-design-theory]
---

# Advanced TypeScript Types

Implementing advanced TypeScript type patterns — from conditional and mapped types through template literals, infer, and type-level programming.

## When to Use

- Building type-safe TypeScript libraries
- Implementing complex type transformations
- Generic utility types
- Type-level validation and parsing

## TypeScript Type Patterns

```typescript
// Conditional types with infer
type UnpackPromise<T> = T extends Promise<infer U> ? U : T;
type Result = UnpackPromise<Promise<string>>; // string

// Mapped types with key remapping
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
};

// Template literal types
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<'click'>; // 'onClick'

// Discriminated union pattern
type ApiResult<T> = 
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }
  | { status: 'loading' };
```

## Verification Checklist

- [ ] Conditional types with infer for unwrapping
- [ ] Mapped types with key remapping and filtering
- [ ] Template literal types for string manipulation
- [ ] Recursive type aliases
- [ ] Discriminated unions for state modeling
- [ ] satisfies operator for type validation (TS 4.9+)
