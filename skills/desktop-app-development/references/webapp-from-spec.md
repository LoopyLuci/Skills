# Building Complete Webapps from Generated Specs

Pattern for building production-ready webapps from a WebBuilder-generated project spec. Covers Flask backend, enhanced frontend, security, testing, and deployment.

## Trigger

When the user asks to "build a complete webapp" or "build a webapp using only the program" — meaning generate a project spec and then implement it as a working webapp with backend, frontend, and tests.

## Workflow

1. **Generate project spec** — Use the WebBuilder program's project generation to create a JSON spec with sections, props, colors, and content
2. **Build Flask backend** — REST API with JWT auth, SQLAlchemy models, rate limiting, security headers
3. **Build enhanced frontend** — HTML/CSS/JS with SEO, accessibility, performance, and UX improvements
4. **Add tests** — pytest with Flask test client, covering auth, API, and security headers
5. **Verify end-to-end** — Run server, test all endpoints, confirm security headers present

## Flask Backend Pattern

```python
# app.py structure
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_limiter import Limiter
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

# Extensions initialized OUTSIDE create_app to avoid re-registration errors
db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)

# Models defined at module level
class User(UserMixin, db.Model):
    # ... fields ...
    def generate_token(self):
        payload = {'user_id': self.id, 'exp': datetime.utcnow() + timedelta(hours=24)}
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def create_app():
    app = Flask(__name__, static_folder='.', static_url_path='')
    db.init_app(app)
    # ... register routes ...
    with app.app_context():
        db.create_all()
    return app
```

### Key Security Headers

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
```

### JWT Auth Pattern

```python
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        token = token.replace('Bearer ', '')
        user = User.verify_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(user, *args, **kwargs)
    return decorated
```

### Rate Limiting

```python
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ...
```

## Frontend Enhancement Checklist

### SEO
- [ ] `<meta name="description">` with compelling summary
- [ ] `<meta name="keywords">` for relevant terms
- [ ] Open Graph tags (`og:title`, `og:description`, `og:image`, `og:url`)
- [ ] Twitter Card tags (`twitter:card`, `twitter:title`, `twitter:description`)
- [ ] JSON-LD structured data (`application/ld+json`)
- [ ] `<link rel="canonical">` tag
- [ ] `sitemap.xml` with all pages
- [ ] `robots.txt` with crawler directives

### Accessibility (WCAG 2.1 AA)
- [ ] Skip navigation link (`<a href="#main" class="skip-nav">`)
- [ ] ARIA labels on all interactive elements (`aria-label`, `aria-expanded`, `aria-controls`)
- [ ] Focus indicators (`*:focus-visible { outline: 2px solid ... }`)
- [ ] Reduced motion support (`@media (prefers-reduced-motion: reduce)`)
- [ ] Semantic HTML (`<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Color contrast 4.5:1 minimum for text

### Performance
- [ ] Preload critical assets (`<link rel="preload">`)
- [ ] Preconnect to external domains (`<link rel="preconnect">`)
- [ ] CSS containment for complex sections
- [ ] Lazy loading for below-fold images

### UX
- [ ] Scroll progress indicator
- [ ] Back-to-top button (appears after 500px scroll)
- [ ] Smooth scroll with sticky nav offset
- [ ] Mobile hamburger menu
- [ ] FAQ accordion with smooth animation
- [ ] Hover effects on cards and buttons

## Testing Pattern

```python
import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200

def test_register(client):
    response = client.post('/auth/register', json={
        'email': 'test@example.com', 'password': 'password123', 'name': 'Test'
    })
    assert response.status_code == 201

def test_security_headers(client):
    response = client.get('/')
    assert response.headers.get('X-Frame-Options') == 'DENY'
```

## Common Pitfalls

1. **SQLAlchemy re-registration**: Define models OUTSIDE `create_app()` to avoid "Table already defined" errors when running tests
2. **JWT token expiration**: Always handle `jwt.ExpiredSignatureError` and `jwt.InvalidTokenError`
3. **Rate limiter storage**: Default in-memory storage warns in production; use Redis for production
4. **Static file serving**: Use `send_from_directory('.', 'index.html')` for SPA-style routing
5. **CORS**: Initialize CORS before routes; configure origins properly for production

## Verification Checklist

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Register
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test"}'

# Login (capture token)
TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' | python -c "import sys,json;print(json.load(sys.stdin)['token'])")

# Protected route
curl http://localhost:5000/api/v1/projects -H "Authorization: Bearer $TOKEN"

# Security headers
curl -D - http://localhost:5000 | grep -i "x-frame\|x-content-type\|x-xss"

# Run tests
pytest test_app.py -v
```
