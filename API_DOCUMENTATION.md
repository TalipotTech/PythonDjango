# 🚀 Ensate Workshops - REST API & JWT Authentication Guide

## 📋 Overview

This API provides JWT-based authentication and RESTful endpoints for managing quiz sessions, attendees, questions, responses, and feedback.

### Features Implemented:
- ✅ JWT Authentication (Access & Refresh Tokens)
- ✅ User Registration & Profile Management
- ✅ RESTful API for all models
- ✅ Hit Counter Application (Track page visits)
- ✅ Role-based Authorization (Admin vs User)
- ✅ CORS Support for frontend applications
- ✅ API Documentation & Browsable API

---

## 🔧 Installation

### Quick Install:
```powershell
.\install_api.ps1
```

### Manual Install:
```powershell
# Install packages
pip install djangorestframework djangorestframework-simplejwt django-cors-headers django-filter

# Create & apply migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
```

---

## 🔐 Authentication

### 1. User Registration
**Endpoint:** `POST /api/auth/register/`

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password2": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_staff": false
    },
    "message": "User registered successfully. Please login to get your access token."
}
```

---

### 2. Login (Get JWT Token)
**Endpoint:** `POST /api/auth/token/`

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Token Lifetime:**
- Access Token: 1 hour
- Refresh Token: 7 days

---

### 3. Refresh Token
**Endpoint:** `POST /api/auth/token/refresh/`

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 4. Get/Update Profile
**Endpoint:** `GET/PUT /api/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_staff": false
}
```

---

## 📚 API Endpoints

### Quiz Sessions

#### List All Sessions
```
GET /api/sessions/
```
**Public endpoint** - No authentication required

**Response:**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Python Django Workshop",
            "teacher": "SAMEESH KUMAR.P.K",
            "start_time": "2025-10-23T09:00:00Z",
            "end_time": "2025-10-23T16:00:00Z",
            "session_code": "ABC12345",
            "attendee_count": 15,
            "is_active": true,
            "time_until_start": 0,
            "time_until_end": 25200,
            "created_at": "2025-10-20T10:00:00Z"
        }
    ]
}
```

#### Get Active Sessions
```
GET /api/sessions/active_sessions/
```

#### Get Upcoming Sessions
```
GET /api/sessions/upcoming_sessions/
```

#### Verify Session Code
```
POST /api/sessions/verify_code/
```

**Request:**
```json
{
    "session_code": "ABC12345"
}
```

**Response:**
```json
{
    "valid": true,
    "message": "Session code is valid",
    "session": { /* session details */ }
}
```

#### Create Session (Admin Only)
```
POST /api/sessions/
Authorization: Bearer <access_token>
```

**Request:**
```json
{
    "title": "Advanced AI Workshop",
    "teacher": "Expert Instructor",
    "start_time": "2025-10-25T09:00:00Z",
    "end_time": "2025-10-25T17:00:00Z"
}
```

---

### Attendees

#### Register Attendee
```
POST /api/attendees/
```
**Public endpoint** - No authentication required

**Request:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25,
    "gender": "Male",
    "place": "New York",
    "session_code": "ABC12345"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25,
    "gender": "Male",
    "place": "New York",
    "class_session": 1,
    "session_title": "Python Django Workshop",
    "session_code": "ABC12345",
    "session_code_used": "ABC12345",
    "quiz_started_at": null,
    "quiz_completed": false,
    "created_at": "2025-10-23T10:00:00Z"
}
```

#### List Attendees (Admin Only)
```
GET /api/attendees/
Authorization: Bearer <access_token>
```

#### Get My Registrations
```
GET /api/attendees/my_registrations/?email=john@example.com
Authorization: Bearer <access_token>
```

---

### Questions

#### List Questions
```
GET /api/questions/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `session`: Filter by session ID
- `question_type`: Filter by type (text, multiple_choice)

**Response:**
```json
{
    "count": 10,
    "results": [
        {
            "id": 1,
            "session": 1,
            "session_title": "Python Django Workshop",
            "question_text": "What is Django?",
            "question_type": "multiple_choice",
            "options": ["Framework", "Library", "Language"],
            "created_at": "2025-10-20T10:00:00Z"
        }
    ]
}
```

**Note:** `correct_answer` field is hidden for non-staff users.

---

### Responses

#### Submit Response
```
POST /api/responses/
Authorization: Bearer <access_token>
```

**Request:**
```json
{
    "attendee": 1,
    "question": 1,
    "text_response": "Framework"
}
```

#### Get My Responses
```
GET /api/responses/my_responses/?email=john@example.com
Authorization: Bearer <access_token>
```

---

### Reviews/Feedback

#### Submit Review
```
POST /api/reviews/
Authorization: Bearer <access_token>
```

**Request:**
```json
{
    "attendee": 1,
    "session": 1,
    "content": "Excellent workshop! Learned a lot about Django."
}
```

#### List All Reviews (Admin Only)
```
GET /api/reviews/
Authorization: Bearer <access_token>
```

---

### Statistics (Admin Only)

#### Dashboard Statistics
```
GET /api/stats/dashboard/
Authorization: Bearer <admin_access_token>
```

**Response:**
```json
{
    "sessions": {
        "total": 10,
        "active": 2,
        "upcoming": 3,
        "past": 5
    },
    "attendees": {
        "total": 150,
        "completed": 120,
        "completion_rate": 80.0
    },
    "content": {
        "questions": 50,
        "responses": 1500,
        "reviews": 100
    },
    "traffic": {
        "total_hits": 5000,
        "unique_visitors": 800
    },
    "recent_activity": {
        "attendees": [ /* last 5 attendees */ ],
        "reviews": [ /* last 5 reviews */ ]
    }
}
```

---

## 📊 Hit Counter Application

### Features:
- ✅ Automatic tracking of all page visits
- ✅ Records IP address, user agent, path, method
- ✅ Tracks unique visitors
- ✅ Statistics by date, page, user

### Model Fields:
```python
class HitCounter(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40)
    user = models.ForeignKey(User)  # If authenticated
```

### Statistics Methods:
```python
HitCounter.get_total_hits()           # Total hits
HitCounter.get_unique_visitors()      # Unique IPs
HitCounter.get_hits_today()           # Today's hits
HitCounter.get_popular_pages(10)      # Top 10 pages
```

### View in Admin:
1. Go to: http://127.0.0.1:8000/django-admin/
2. Login with admin credentials
3. View "Hit Counters" section

---

## 🧪 Testing the API

### Using cURL:

**Register User:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"TestPass123","password2":"TestPass123"}'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}'
```

**Get Sessions (with token):**
```bash
curl -X GET http://127.0.0.1:8000/api/sessions/ \
  -H "Authorization: Bearer <your_access_token>"
```

---

### Using Postman:

1. **Import Collection:**
   - Create new collection "Ensate Workshops API"
   - Add requests for each endpoint

2. **Set Environment Variables:**
   - `base_url`: http://127.0.0.1:8000
   - `access_token`: (obtained from login)

3. **Test Flow:**
   - Register → Login → Get Token → Use Token in Headers

---

## 🔒 Authorization Levels

### Public Endpoints (No Auth Required):
- GET `/api/sessions/`
- GET `/api/sessions/active_sessions/`
- GET `/api/sessions/upcoming_sessions/`
- POST `/api/sessions/verify_code/`
- POST `/api/attendees/` (Registration)
- POST `/api/auth/register/`
- POST `/api/auth/token/`

### Authenticated Users:
- GET/PUT `/api/auth/profile/`
- GET `/api/attendees/my_registrations/`
- GET `/api/questions/`
- GET/POST `/api/responses/`
- POST `/api/reviews/`

### Admin Only:
- POST/PUT/DELETE `/api/sessions/`
- GET `/api/attendees/` (list all)
- POST/PUT/DELETE `/api/questions/`
- GET `/api/reviews/` (list all)
- GET `/api/stats/dashboard/`

---

## 🌐 CORS Configuration

Allowed origins (for frontend apps):
- http://localhost:3000
- http://localhost:8080
- http://127.0.0.1:3000
- http://127.0.0.1:8080

To add more origins, edit `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://your-frontend-domain.com",
]
```

---

## 📱 Frontend Integration Example

### JavaScript (Fetch API):

```javascript
// Login
async function login(username, password) {
    const response = await fetch('http://127.0.0.1:8000/api/auth/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
}

// Get Sessions (with auth)
async function getSessions() {
    const token = localStorage.getItem('access_token');
    const response = await fetch('http://127.0.0.1:8000/api/sessions/', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return await response.json();
}

// Register Attendee
async function registerAttendee(data) {
    const response = await fetch('http://127.0.0.1:8000/api/attendees/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return await response.json();
}
```

---

## 🐛 Troubleshooting

### Common Issues:

**1. "Authorization header must contain two space-delimited values"**
- Solution: Use `Bearer <token>` format, not just `<token>`

**2. "Token is invalid or expired"**
- Solution: Use refresh token to get new access token

**3. "CORS error"**
- Solution: Add your frontend URL to `CORS_ALLOWED_ORIGINS` in settings.py

**4. "Method not allowed"**
- Solution: Check if endpoint supports the HTTP method (GET/POST/PUT/DELETE)

---

## 📝 Summary

**What's Been Added:**
1. ✅ JWT Authentication System
2. ✅ REST API for all models
3. ✅ Hit Counter Application
4. ✅ Role-based Authorization
5. ✅ API Documentation
6. ✅ CORS Support

**Next Steps:**
1. Run `.\install_api.ps1` to install
2. Test API at http://127.0.0.1:8000/api/
3. Create frontend application
4. Integrate with mobile apps

**Support:**
- API Docs: http://127.0.0.1:8000/api/
- Browsable API: http://127.0.0.1:8000/api/sessions/
- Django Admin: http://127.0.0.1:8000/django-admin/
