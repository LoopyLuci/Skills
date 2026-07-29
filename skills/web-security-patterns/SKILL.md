---
name: web-security-patterns
description: "Use when implementing web application security patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-security, OWASP, XSS, CSRF, SQL-injection, secure-coding]
    related_skills: [cryptography-implementation-patterns, api-design-rest-graphql, api-gateway-load-balancing, frontend-bootstrap]
---

# Web Security Patterns

Implementing secure web applications against the OWASP Top 10 — from input validation through authentication, CSRF protection, CSP headers, and secure session management.

## When to Use

- Building a new web application (any framework)
- Auditing an existing app for security vulnerabilities
- Implementing authentication and authorization
- Protecting against XSS, CSRF, SQLi, and other injection attacks
- Setting up Content Security Policy and other security headers

## Defense Layers

```
Input → Validation → Sanitization → Business Logic → Output → Encoding → Client
                                            ↓
                                      CSRF Token
                                        Check
```

## Injection Prevention

### SQL Injection Prevention

```python
# BAD — string interpolation
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# GOOD — parameterized queries
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

# GOOD — ORM (usually safe)
User.objects.filter(email=email)

# For dynamic identifiers (table names, column names — can't parameterize)
# Validate against an allowlist
ALLOWED_TABLES = {'users', 'orders', 'products'}
if table_name not in ALLOWED_TABLES:
    raise ValueError(f"Invalid table: {table_name}")
cursor.execute(f"SELECT * FROM {table_name}")  # Now safe
```

### XSS Prevention

```python
# NEVER do this:
template = f"<div>{user_input}</div>"  # XSS if user_input has <script>

# ALWAYS encode output:
import html
safe_html = f"<div>{html.escape(user_input)}</div>"

# Template engines with auto-escaping (Jinja2, React JSX)
# Jinja2: {{ user_input }} is auto-escaped (unless |safe filter used)
# React: {userInput} is auto-escaped (unless dangerouslySetInnerHTML used)

# Context-specific encoding:
def encode_for_context(value, context='html'):
    """Encode based on output context."""
    if context == 'html':
        return html.escape(value, quote=True)
    elif context == 'attribute':
        # Encode for HTML attribute context
        return value.replace('"', '&quot;').replace("'", '&#x27;')
    elif context == 'javascript':
        # Encode for JS string context
        return json.dumps(value)[1:-1]  # Simple approach
    elif context == 'url':
        from urllib.parse import quote
        return quote(value, safe='')
    return value
```

### CSP (Content Security Policy) Headers

```python
# Content Security Policy — prevents XSS even if injection occurs
CSP_HEADER = (
    "default-src 'self';"
    "script-src 'self' https://cdn.example.com;"
    "style-src 'self' 'unsafe-inline';"
    "img-src 'self' data: https:;"
    "font-src 'self';"
    "connect-src 'self' https://api.example.com;"
    "frame-ancestors 'none';"
    "base-uri 'self';"
    "form-action 'self';"
)

# Nonce-based CSP (for inline scripts)
import secrets
nonce = secrets.token_urlsafe(16)
CSP_WITH_NONCE = f"script-src 'nonce-{nonce}';"
# Then in HTML: <script nonce="{nonce}">alert('safe')</script>
```

## Authentication Patterns

### Secure Session Management

```python
import secrets
import hmac
import hashlib
from datetime import datetime, timedelta

class SessionManager:
    """Secure session tokens with rotation and binding."""
    
    def __init__(self, secret_key: bytes):
        self.secret = secret_key
        self.sessions = {}  # In production: Redis
    
    def create_session(self, user_id: int, metadata: dict = None) -> str:
        """Create a session with binding metadata."""
        session_id = secrets.token_urlsafe(32)
        
        # Sign the session ID to prevent tampering
        signature = hmac.new(
            self.secret,
            session_id.encode(),
            hashlib.sha256
        ).hexdigest()
        
        token = f"{session_id}.{signature}"
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'metadata': metadata or {},
            'ip_address': metadata.get('ip') if metadata else None,
        }
        
        return token
    
    def validate_session(self, token: str, request_ip: str = None) -> dict:
        """Validate session and check binding."""
        if '.' not in token:
            return None
        
        session_id, signature = token.split('.', 1)
        
        # Verify signature
        expected = hmac.new(
            self.secret, session_id.encode(), hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected):
            return None
        
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        # Optional: IP binding
        if request_ip and session.get('ip_address'):
            if request_ip != session['ip_address']:
                return None  # Possible session hijacking
        
        return session
```

### JWT Best Practices

```python
import jwt
from datetime import datetime, timedelta

class JWTManager:
    """JWT with security best practices."""
    
    def __init__(self, secret: str, issuer: str = 'myapp'):
        self.secret = secret
        self.issuer = issuer
    
    def create_token(self, user_id: str, role: str, ttl_minutes: int = 15):
        """Short-lived access token."""
        now = datetime.utcnow()
        payload = {
            'sub': user_id,
            'iss': self.issuer,
            'iat': now,
            'exp': now + timedelta(minutes=ttl_minutes),
            'role': role,
            'jti': secrets.token_hex(8),  # Unique token ID
            'type': 'access'
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    def create_refresh_token(self, user_id: str, ttl_days: int = 7):
        """Long-lived refresh token (stored server-side)."""
        now = datetime.utcnow()
        payload = {
            'sub': user_id,
            'iss': self.issuer,
            'iat': now,
            'exp': now + timedelta(days=ttl_days),
            'jti': secrets.token_hex(16),
            'type': 'refresh'
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    def verify_token(self, token: str) -> dict:
        """Verify and decode. Raises on expiration/invalid."""
        try:
            payload = jwt.decode(
                token, self.secret,
                algorithms=['HS256'],
                issuer=self.issuer,
                options={'require': ['exp', 'iat', 'jti', 'type']}
            )
            return payload
        except jwt.ExpiredSignatureError:
            return {'error': 'token_expired'}
        except jwt.InvalidTokenError:
            return {'error': 'invalid_token'}
```

## CSRF Protection

```python
class CSRFProtection:
    """Double-submit cookie pattern for CSRF."""
    
    def generate_token(self) -> str:
        """Generate CSRF token."""
        return secrets.token_urlsafe(32)
    
    def validate_request(self, request, csrf_cookie_name='csrf_token'):
        """Validate CSRF: token must be in both header and cookie."""
        token_in_cookie = request.cookies.get(csrf_cookie_name)
        token_in_header = request.headers.get('X-CSRF-Token')
        
        if not token_in_cookie or not token_in_header:
            return False
        
        return secrets.compare_digest(token_in_cookie, token_in_header)


# SameSite cookie attribute (modern CSRF protection)
# Set-Cookie: session=abc; SameSite=Lax; Secure; HttpOnly
# SameSite=Lax: sent for top-level navigations (safe)
# SameSite=Strict: never sent for cross-site requests (most secure)
# SameSite=None: must also set Secure; allows cross-site (for OAuth etc.)
```

## Security Headers

```python
SECURITY_HEADERS = {
    'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
    'X-Content-Type-Options': 'nosniff',          # Prevents MIME sniffing
    'X-Frame-Options': 'DENY',                    # Prevents clickjacking
    'X-XSS-Protection': '0',                      # Disables legacy XSS filter
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
    'Content-Security-Policy': "default-src 'self'",
}

def apply_security_headers(response):
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response
```

## Common Pitfalls

1. **Client-side validation only** — server must validate everything; client validation is UX only
2. **Missing HTTPS** — anything without TLS travels in plaintext; use HSTS
3. **Verbose error messages** — "User not found" vs "Wrong password" leaks user identities
4. **IDOR (Insecure Direct Object Reference)** — always check authorization, not just authentication
5. **Rate limiting missing** — login endpoints without rate limiting get brute-forced
6. **Dependency vulnerabilities** — libraries with known CVEs are the #1 attack vector; keep them updated

## Verification Checklist

- [ ] All inputs validated + sanitized (no raw interpolation into SQL/HTML/JS)
- [ ] HTTPS enforced with HSTS
- [ ] CSP header set with restrictive policy
- [ ] Authentication uses bcrypt/Argon2 for passwords, short-lived JWTs
- [ ] CSRF protection active on all state-changing endpoints
- [ ] Rate limiting on auth endpoints (login, password reset, API keys)
- [ ] No sensitive data in URLs or logs
- [ ] Session tokens are random, signed, and bound to metadata

## See Also

- cryptography-implementation-patterns — encryption and hashing
- api-design-rest-graphql — secure API design
- api-gateway-load-balancing — rate limiting at edge
- frontend-bootstrap — secure frontend patterns
