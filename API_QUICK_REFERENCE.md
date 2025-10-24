# REST API Quick Reference Card

## Base URL
```
http://localhost:8000/api/
```

## Authentication Header
```
Authorization: Bearer <your_access_token>
```

---

## Quick Commands

### Get API Overview
```bash
curl http://localhost:8000/api/
```

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user@example.com","password":"pass123","password2":"pass123"}'
```

### Login (Get Token)
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123"}'
```

### Use Token
```bash
TOKEN="your_access_token_here"

curl http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Common Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/` | No | API overview |
| POST | `/api/auth/register/` | No | Register user |
| POST | `/api/auth/token/` | No | Login (get JWT) |
| POST | `/api/auth/token/refresh/` | No | Refresh token |
| GET | `/api/auth/profile/` | Yes | Get profile |
| GET | `/api/sessions/` | No | List sessions |
| GET | `/api/sessions/active_sessions/` | No | Active sessions |
| POST | `/api/sessions/verify_code/` | No | Verify session code |
| POST | `/api/attendees/` | No | Register attendee |
| GET | `/api/attendees/my_registrations/` | Yes | My registrations |
| GET | `/api/questions/` | Yes | List questions |
| POST | `/api/responses/` | Yes | Submit answer |
| GET | `/api/responses/my_responses/` | Yes | My responses |
| POST | `/api/reviews/` | Yes | Submit review |
| GET | `/api/progress/my_progress/` | Yes | My quiz progress |
| GET | `/api/attendance/my_attendance/` | Yes | My attendance |
| GET | `/api/stats/dashboard/` | Admin | Dashboard stats |

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Auth required |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error |

---

## Filtering Examples

```bash
# Filter sessions by teacher
/api/sessions/?teacher=Dr.+Smith

# Search sessions
/api/sessions/?search=python

# Filter attendees by session
/api/attendees/?class_session=1

# Filter by submission status
/api/attendees/?has_submitted=true

# Pagination
/api/sessions/?page=2&page_size=10

# Ordering
/api/sessions/?ordering=-start_time
```

---

## Python Quick Start

```python
import requests

BASE = "http://localhost:8000/api"

# Login
r = requests.post(f"{BASE}/auth/token/", 
    json={"username": "user1", "password": "pass123"})
token = r.json()['access']

# Use token
headers = {"Authorization": f"Bearer {token}"}

# Get sessions
r = requests.get(f"{BASE}/sessions/", headers=headers)
sessions = r.json()

# Register attendee
r = requests.post(f"{BASE}/attendees/", json={
    "name": "John Doe",
    "phone": "1234567890",
    "email": "john@example.com",
    "age": 25,
    "place": "Boston",
    "session_code": "ABC12345"
})
```

---

## JavaScript Quick Start

```javascript
const BASE = 'http://localhost:8000/api';

// Login
const loginRes = await fetch(`${BASE}/auth/token/`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username: 'user1', password: 'pass123'})
});
const {access} = await loginRes.json();

// Get sessions
const sessionsRes = await fetch(`${BASE}/sessions/`, {
  headers: {'Authorization': `Bearer ${access}`}
});
const sessions = await sessionsRes.json();
```

---

## Browsable API

Open in browser for interactive testing:
- http://localhost:8000/api/
- http://localhost:8000/api/sessions/
- http://localhost:8000/api/attendees/

---

## Documentation Files

- **REST_API_DOCUMENTATION.md** - Complete reference
- **REST_API_QUICK_START.md** - Getting started guide
- **REST_API_COMPLETE.md** - Implementation summary
- **test_rest_api.py** - Automated tests

---

## Tips

💡 Access tokens expire after 1 hour - use refresh token  
💡 Use browsable API for easy testing  
💡 Check response status codes for errors  
💡 Non-staff users can't see correct answers  
💡 Most endpoints support pagination, filtering, search  

---

## Start Server
```bash
python manage.py runserver
```

## Run Tests
```bash
python test_rest_api.py
```

---

**Happy API Development! 🚀**
