---
name: api-and-interface-design
description: Use when designing APIs, module boundaries, or any public interface; creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills]
    source: addyosmani/agent-skills
    adapted: true
---

# API and Interface Design

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Designing APIs, module boundaries, or any public interface
- Creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend

## When NOT to Use

- Endpoints that return different shapes depending on conditions
- Inconsistent error formats across endpoints
- Validation scattered throughout internal code instead of at boundaries
- Breaking changes to existing fields (type changes, removals)
- List endpoints without pagination
- Verbs in REST URLs (`/api/createTask`, `/api/getUsers`)
- Third-party API responses used without validation or sanitization
- A `SELECT` for an idempotency key followed by an `INSERT` — that's a race, not a guard
- An idempotency key derived from a UUID, timestamp, or anything else regenerated per attempt
- The same key accepted with a different request body, silently returning the first response
- A key retention window shorter than the longest path that can re-deliver the request

Interfaces — REST endpoints, GraphQL schemas, module boundaries, component props, database-backed contracts — succeed when the right call is easy and the wrong call is hard. This skill covers designing those surfaces up front, keeping error behaviour consistent, validating only where outside data enters, extending without breaking consumers, and honouring idempotency keys when retries are possible.

## Design Principles

### Treat observable behaviour as a contract

Once an API has enough consumers, every observable detail — undocumented quirks, error message wording, response ordering, timing — ends up depended on by somebody. Implications:

- Expose deliberately; every visible behaviour is a potential commitment.
- Keep implementation details internal, because anything a caller can see, someone will rely on.
- Plan retirement before launch; removing something people depend on needs its own process.
- Contract tests do not make changes safe: they cannot cover behaviour nobody documented.

### Stay at one version

Avoid forcing consumers to choose between versions of the same dependency or API; divergent version needs create diamond dependency problems. Design as though only one version exists at a time — extend rather than fork.

### Define the contract first

Specify the surface, then build against it; the contract is the specification and the implementation follows.

```typescript
// Define the contract first
interface TaskAPI {
  // Creates a task and returns the created task with server-generated fields
  createTask(input: CreateTaskInput): Promise<Task>;

  // Returns paginated tasks matching filters
  listTasks(params: ListTasksParams): Promise<PaginatedResult<Task>>;

  // Returns a single task or throws NotFoundError
  getTask(id: string): Promise<Task>;

  // Partial update — only provided fields change
  updateTask(id: string, input: UpdateTaskInput): Promise<Task>;

  // Idempotent delete — succeeds even if already deleted
  deleteTask(id: string): Promise<void>;
}
```

### Use one error strategy everywhere

Every error response should share one shape, and status codes should carry meanings the client can act on:

```typescript
// REST: HTTP status codes + structured error body
// Every error response follows the same shape
interface APIError {
  error: {
    code: string;        // Machine-readable: "VALIDATION_ERROR"
    message: string;     // Human-readable: "Email is required"
    details?: unknown;   // Additional context when helpful
  };
}

// Status code mapping
// 400 → Client sent invalid data
// 401 → Not authenticated
// 403 → Authenticated but not authorized
// 404 → Resource not found
// 409 → Conflict (duplicate, version mismatch)
// 422 → Validation failed (semantically invalid)
// 500 → Server error (never expose internal details)
```

Mixing patterns — some endpoints throwing, others returning null, others returning `{ error }` — leaves consumers unable to predict behaviour.

### Validate at boundaries only

Trust internal code once input has been checked at its edge:

```typescript
// Validate at the API boundary
app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid task data',
        details: result.error.flatten(),
      },
    });
  }

  // After validation, internal code trusts the types
  const task = await taskService.create(result.data);
  return res.status(201).json(task);
});
```

Validation belongs at route handlers taking user input, form submission handlers, environment variable loading, and — always — parsing third-party service responses, which must be treated as untrusted. It does not belong between internal functions sharing type contracts, inside utilities called by already-validated code, or on data fresh from your own database.

### Grow additively

New fields should be optional additions; never retype or remove existing ones.

```typescript
// Good: Add optional fields
interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';  // Added later, optional
  labels?: string[];                       // Added later, optional
}

// Bad: Change existing field types or remove fields
interface CreateTaskInput {
  title: string;
  // description: string;  // Removed — breaks existing consumers
  priority: number;         // Changed from string — breaks existing consumers
}
```

### Name predictably

| Pattern | Convention | Example |
|---------|-----------|---------|
| REST endpoints | Plural nouns, no verbs | `GET /api/tasks`, `POST /api/tasks` |
| Query params | camelCase | `?sortBy=createdAt&pageSize=20` |
| Response fields | camelCase | `{ createdAt, updatedAt, taskId }` |
| Boolean fields | is/has/can prefix | `isComplete`, `hasAttachments` |
| Enum values | UPPER_SNAKE | `"IN_PROGRESS"`, `"COMPLETED"` |

### Honour the idempotency key properly

Accepting `Idempotency-Key` is the contract; storing the key against the result is the implementation. Careless handling is worse than refusing the header, because the client now believes retrying is safe when it is not.

Derive the key from the intent, so it is stable across retries of one action and different for distinct actions:

```typescript
crypto.randomUUID()                    // ✗ new key per attempt — every retry is a new charge
`${userId}:${amount}`                  // ✗ two legitimate $50 charges collapse into one
`${orderId}:${Date.now()}`             // ✗ a timestamp is randomUUID() wearing a hat

req.headers['idempotency-key']         // ✓ client generates once, reuses on retry
`charge:v1:${orderId}`                 // ✓ derived from an immutable identifier
```

Claim the key atomically — a check followed by an insert is a race, so let the unique constraint pick the winner:

```typescript
// ✗ TOCTOU: two concurrent retries both read "not seen", both charge
if (!(await db.exists(key))) {
  await chargeCard(amount);
  await db.insert(key);
}

// ✓ let the unique constraint pick the winner
try {
  await db.insert({ key, state: 'in_progress', requestHash });
} catch (e) {
  if (isUniqueViolation(e)) return replayOrReject(key);
  throw e;
}
const result = await chargeCard(amount);
await db.update({ key, state: 'succeeded', response: result });
```

Guard the payload: the same key with a different body is a client bug and must fail loudly instead of replaying the first response.

```typescript
if (existing.requestHash !== hash(req.body)) {
  return res.status(422).json({
    error: { code: 'IDEMPOTENCY_KEY_REUSED', message: 'Idempotency key reused with a different payload' },
  });
}
```

Choose deliberately what an in-flight duplicate receives:

| Strategy | Response | Use when |
|---|---|---|
| Reject | `409 Conflict` | Client can retry later; simplest and safest |
| Wait | Block for the result, bounded | Caller needs it synchronously |
| Return pending | `202` + status URL | Long-running effects |

Never let a second caller through because the first "seems stuck": an attempt whose fate is unknown is exactly when duplication costs most. Remember there are three outcomes — success, failure, and unknown — so record the intent before calling out, leaving evidence that a crash between call and response must be resolved. Size key retention from the longest retry chain, not disk cost: keys must outlive dead-letter replay and provider dispute windows.

## REST Conventions

### Resources

```
GET    /api/tasks              → List tasks (with query params for filtering)
POST   /api/tasks              → Create a task
GET    /api/tasks/:id          → Get a single task
PATCH  /api/tasks/:id          → Update a task (partial)
DELETE /api/tasks/:id          → Delete a task

GET    /api/tasks/:id/comments → List comments for a task (sub-resource)
POST   /api/tasks/:id/comments → Add a comment to a task
```

### Pagination

Every list endpoint should paginate:

```typescript
// Request
GET /api/tasks?page=1&pageSize=20&sortBy=createdAt&sortOrder=desc

// Response
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 142,
    "totalPages": 8
  }
}
```

### Filtering and partial updates

Filters travel as query parameters (`GET /api/tasks?status=in_progress&assignee=user123&createdAfter=2025-01-01`). PATCH takes partial objects and changes only what is supplied:

```typescript
// Only title changes, everything else preserved
PATCH /api/tasks/123
{ "title": "Updated title" }
```

## TypeScript Patterns

Model variants as discriminated unions so consumers narrow by type:

```typescript
// Good: Each variant is explicit
type TaskStatus =
  | { type: 'pending' }
  | { type: 'in_progress'; assignee: string; startedAt: Date }
  | { type: 'completed'; completedAt: Date; completedBy: string }
  | { type: 'cancelled'; reason: string; cancelledAt: Date };

// Consumer gets type narrowing
function getStatusLabel(status: TaskStatus): string {
  switch (status.type) {
    case 'pending': return 'Pending';
    case 'in_progress': return `In progress (${status.assignee})`;
    case 'completed': return `Done on ${status.completedAt}`;
    case 'cancelled': return `Cancelled: ${status.reason}`;
  }
}
```

Keep input and output types separate so server-generated fields never leak into requests:

```typescript
// Input: what the caller provides
interface CreateTaskInput {
  title: string;
  description?: string;
}

// Output: what the system returns (includes server-generated fields)
interface Task {
  id: string;
  title: string;
  description: string | null;
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}
```

Brand identifiers so a `UserId` cannot silently stand in for a `TaskId`:

```typescript
type TaskId = string & { readonly __brand: 'TaskId' };
type UserId = string & { readonly __brand: 'UserId' };

// Prevents accidentally passing a UserId where a TaskId is expected
function getTask(id: TaskId): Promise<Task> { ... }
```

## Objections and Answers

| Objection | Response |
|---|---|
| "We'll document it later" | Types are the documentation; define them first. |
| "We don't need pagination yet" | You will once someone reaches 100+ items; add it from the start. |
| "PATCH is complicated, let's use PUT" | PUT demands the full object every time; clients want partial updates. |
| "We'll version when we need to" | Breaking changes without versioning break consumers; design for extension. |
| "Nobody uses that undocumented behaviour" | If it is observable, somebody depends on it. |
| "We can maintain two versions" | Multiple versions multiply maintenance and create diamond dependencies. |
| "Internal APIs don't need contracts" | Internal consumers are still consumers; contracts decouple and allow parallel work. |
| "Accepting the header is enough" | Accepting without honouring tells clients retrying is safe when it is not. |
| "Our queue is exactly-once" | Broker acknowledgement and side effect are separate transactions; assume at-least-once and process idempotently. |
| "Duplicate requests are rare" | They correlate: retries spike exactly when a dependency degrades. |

## Verification

- [ ] Each endpoint has typed input and output schemas.
- [ ] All error responses share one format and one status-code vocabulary.
- [ ] Validation happens only at system boundaries, not inside trusted internals.
- [ ] List endpoints paginate; filters use query parameters.
- [ ] New fields are additive and optional; no existing field retyped or removed.
- [ ] Naming follows the same convention across every endpoint.
- [ ] Contracts/types are committed alongside the implementation.
- [ ] State-changing endpoints either honour an idempotency key or are documented as unsafe to retry.
- [ ] The key is claimed in one atomic operation guarded by a unique constraint.
- [ ] A key reused with a different payload fails loudly instead of replaying the wrong response.
- [ ] The in-flight duplicate response is a deliberate choice (`409`, wait, or `202`), not whatever falls out.
- [ ] Key retention outlives the longest retry path, including dead-letter replay.

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...
- [context-engineering](../context-engineering/SKILL.md) — Use when starting a new session, when agent output quality degrades, when switching betwee...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/api-and-interface-design/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
