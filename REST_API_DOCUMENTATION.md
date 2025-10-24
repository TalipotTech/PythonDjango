# REST API Documentation - Django Quiz/Survey System

## Overview
This is a comprehensive REST API for the Django Quiz/Survey application with JWT authentication. The API provides full CRUD operations for all major models and includes advanced features like quiz progress tracking, session attendance, and analytics.

**Base URL:** `http://localhost:8000/api/`  
**API Version:** 2.0  
**Authentication:** JWT Bearer Token

---

## Table of Contents
1. [Authentication](#authentication)
2. [Sessions](#sessions)
3. [Attendees](#attendees)
4. [Questions](#questions)
5. [Responses](#responses)
6. [Reviews](#reviews)
7. [Quiz Progress](#quiz-progress)
8. [Attendance Tracking](#attendance-tracking)
9. [Admin Management](#admin-management)
10. [Hit Counter & Analytics](#hit-counter--analytics)
11. [Statistics](#statistics)

---

## Authentication

### Register New User
**POST** `/api/auth/register/`

Register a new user account.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password2": "securepassword123",
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

### Login (Get JWT Token)
**POST** `/api/auth/token/`

Obtain access and refresh tokens.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Refresh Token
**POST** `/api/auth/token/refresh/`

Get a new access token using refresh token.

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

### Get User Profile
**GET** `/api/auth/profile/`

Get current user's profile information.

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

## Sessions

### List All Sessions
**GET** `/api/sessions/`

Get list of all quiz sessions (paginated).

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20)
- `teacher` - Filter by teacher name
- `search` - Search in title, teacher, or session_code

**Response (200 OK):**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/sessions/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python Basics Workshop",
      "teacher": "Dr. Smith",
      "start_time": "2025-10-25T10:00:00Z",
      "end_time": "2025-10-25T12:00:00Z",
      "session_code": "ABC12345",
      "attendee_count": 25,
      "is_active": false,
      "time_until_start": 0,
      "time_until_end": 0
    }
  ]
}
```

---

### Get Active Sessions
**GET** `/api/sessions/active_sessions/`

Get currently active sessions (no authentication required).

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "title": "Web Development Bootcamp",
    "teacher": "Prof. Johnson",
    "start_time": "2025-10-24T09:00:00Z",
    "end_time": "2025-10-24T17:00:00Z",
    "session_code": "WEB98765",
    "attendee_count": 30,
    "is_active": true,
    "time_until_start": 0,
    "time_until_end": 3600
  }
]
```

---

### Get Upcoming Sessions
**GET** `/api/sessions/upcoming_sessions/`

Get future sessions that haven't started yet.

---

### Verify Session Code
**POST** `/api/sessions/verify_code/`

Check if a session code is valid and active.

**Request Body:**
```json
{
  "session_code": "ABC12345"
}
```

**Response (200 OK):**
```json
{
  "valid": true,
  "message": "Session code is valid",
  "session": {
    "id": 1,
    "title": "Python Basics Workshop",
    "teacher": "Dr. Smith",
    "start_time": "2025-10-25T10:00:00Z",
    "end_time": "2025-10-25T12:00:00Z",
    "session_code": "ABC12345",
    "attendee_count": 25,
    "is_active": true
  }
}
```

---

### Create Session (Admin Only)
**POST** `/api/sessions/`

Create a new quiz session.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Request Body:**
```json
{
  "title": "Django Advanced Topics",
  "teacher": "Dr. Martinez",
  "start_time": "2025-11-01T14:00:00Z",
  "end_time": "2025-11-01T16:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "id": 5,
  "title": "Django Advanced Topics",
  "teacher": "Dr. Martinez",
  "start_time": "2025-11-01T14:00:00Z",
  "end_time": "2025-11-01T16:00:00Z",
  "session_code": "DJG45678",
  "attendee_count": 0,
  "is_active": false
}
```

---

### Get Session Details
**GET** `/api/sessions/{id}/`

Get detailed information about a specific session including questions and attendees.

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Python Basics Workshop",
  "teacher": "Dr. Smith",
  "start_time": "2025-10-25T10:00:00Z",
  "end_time": "2025-10-25T12:00:00Z",
  "session_code": "ABC12345",
  "attendee_count": 25,
  "is_active": false,
  "questions": [...],
  "attendees": [...]
}
```

---

## Attendees

### Register Attendee
**POST** `/api/attendees/`

Register for a quiz session (no authentication required).

**Request Body:**
```json
{
  "name": "Jane Doe",
  "phone": "1234567890",
  "email": "jane@example.com",
  "age": 25,
  "place": "New York",
  "session_code": "ABC12345"
}
```

**Response (201 Created):**
```json
{
  "id": 15,
  "name": "Jane Doe",
  "phone": "1234567890",
  "email": "jane@example.com",
  "age": 25,
  "place": "New York",
  "class_session": 1,
  "session_title": "Python Basics Workshop",
  "session_code": "ABC12345",
  "has_submitted": false,
  "quiz_started_at": null,
  "created_at": "2025-10-24T10:30:00Z",
  "updated_at": "2025-10-24T10:30:00Z"
}
```

---

### List All Attendees (Admin Only)
**GET** `/api/attendees/`

**Query Parameters:**
- `class_session` - Filter by session ID
- `has_submitted` - Filter by submission status (true/false)
- `search` - Search by name, email, or place

---

### Get My Registrations
**GET** `/api/attendees/my_registrations/?email=jane@example.com`

Get all registrations for a specific email address.

**Headers:**
```
Authorization: Bearer <access_token>
```

---

### Submit Quiz
**POST** `/api/attendees/{id}/submit_quiz/`

Mark an attendee's quiz as submitted.

---

## Questions

### List Questions
**GET** `/api/questions/`

Get all questions (authenticated users only).

**Query Parameters:**
- `class_session` - Filter by session ID
- `question_type` - Filter by type (multiple_choice, text_response)

**Response (200 OK):**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "class_session": 1,
      "session_title": "Python Basics Workshop",
      "text": "What is a list in Python?",
      "question_type": "multiple_choice",
      "option1": "A mutable sequence",
      "option2": "A dictionary",
      "option3": "A string",
      "option4": "None of the above",
      "correct_option": 1
    }
  ]
}
```

Note: `correct_option` is hidden for non-staff users.

---

### Create Question (Admin Only)
**POST** `/api/questions/`

**Request Body:**
```json
{
  "class_session": 1,
  "text": "What is Django?",
  "question_type": "multiple_choice",
  "option1": "A web framework",
  "option2": "A database",
  "option3": "A programming language",
  "option4": "An IDE",
  "correct_option": 1
}
```

---

## Responses

### Submit Response
**POST** `/api/responses/`

Submit an answer to a question.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body (Multiple Choice):**
```json
{
  "attendee": 15,
  "question": 1,
  "selected_option": 1
}
```

**Request Body (Text Response):**
```json
{
  "attendee": 15,
  "question": 2,
  "text_response": "Django is a high-level Python web framework."
}
```

**Response (201 Created):**
```json
{
  "id": 42,
  "attendee": 15,
  "attendee_name": "Jane Doe",
  "question": 1,
  "question_text": "What is a list in Python?",
  "selected_option": 1,
  "text_response": null,
  "is_correct": true
}
```

---

### Get My Responses
**GET** `/api/responses/my_responses/?email=jane@example.com`

Get all responses submitted by a user.

---

## Reviews

### Submit Review
**POST** `/api/reviews/`

Submit feedback/review for a session.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "attendee": 15,
  "content": "Great session! Learned a lot about Python basics."
}
```

---

### List All Reviews (Admin Only)
**GET** `/api/reviews/`

---

## Quiz Progress

### Get Progress
**GET** `/api/progress/`

Get quiz progress records (authenticated users see only their own).

**Response (200 OK):**
```json
{
  "results": [
    {
      "id": 5,
      "attendee": 15,
      "attendee_name": "Jane Doe",
      "class_session": 1,
      "session_title": "Python Basics Workshop",
      "last_answered_at": "2025-10-24T11:30:00Z",
      "is_fully_completed": false,
      "progress_stats": {
        "total": 10,
        "answered": 7,
        "pending": 3,
        "percentage": 70.0
      },
      "answered_question_ids": [1, 2, 3, 4, 5, 6, 7]
    }
  ]
}
```

---

### Get My Progress
**GET** `/api/progress/my_progress/?email=jane@example.com`

---

### Update Completion Status
**POST** `/api/progress/{id}/update_completion/`

Check and update if all questions are answered.

---

## Attendance Tracking

### Get Attendance History
**GET** `/api/attendance/`

Get session attendance records.

**Response (200 OK):**
```json
{
  "results": [
    {
      "id": 8,
      "attendee": 15,
      "attendee_name": "Jane Doe",
      "attendee_email": "jane@example.com",
      "class_session": 1,
      "session_title": "Python Basics Workshop",
      "session_code": "ABC12345",
      "joined_at": "2025-10-24T10:35:00Z",
      "has_submitted": true
    }
  ]
}
```

---

### Get My Attendance
**GET** `/api/attendance/my_attendance/?email=jane@example.com`

---

### Get Session Attendees (Admin Only)
**GET** `/api/attendance/session_attendees/?session_id=1`

---

## Admin Management

### Register Admin
**POST** `/api/admins/register/`

Register a new admin account.

**Request Body:**
```json
{
  "username": "admin_user",
  "email": "admin@example.com",
  "password": "securepassword123",
  "password2": "securepassword123"
}
```

---

### List Admins (Admin Only)
**GET** `/api/admins/`

---

## Hit Counter & Analytics

### Get Hit Statistics (Admin Only)
**GET** `/api/hits/statistics/`

Get website traffic statistics.

**Response (200 OK):**
```json
{
  "total_hits": 5432,
  "unique_visitors": 1234,
  "hits_today": 156,
  "popular_pages": [
    {"path": "/", "hit_count": 2100},
    {"path": "/sessions/", "hit_count": 890},
    {"path": "/quiz/", "hit_count": 654}
  ]
}
```

---

### List Hit Records (Admin Only)
**GET** `/api/hits/`

---

## Statistics

### Dashboard Statistics (Admin Only)
**GET** `/api/stats/dashboard/`

Get comprehensive dashboard statistics.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Response (200 OK):**
```json
{
  "sessions": {
    "total": 50,
    "active": 2,
    "upcoming": 15,
    "past": 33
  },
  "attendees": {
    "total": 1234
  },
  "content": {
    "questions": 250,
    "responses": 8765,
    "reviews": 234
  },
  "traffic": {
    "total_hits": 5432,
    "unique_visitors": 1234
  },
  "recent_activity": {
    "attendees": [...],
    "reviews": [...]
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

---

## Usage Examples

### Python Requests Library

```python
import requests

BASE_URL = "http://localhost:8000/api"

# 1. Register a user
register_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
}
response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
print(response.json())

# 2. Login and get token
login_data = {
    "username": "testuser",
    "password": "testpass123"
}
response = requests.post(f"{BASE_URL}/auth/token/", json=login_data)
tokens = response.json()
access_token = tokens['access']

# 3. Use token to access protected endpoints
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Get active sessions
response = requests.get(f"{BASE_URL}/sessions/active_sessions/")
print(response.json())

# Register for a session
attendee_data = {
    "name": "John Smith",
    "phone": "1234567890",
    "email": "john@example.com",
    "age": 30,
    "place": "Boston",
    "session_code": "ABC12345"
}
response = requests.post(f"{BASE_URL}/attendees/", json=attendee_data)
attendee = response.json()

# Submit a response
response_data = {
    "attendee": attendee['id'],
    "question": 1,
    "selected_option": 1
}
response = requests.post(f"{BASE_URL}/responses/", json=response_data, headers=headers)
print(response.json())
```

---

### JavaScript (Fetch API)

```javascript
const BASE_URL = 'http://localhost:8000/api';

// Login
async function login(username, password) {
  const response = await fetch(`${BASE_URL}/auth/token/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access);
  return data;
}

// Get active sessions
async function getActiveSessions() {
  const response = await fetch(`${BASE_URL}/sessions/active_sessions/`);
  return await response.json();
}

// Register attendee
async function registerAttendee(attendeeData) {
  const response = await fetch(`${BASE_URL}/attendees/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(attendeeData)
  });
  return await response.json();
}

// Submit response with authentication
async function submitResponse(responseData) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`${BASE_URL}/responses/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(responseData)
  });
  return await response.json();
}
```

---

## Testing the API

### Using cURL

```bash
# Get API overview
curl http://localhost:8000/api/

# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"pass123","password2":"pass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123"}'

# Get active sessions
curl http://localhost:8000/api/sessions/active_sessions/

# Access protected endpoint
curl http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Browsable API

Django REST Framework provides a browsable API interface. Simply visit `http://localhost:8000/api/` in your web browser after starting the server to explore and test endpoints interactively.

---

## Notes

1. **Token Expiration:** Access tokens expire after 1 hour. Use the refresh token to get a new access token.
2. **Pagination:** Most list endpoints are paginated with 20 items per page by default.
3. **Filtering:** Use query parameters to filter results (e.g., `?class_session=1&has_submitted=true`).
4. **CORS:** CORS is configured for `localhost:3000` and `localhost:8080`. Update `settings.py` for production.
5. **Production:** Remember to:
   - Change `SECRET_KEY`
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Use HTTPS
   - Implement rate limiting
   - Add proper logging

---

## Support

For issues or questions, refer to the project documentation or contact the development team.
