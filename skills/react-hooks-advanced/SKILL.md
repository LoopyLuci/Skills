---
name: react-hooks-advanced
description: "Use when implementing advanced React hooks patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [react, hooks, useReducer, useContext, custom-hooks, performance]
    related_skills: [typescript-advanced-types, frontend-bootstrap, graphql-client-patterns]
---

# Advanced React Hooks

Implementing advanced React hooks — from custom hooks composition through useReducer patterns, context optimization, and performance hooks.

## When to Use

- Building complex React components with hooks
- Optimizing React render performance
- Composing custom hooks
- State management with useReducer

## Hook Patterns

```typescript
import { useState, useCallback, useMemo, useRef, useReducer } from 'react';

// Custom hook composition
function useUserData(userId: string) {
  const { data, loading } = useFetch(`/api/users/${userId}`);
  const { update } = useMutate(`/api/users/${userId}`);
  const notifications = useNotifications();
  
  return { user: data, loading, update, notifications };
}

// useReducer with action types
type Action = 
  | { type: 'INCREMENT'; payload: number }
  | { type: 'RESET' }
  | { type: 'SET'; payload: number };

function counterReducer(state: number, action: Action): number {
  switch (action.type) {
    case 'INCREMENT': return state + action.payload;
    case 'RESET': return 0;
    case 'SET': return action.payload;
  }
}
```

## Verification Checklist

- [ ] Custom hooks compose business logic
- [ ] useMemo/useCallback prevent unnecessary re-renders
- [ ] useRef for mutable values without re-render
- [ ] useReducer for complex state logic
- [ ] Context splitting to prevent unnecessary renders
- [ ] Custom hooks tested independently
