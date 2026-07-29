---
name: graphql-api-implementation
description: "Use when implementing GraphQL APIs and servers."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [graphql, API, schema, resolvers, Apollo, Relay, federation]
    related_skills: [api-design-rest-graphql, microservices-decomposition, api-testing-patterns, oauth-authentication-patterns]
---

# GraphQL API Implementation

Designing and implementing GraphQL APIs — from schema design and resolvers through subscriptions, federation, caching, and security.

## When to Use

- Building flexible APIs where clients control response shape
- Reducing over-fetching and under-fetching (vs REST)
- Implementing real-time subscriptions
- Aggregating data from multiple sources (federation)
- Mobile apps needing efficient data loading

## Schema Design

```python
SCHEMA_TEMPLATE = """
type Query {
  user(id: ID!): User
  users(page: Int, limit: Int): UserConnection!
  search(query: String!): [SearchResult!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  userCreated: User!
  userUpdated(id: ID!): User!
}

type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

input CreateUserInput {
  name: String!
  email: String!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}
"""
```

## Common Pitfalls

1. **N+1 problem** — loading related objects causes many DB queries; use DataLoader
2. **Overly deep queries** — malicious queries can cause performance issues; set depth limits
3. **No caching** — POST requests don't cache naturally; use automatic persisted queries, CDN
4. **Schema debt** — fields that should be deprecated linger forever; use deprecation reason
5. **Auth in resolvers** — authorization must be uniform, not scattered across resolvers

## Verification Checklist

- [ ] Schema follows conventions (types, inputs, enums, pagination)
- [ ] DataLoader implemented for batching
- [ ] Query complexity/depth limiting configured
- [ ] Authentication middleware at transport level
- [ ] Authorization in business logic layer (not resolvers)
- [ ] Subscriptions secured (auth on connect)
- [ ] Federation-ready (if multiple services)
