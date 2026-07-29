---
name: api-penetration-testing
description: "Use when testing API security and endpoints."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [API-pentest, REST, GraphQL, JWT, OAuth, rate-limiting, injection]
    related_skills: [webapp-penetration-testing, sql-injection-exploitation, web-security-patterns, oauth-authentication-patterns]
---

# API Penetration Testing

Testing API security — from REST and GraphQL endpoint testing through authentication bypass, injection, rate limiting, and business logic flaws.

## When to Use

- Testing REST API security
- Testing GraphQL API security
- Finding API authentication and authorization flaws
- Testing API rate limiting and abuse cases
- API-specific vulnerabilities (mass assignment, IDOR)

## API Testing Techniques

```python
API_TESTS = {
    'auth_bypass': 'Test missing/weak JWT, OAuth misconfig, API key in URL, default tokens',
    'injection': 'Test SQL/NoSQL injection in params, headers, request bodies',
    'idor': 'Test object ID manipulation (user/123 → user/124)',
    'mass_assignment': 'Test extra fields in request body (is_admin=true)',
    'rate_limiting': 'Test without auth headers, IP-based limiting bypass (X-Forwarded-For)',
    'graphql_introspection': 'Test if introspection is enabled (query __schema)',
    'graphql_batching': 'Test batch queries for rate limit bypass',
}

# REST API testing with curl
API_TESTS_CURL = {
    'jwt_none_algorithm': "curl -H 'Authorization: Bearer eyJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ.' https://api.example.com/admin",
    'idor_test': "curl https://api.example.com/users/123",
    'mass_assignment': "curl -X PUT https://api.example.com/users/me -d '{\"role\":\"admin\"}'",
}

# GraphQL query depth testing
GRAPHQL_DEPTH = """
query DeepQuery {
  user(id: 1) {
    posts { comments { author { posts { comments { author { name } } } } } }
  }
}
"""
```

## Verification Checklist

- [ ] Authentication tested (JWT none algo, token in URL, missing auth)
- [ ] Authorization tested (IDOR, horizontal/vertical privilege esc)
- [ ] Injection tested (SQL, NoSQL, command injection in params)
- [ ] Rate limiting tested (brute force, resource exhaustion)
- [ ] Mass assignment tested (extra fields in request)
- [ ] GraphQL: introspection, query depth, batching attacks
- [ ] Input validation tested (XSS, SSRF, XXE)
- [ ] API versioning and deprecation tested
- [ ] CORS configuration reviewed
