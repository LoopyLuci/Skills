---
name: fullstack-dev-api-design
description: Use when designing REST API endpoints, choosing HTTP methods, implementing pagination, or writing OpenAPI specs.
tags: [api, rest, graphql, grpc, openapi, backend, design]
related_skills: [fullstack-dev-db-schema, android-native-dev]
---

# API Design Guidelines

Framework-agnostic API design guide covering REST, GraphQL, and gRPC with 50+ rules across 10 categories.

## Quick Start Checklist

- [ ] Resource named as plural noun (`/orders` not `/getOrders`)
- [ ] URL in kebab-case, body fields in camelCase
- [ ] Correct HTTP method (GET=read, POST=create, PUT=replace, PATCH=partial, DELETE=remove)
- [ ] Correct status code (201 Created, 422 Validation, 404 Not Found)
- [ ] Error response follows RFC 9457 envelope
- [ ] Pagination on all list endpoints (default 20, max 100)
- [ ] Authentication via Bearer token in header
- [ ] Request ID in response header (`X-Request-Id`)
- [ ] Rate limit headers included
- [ ] Endpoint documented in OpenAPI spec

## Code Example: Error Response (RFC 9457)

```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 422,
  "detail": "Account balance $10.00 is less than withdrawal $50.00.",
  "request_id": "req_7f3a8b2c",
  "errors": [
    { "field": "amount", "message": "Exceeds balance", "code": "INSUFFICIENT_BALANCE" }
  ]
}
```

## Code Example: Cursor Pagination

```json
{
  "data": [...],
  "pagination": { "next_cursor": "abc123", "has_more": true }
}
```

## Common Pitfalls

- **Verbs in URLs**: Use HTTP methods, not `/getUser` or `/createOrder`
- **200 for errors**: Always use correct 4xx/5xx status codes
- **Deep nesting**: Max 2 levels nesting, then flatten with query params
- **Stack traces in production**: Log internally, return safe error messages
- **No pagination**: Always paginate list endpoints

## Verification Checklist

- [ ] Resources use plural nouns
- [ ] HTTP methods match semantics
- [ ] Status codes correct for each scenario
- [ ] Error format consistent (RFC 9457)
- [ ] Pagination implemented on list endpoints
- [ ] OpenAPI spec documented
