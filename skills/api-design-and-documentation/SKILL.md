---
name: api-design-and-documentation
description: "Use for REST API design. Resources, schemas, OpenAPI, auth."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [programming, api, rest, design, documentation, openapi]
    related_skills: [database-schema-design, code-review-checklist]
---

# API Design & Documentation

## Overview

A comprehensive methodology for designing RESTful APIs that are consistent, discoverable, and maintainable. Covers resource modeling, endpoint naming conventions, status codes, request/response schema design, pagination, error handling, authentication/authorization strategies, and OpenAPI/Swagger spec generation with schema validation patterns.

## When to Use

- Designing a new REST API from scratch
- Reviewing or standardizing an existing API design
- Generating OpenAPI 3.x specs for documentation or client generation
- Planning versioning, deprecation, or migration strategies
- Onboarding teams to API-first development workflows

## Workflow

### Phase 1: Resource Modeling

Identify domain entities and their relationships.

```bash
# Discover domain entities from an existing codebase
grep -rh --include='*.py' -E '^class [A-Z]\w+(Model|Schema|Entity|DTO)\b' . | head -30
grep -rh --include='*.ts' --include='*.js' -E '^(export )?interface [A-Z]\w+' . | head -30
grep -rh --include='*.{ts,js}' -E '^(export )?type [A-Z]\w+ =' . | head -30
```

**Resource naming principles:**
- Use **plural nouns** for collections: `/users`, `/orders`, `/products`
- Use **singular nouns** for singletons or single-instance: `/profile`, `/config`
- Use **nesting** for sub-resources only when the child is inseparable from the parent: `/users/{id}/addresses`
- Avoid nest > 2 levels — introduce sub-resource identifiers instead

**Resource relationships table:**

| Endpoint | Collection/Item | Example |
|----------|----------------|---------|
| `GET /users` | Collection | List users |
| `GET /users/{id}` | Item | Get one user |
| `POST /users` | Collection | Create user |
| `PUT /users/{id}` | Item | Replace user |
| `PATCH /users/{id}` | Item | Partial update |
| `DELETE /users/{id}` | Item | Remove user |

### Phase 2: Endpoint Design with Standard HTTP Verbs

Use HTTP verbs semantically:

```python
# Example: Flask resource routing
# GET    /users          → list_users()
# POST   /users          → create_user()
# GET    /users/{id}     → get_user(id)
# PUT    /users/{id}     → update_user(id)     # full replacement
# PATCH  /users/{id}     → patch_user(id)      # partial update
# DELETE /users/{id}     → delete_user(id)

# Action endpoints (for non-CRUD operations):
# POST   /users/{id}/activate      → activate_user(id)
# POST   /orders/{id}/cancel       → cancel_order(id)
# POST   /payments/{id}/refund     → refund_payment(id)
```

**Naming conventions:**
- Use kebab-case for resource names: `/order-items`, not `/orderItems` or `/order_items`
- Use snake_case for query parameters: `?page_number=1&page_size=20`
- Use camelCase in JSON response bodies (JavaScript convention)
- Use lowercase for all URL segments
- Use hyphens (not underscores) in URLs

### Phase 3: Status Code Strategy

```python
STATUS_CODES = {
    # Success
    200: "GET - Success, DELETE - Success",
    201: "POST - Resource created",
    202: "Accepted for async processing",
    204: "Success, no body (DELETE, PUT)",

    # Client Errors
    400: "Bad request - malformed syntax or invalid params",
    401: "Unauthenticated - missing/invalid credentials",
    403: "Forbidden - authenticated but not authorized",
    404: "Not found - resource doesn't exist",
    405: "Method not allowed",
    409: "Conflict - resource state conflict (e.g. duplicate)",
    422: "Unprocessable entity - validation errors",
    429: "Too many requests - rate limited",

    # Server Errors
    500: "Internal server error",
    502: "Bad gateway",
    503: "Service unavailable",
    504: "Gateway timeout",
}
```

### Phase 4: Request/Response Schema Design

**Pagination:**

```json
// Request
GET /users?page=2&per_page=20
GET /users?cursor=eyJpZCI6MX0&limit=20

// Response (offset-based)
{
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total_items": 142,
    "total_pages": 8,
    "links": {
      "first": "/users?page=1&per_page=20",
      "prev": "/users?page=1&per_page=20",
      "next": "/users?page=3&per_page=20",
      "last": "/users?page=8&per_page=20"
    }
  }
}

// Response (cursor-based - preferred for real-time data)
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6NTB9",
    "has_more": true
  }
}
```

**Error response envelope:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request was invalid",
    "details": [
      {
        "field": "email",
        "message": "must be a valid email address",
        "code": "INVALID_FORMAT"
      }
    ],
    "request_id": "req_abc123",
    "docs_url": "https://api.example.com/docs/errors#VALIDATION_ERROR"
  }
}
```

**Standard response envelope (recommended for consistency):**

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2025-07-28T12:00:00Z"
  }
}
```

### Phase 5: Authentication & Authorization

```yaml
# Strategy selection

API Keys:
  - Best for: Machine-to-machine, simple auth
  - Transport: Header (X-API-Key) or query param
  - Risk: Low entropy, easy to leak
  - Pattern: 
    request.headers['X-API-Key'] == stored_key

JWT (Bearer Token):
  - Best for: User-facing APIs, stateless auth
  - Transport: Authorization: Bearer <token>
  - Claims: sub, role, exp, iat, jti
  - Signature: RS256 (asymmetric) preferred over HS256
  - Pattern:
    token = request.headers['Authorization'].split('Bearer ')[1]
    payload = jwt.decode(token, public_key, algorithms=['RS256'])

OAuth2:
  - Best for: Third-party app authorization
  - Flows:
    - Authorization Code (+ PKCE) → Web apps, mobile
    - Client Credentials → Server-to-server
    - Device Code → CLI tools, IoT
  - Scopes: granular permission model

API Key + JWT hybrid:
  - API key identifies the client application
  - JWT identifies the user and carries permissions
  - Both validated on every request
```

### Phase 6: OpenAPI / Swagger Spec Generation

Generate a spec from code annotations or from a skeleton:

```yaml
openapi: 3.0.3
info:
  title: Users API
  description: User management API
  version: 1.0.0
  contact:
    name: API Team
    url: https://api.example.com/support
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      operationId: listUsers
      summary: List all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Paginated list of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
    post:
      operationId: createUser
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '422':
          description: Validation error
          $ref: '#/components/responses/ValidationError'

components:
  schemas:
    User:
      type: object
      required: [id, email, name]
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        created_at:
          type: string
          format: date-time
          readOnly: true
    CreateUserRequest:
      type: object
      required: [email, name]
      properties:
        email:
          type: string
          format: email
        name:
          type: string
        password:
          type: string
          minLength: 8
          writeOnly: true
    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'
    Pagination:
      type: object
      properties:
        page:
          type: integer
        per_page:
          type: integer
        total_items:
          type: integer
        total_pages:
          type: integer
  responses:
    ValidationError:
      description: Validation error
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                $ref: '#/components/schemas/ErrorDetail'
    ErrorDetail:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
```

### Phase 7: API Versioning & Deprecation

```python
VERSIONING_STRATEGIES = {
    "url_path": "https://api.example.com/v1/users",      # Most common
    "header":    "Accept: application/vnd.example.v1+json",   # More flexible
    "query":     "https://api.example.com/users?version=1",   # Cache-busting issues
}

# Deprecation headers (return on every response to deprecated endpoints)
{
    "Sunset": "Sat, 31 Dec 2025 23:59:59 GMT",
    "Deprecation": "true",
    "Link": "<https://api.example.com/docs/v2-migration>; rel=\"deprecation\""
}
```

**Recommendation:** Use URL path versioning (`/v1/`, `/v2/`) for public APIs. Use header/content-type versioning for internal/microservice APIs.

### Phase 8: Validation & Schema Design Patterns

```python
# Pattern 1: Input validation with Pydantic (Python)
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from uuid import UUID, uuid4

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)
    role: str = Field(default="user", pattern=r"^(admin|user|viewer)$")

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError('password must contain a digit')
        if not any(c.isupper() for c in v):
            raise ValueError('password must contain uppercase')
        return v

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}

# Pattern 2: TypeScript interface for frontend consumption
"""
interface CreateUserRequest {
  email: string;    // format: email
  name: string;     // 1-100 chars
  password: string; // min 8 chars
  role?: 'admin' | 'user' | 'viewer';
}

interface User {
  id: string;       // uuid
  email: string;
  name: string;
  role: string;
  created_at: string; // date-time
}
"""
```

## Common Pitfalls

- **Over-nesting resources**: Beyond 2 levels, use query params or sub-resource IDs. `/orgs/{id}/projects/{pid}/tasks/{tid}` is too deep — use `/tasks?project_id=xxx`.
- **Inconsistent error responses**: Always return the same error envelope structure. Never mix string errors with structured errors.
- **Exposing internal IDs**: Use UUIDs for public identifiers, not auto-increment integers. This prevents enumeration attacks.
- **Skipping rate limits**: Every public endpoint needs rate limiting headers (`X-RateLimit-Remaining`, `X-RateLimit-Reset`).
- **No pagination on list endpoints**: All list endpoints must paginate. Default to sane limits (20-50 per page). Never return unbounded collections.
- **PUT vs PATCH confusion**: PUT replaces the entire resource. PATCH applies partial changes. Use PATCH for single-field updates.
- **Ignoring idempotency**: PUT, DELETE should be idempotent. POST is not. For payment APIs, use Idempotency-Key headers.
- **API without documentation**: If it's not documented, it doesn't exist. Generate OpenAPI specs from code or maintain them as source of truth.
- **Breaking changes without deprecation**: Never remove or change existing fields without a deprecation period and sunset header.
- **Leaking stack traces**: Never return raw exceptions or stack traces in production API responses. Use generic error codes and log full details server-side.

## Verification Checklist

- [ ] All endpoints use standard HTTP verbs semantically (GET/POST/PUT/PATCH/DELETE)
- [ ] Resource names are plural nouns, kebab-case in URLs
- [ ] Consistent error response envelope across all endpoints
- [ ] All mutation endpoints validate input with schema validation
- [ ] Pagination implemented on all list endpoints (with sensible defaults)
- [ ] Authentication properly implemented (JWT / API Key / OAuth2)
- [ ] Authorization enforced per resource/per action
- [ ] Rate limiting configured and headers returned
- [ ] OpenAPI 3.x spec covers all endpoints with request/response schemas
- [ ] Spec renders without errors in Swagger UI / Redoc
- [ ] CORS configured for allowed origins
- [ ] Versioning strategy chosen and implemented
- [ ] Deprecation headers (Sunset, Deprecation, Link) on deprecated endpoints
- [ ] No secrets, stack traces, or internal IDs in responses
- [ ] Idempotency considered for critical POST endpoints
