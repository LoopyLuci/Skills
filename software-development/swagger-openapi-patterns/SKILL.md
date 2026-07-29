---
name: swagger-openapi-patterns
description: "Use when designing APIs with OpenAPI/Swagger."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [OpenAPI, Swagger, API-design, REST, specification, codegen]
    related_skills: [api-design-and-documentation, api-testing-patterns, api-rate-limiting, graphql-api-implementation]
---

# OpenAPI/Swagger Patterns

Designing APIs with OpenAPI Specification — from spec-first design through code generation, validation, documentation, and SDK generation.

## When to Use

- Designing REST APIs with OpenAPI 3.x
- Spec-first API development (spec → code)
- Auto-generating API documentation
- Generating client SDKs from spec
- Validating API requests/responses against spec

## OpenAPI Patterns

```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0
  description: Manages user accounts and profiles

paths:
  /users/{userId}:
    get:
      summary: Get user by ID
      parameters:
        - name: userId
          in: path
          required: true
          schema: $ref: '#/components/schemas/UserId'
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema: $ref: '#/components/schemas/User'

components:
  schemas:
    UserId:
      type: string
      pattern: '^usr_[a-zA-Z0-9]{24}$'
      example: usr_abc123def456ghi789jkl0
    User:
      type: object
      required: [id, email, name]
      properties:
        id: $ref: '#/components/schemas/UserId'
        email: { type: string, format: email }
        name: { type: string, minLength: 1, maxLength: 100 }
        createdAt: { type: string, format: date-time }
```

## Verification Checklist

- [ ] Spec-first design (spec written before implementation)
- [ ] All endpoints documented with request/response schemas
- [ ] Reusable components defined ($ref, not inline)
- [ ] Validation: spec validates (openapi-generator validate)
- [ ] Request/response validation middleware in API server
- [ ] Client SDKs generated (openapi-generator)
- [ ] API documentation published (Swagger UI, Redoc)
- [ ] Breaking changes detected in CI (openapi-diff)
- [ ] Pagination, error responses, rate limiting documented
