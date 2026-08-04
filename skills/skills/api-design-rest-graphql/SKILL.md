---
name: api-design-rest-graphql
description: "Use when designing REST or GraphQL API architectures."
category: software-development
tags: [api, rest, graphql, design, architecture]
---
# API Design: REST & GraphQL

Designing robust REST and GraphQL APIs.

## REST Design Principles

```
GET    /api/v1/models          → List models
GET    /api/v1/models/:id      → Get model details
POST   /api/v1/models          → Create model
PUT    /api/v1/models/:id      → Replace model
PATCH  /api/v1/models/:id      → Partial update
DELETE /api/v1/models/:id      → Delete model
```

### REST Response Format

```json
// Success: 200
{
  "data": { "id": "abc123", "name": "gpt-4", "status": "ready" },
  "meta": { "request_id": "req_001" }
}

// List: 200
{
  "data": [ ... ],
  "pagination": {
    "cursor": "next_page_token",
    "has_more": true
  }
}

// Error: 4xx/5xx
{
  "error": {
    "code": "model_not_found",
    "message": "Model abc123 not found",
    "details": { "model_id": "abc123" }
  },
  "meta": { "request_id": "req_001" }
}
```

## GraphQL Design

```graphql
type Query {
  model(id: ID!): Model
  models(status: ModelStatus, limit: Int = 10): [Model!]!
  searchModels(query: String!): [Model!]!
}

type Mutation {
  createModel(input: ModelInput!): Model!
  trainModel(id: ID!, config: TrainingConfigInput!): TrainingJob!
  deleteModel(id: ID!): Boolean!
}

type Model {
  id: ID!
  name: String!
  status: ModelStatus!
  config: ModelConfig!
  metrics: ModelMetrics
  createdAt: DateTime!
}

enum ModelStatus { CREATING, TRAINING, READY, FAILED }

input ModelInput {
  name: String!
  architecture: String!
  hiddenSize: Int = 768
  numLayers: Int = 12
}
```

## Versioning

```python
# REST: URL versioning
/api/v1/models
/api/v2/models

# REST: Header versioning
Accept: application/vnd.myapp.v2+json

# GraphQL: Schema versioning
# Add fields with @deprecated directive
type Model @deprecated(reason: "Use ModelV2") {
    oldField: String @deprecated(reason: "Use newField")
}
```

## Pagination

```python
# REST cursor-based (recommended)
def list_models(cursor: str = None, limit: int = 50):
    query = db.query(Model)
    if cursor:
        query = query.filter(Model.id > decode_cursor(cursor))
    items = query.limit(limit + 1).all()
    has_more = len(items) > limit
    return items[:limit], encode_cursor(items[-1].id) if has_more else None

# GraphQL connection pattern
type ModelConnection {
    edges: [ModelEdge!]!
    pageInfo: PageInfo!
}
type ModelEdge {
    cursor: String!
    node: Model!
}
type PageInfo {
    hasNextPage: Boolean!
    endCursor: String
}
```

## Pitfalls

- REST: never return sensitive data in error messages
- GraphQL: N+1 queries need DataLoader or batching
- Rate limiting: use headers `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- Idempotency: POST /payments should have idempotency-key for safety
- Versioning: breaking changes need new version or graceful deprecation
