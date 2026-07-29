---
name: oauth-authentication-patterns
description: "Use when implementing OAuth 2.0 and OpenID Connect auth."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [oauth, openid-connect, authentication, authorization, JWT, SSO]
    related_skills: [web-security-patterns, cryptography-implementation-patterns, api-design-rest-graphql, identity-access-management]
---

# OAuth 2.0 and Authentication Patterns

Implementing OAuth 2.0, OpenID Connect, and modern authentication patterns — from authorization flows through token management, SSO, and security best practices.

## When to Use

- Adding authentication to a web or mobile app
- Implementing SSO (Single Sign-On) for multiple apps
- Building an API that needs authorization
- Integrating with identity providers (Google, GitHub, Azure AD)
- Managing tokens, refresh flows, and sessions

## OAuth 2.0 Flows

```python
OAUTH_FLOWS = {
    'authorization_code': {
        'use_case': 'Web apps with server-side backend',
        'security': 'Most secure — tokens never reach browser',
        'flow': 'Redirect → Auth code → Exchange for tokens → API access',
    },
    'pkce': {
        'use_case': 'Mobile apps, SPAs (single page apps)',
        'security': 'Secure — code verifier prevents interception',
        'flow': 'Generate code_verifier → Auth with code_challenge → Exchange',
    },
    'client_credentials': {
        'use_case': 'Server-to-server, API integrations',
        'security': 'No user context — machine to machine',
        'flow': 'Client ID + Secret → Token → API access',
    },
    'device_code': {
        'use_case': 'CLI tools, smart TVs, input-constrained devices',
        'flow': 'User enters code on another device → Poll for token',
    },
}
```

## JWT Token Handler

```python
import jwt, time
from typing import Dict, Optional

class JWTHandler:
    """Create and verify JWT access and refresh tokens."""
    
    def __init__(self, secret: str, issuer: str = 'myapp'):
        self.secret = secret
        self.issuer = issuer
    
    def create_access_token(self, user_id: str, roles: List[str] = None,
                            ttl: int = 900) -> str:  # 15 min default
        return jwt.encode({
            'sub': user_id, 'iss': self.issuer,
            'iat': int(time.time()),
            'exp': int(time.time()) + ttl,
            'type': 'access', 'roles': roles or [],
        }, self.secret, algorithm='HS256')
    
    def create_refresh_token(self, user_id: str, ttl: int = 2592000) -> str:  # 30 days
        return jwt.encode({
            'sub': user_id, 'iss': self.issuer,
            'iat': int(time.time()),
            'exp': int(time.time()) + ttl,
            'type': 'refresh', 'token_id': str(uuid.uuid4()),
        }, self.secret, algorithm='HS256')
```

## Common Pitfalls

1. **Tokens in URLs** — access tokens in query strings are logged and exposed
2. **No CSRF for auth code flow** — state parameter prevents CSRF; always use it
3. **Storing tokens insecurely** — localStorage is XSS-accessible; use httpOnly cookies
4. **Ignoring token expiration** — expired tokens should trigger refresh flow
5. **Overly permissive scopes** — request minimum scopes; never use `*:*`

## Verification Checklist

- [ ] OAuth flow matches app type (web, mobile, SPA)
- [ ] PKCE used for public clients (mobile, SPA)
- [ ] State parameter prevents CSRF on auth code flow
- [ ] Access tokens short-lived (15 min), refresh tokens with rotation
- [ ] HTTPS enforced for all auth endpoints
- [ ] Token storage is secure (httpOnly cookies or secure storage)
- [ ] CORS properly configured for auth endpoints
