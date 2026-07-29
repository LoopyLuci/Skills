---
name: graphql-client-patterns
description: "Use when implementing GraphQL client patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [graphql, client, Apollo, Relay, queries, mutations, subscriptions, caching]
    related_skills: [graphql-api-implementation, api-testing-patterns, frontend-bootstrap, caching-strategies]
---

# GraphQL Client Patterns

Implementing GraphQL client patterns — from query composition and fragment management through Apollo/Relay client setup, caching, optimistic updates, and pagination.

## When to Use

- Building frontend apps that consume GraphQL APIs
- Managing GraphQL queries, mutations, and subscriptions
- Implementing client-side caching and optimistic UI
- Handling pagination (cursor, offset, infinite scroll)
- Type-safe GraphQL operations with codegen

## Client Patterns

```python
CLIENT_PATTERNS = {
    'fragments': 'Reusable field selections that compose into queries',
    'pagination': 'Relay-style cursor pagination vs offset-based',
    'optimistic_update': 'Immediately update UI before server confirms mutation',
    'subscriptions': 'WebSocket-based real-time updates for live data',
    'normalized_cache': 'Apollo/Relay cache normalizes by __typename + id',
}

# Apollo Client setup (React)
APOLLO_SETUP = """
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';

const client = new ApolloClient({
  link: createHttpLink({ uri: '/graphql' }),
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          posts: {
            merge(existing, incoming) {
              return incoming;
            }
          }
        }
      }
    }
  })
});
"""
```

## Verification Checklist

- [ ] Fragments used for reusable field selections
- [ ] Pagination strategy chosen (cursor or offset)
- [ ] Client cache configured (normalized, type policies)
- [ ] Optimistic updates for key mutations (create, update)
- [ ] Error handling for failed operations (network, GraphQL errors)
- [ ] Type-safe (GraphQL Codegen)
- [ ] Subscriptions with reconnection logic
