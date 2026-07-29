---
name: expressjs-api-patterns
description: "Use when building APIs with Express.js."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [express, node, API, middleware, routing, error-handling]
    related_skills: [api-design-rest-graphql, api-testing-patterns, swagger-openapi-patterns]
---

# Express.js API Patterns

Building APIs with Express.js — from middleware patterns and routing through error handling, validation, and production best practices.

## When to Use

- Building REST APIs with Express.js
- Implementing middleware chains
- Error handling and validation
- Authentication and authorization middleware

## Express Patterns

```javascript
const express = require('express');
const app = express();

// Async error wrapper
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

// Route with validation
app.post('/api/users', validate(schema), asyncHandler(async (req, res) => {
  const user = await createUser(req.body);
  res.status(201).json(user);
}));

// Global error handler
app.use((err, req, res, next) => {
  const status = err.status || 500;
  res.status(status).json({
    error: { message: err.message, code: err.code }
  });
});
```

## Verification Checklist

- [ ] Middleware order (security → parsing → auth → routes → error)
- [ ] Async error handling wrapper
- [ ] Input validation middleware
- [ ] Structured error responses
- [ ] CORS and security headers (helmet)
- [ ] Rate limiting middleware
