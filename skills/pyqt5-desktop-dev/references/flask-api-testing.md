# Flask Backend API Testing Pattern

## Overview
WebBuilder uses a Flask backend with JWT authentication. This reference covers the API workflow for testing.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/v1/health | No | Health check |
| POST | /auth/register | No | Create user account |
| POST | /auth/login | No | Get JWT token |
| GET | /api/v1/projects | Bearer | List user's projects |
| POST | /api/v1/projects | Bearer | Create new project |
| POST | /api/v1/analytics | No | Track analytics event |
| POST | /auth/logout | Bearer | Invalidate session |

## Testing Workflow

```bash
# 1. Health check
curl -s http://localhost:5000/api/v1/health

# 2. Register
curl -s -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@webbuilder.com","password":"securepass123","name":"Test"}'

# 3. Login (extract token)
TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@webbuilder.com","password":"securepass123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['token'])")

# 4. Create project
curl -s -X POST http://localhost:5000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Website","description":"Test","content":"{}"}'

# 5. List projects
curl -s http://localhost:5000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN"
```

## Error Cases

| Case | Expected Response |
|------|-------------------|
| No token | `{"error":"Token missing"}` 401 |
| Invalid token | `{"error":"Invalid or expired token"}` 401 |
| Wrong password | `{"error":"Invalid credentials"}` 401 |
| Duplicate email | `{"error":"Email already registered"}` 409 |
| Short password | `{"error":"Password must be at least 8 characters"}` 400 |
| Missing project name | `{"error":"Name is required"}` 400 |

## Running the Backend

```bash
cd "/c/Users/Server/Desktop/WebBuilder/output"
python app.py 2>&1
# Running on http://127.0.0.1:5000
```

## JWT Token Handling

Tokens are generated with `jwt.encode()` using HS256 algorithm. The token payload contains:
- `user_id`: integer user ID
- `exp`: expiration timestamp (24 hours from issue)
- `iat`: issued-at timestamp

Tokens must be passed as `Authorization: Bearer <token>` header on protected routes.