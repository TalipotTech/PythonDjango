# Swagger API Documentation & React Integration Guide

## 📋 Table of Contents
1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [React Integration Examples](#react-integration-examples)
5. [Error Handling](#error-handling)
6. [Testing with Swagger UI](#testing-with-swagger-ui)

---

## 🌐 API Overview

### Base URLs
- **Django Server**: `http://127.0.0.1:8000`
- **API Base**: `http://127.0.0.1:8000/api/`
- **Swagger UI**: `http://127.0.0.1:8000/api/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/`

### Authentication
Most endpoints require **JWT (JSON Web Token)** authentication.

**Authorization Header Format:**
```
Authorization: Bearer <your_access_token>
```

---

## 🔐 Authentication

### 1. User Registration
**Endpoint:** `POST /api/auth/register/`  
**Authentication:** Not required

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
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
**Authentication:** Not required

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 3. Refresh Token
**Endpoint:** `POST /api/auth/token/refresh/`  
**Authentication:** Not required

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 4. Get User Profile
**Endpoint:** `GET /api/auth/profile/`  
**Authentication:** Required

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_staff": false
}
```

---

## 📚 API Endpoints

### Sessions (Quiz Sessions)

#### List All Sessions
**Endpoint:** `GET /api/sessions/`  
**Authentication:** Not required

**Query Parameters:**
- `teacher` - Filter by teacher name
- `search` - Search in title, teacher, session_code
- `ordering` - Order by: `start_time`, `end_time`, `created_at`

**Response (200 OK):**
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/sessions/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introduction to Django REST Framework",
      "teacher": "Dr. Sarah Johnson",
      "start_time": "2025-11-01T10:00:00Z",
      "end_time": "2025-11-01T12:00:00Z",
      "session_code": "ABC12345",
      "attendee_count": 25,
      "is_active": true,
      "time_until_start": 0,
      "time_until_end": 7200
    }
  ]
}
```

---

#### Create Session (Admin Only)
**Endpoint:** `POST /api/sessions/`  
**Authentication:** Required (Admin)

**Request Body:**
```json
{
  "title": "Advanced Python Programming",
  "teacher": "Prof. Michael Chen",
  "start_time": "2025-11-05T14:00:00Z",
  "end_time": "2025-11-05T16:30:00Z"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "title": "Advanced Python Programming",
  "teacher": "Prof. Michael Chen",
  "start_time": "2025-11-05T14:00:00Z",
  "end_time": "2025-11-05T16:30:00Z",
  "session_code": "PYTHON01",
  "attendee_count": 0,
  "is_active": false,
  "time_until_start": 432000,
  "time_until_end": 441000
}
```

---

#### Get Active Sessions
**Endpoint:** `GET /api/sessions/active_sessions/`  
**Authentication:** Not required

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Introduction to Django REST Framework",
    "teacher": "Dr. Sarah Johnson",
    "start_time": "2025-11-01T10:00:00Z",
    "end_time": "2025-11-01T12:00:00Z",
    "session_code": "ABC12345",
    "attendee_count": 25,
    "is_active": true,
    "time_until_start": 0,
    "time_until_end": 7200
  }
]
```

---

#### Verify Session Code
**Endpoint:** `POST /api/sessions/verify_code/`  
**Authentication:** Not required

**Request Body:**
```json
{
  "session_code": "ABC12345"
}
```

**Response (200 OK - Valid):**
```json
{
  "valid": true,
  "message": "Session code is valid",
  "session": {
    "id": 1,
    "title": "Introduction to Django REST Framework",
    "teacher": "Dr. Sarah Johnson",
    "start_time": "2025-11-01T10:00:00Z",
    "end_time": "2025-11-01T12:00:00Z",
    "session_code": "ABC12345",
    "attendee_count": 25,
    "is_active": true,
    "time_until_start": 0,
    "time_until_end": 7200
  }
}
```

**Response (400 Bad Request - Not Started):**
```json
{
  "valid": false,
  "message": "Session has not started yet",
  "session": { ... }
}
```

---

### Attendees

#### Register as Attendee
**Endpoint:** `POST /api/attendees/`  
**Authentication:** Not required

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "1234567890",
  "email": "john.doe@example.com",
  "session_code": "ABC12345"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "phone": "1234567890",
  "email": "john.doe@example.com",
  "age": null,
  "place": "",
  "class_session": 1,
  "session_title": "Introduction to Django REST Framework",
  "session_code": "ABC12345",
  "has_submitted": false,
  "quiz_started_at": null,
  "created_at": "2025-10-31T10:00:00Z",
  "updated_at": "2025-10-31T10:00:00Z"
}
```

---

#### Get My Registrations
**Endpoint:** `GET /api/attendees/my_registrations/?email=john@example.com`  
**Authentication:** Required

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "phone": "1234567890",
    "email": "john.doe@example.com",
    "class_session": 1,
    "session_title": "Introduction to Django REST Framework",
    "has_submitted": false
  }
]
```

---

### Reviews/Feedback

#### Submit Feedback
**Endpoint:** `POST /api/reviews/`  
**Authentication:** Not required

**Request Body:**
```json
{
  "attendee": 1,
  "content": "Great workshop! Learned a lot about Django REST Framework.",
  "feedback_type": "review"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "attendee": 1,
  "attendee_name": "John Doe",
  "attendee_email": "john.doe@example.com",
  "content": "Great workshop! Learned a lot about Django REST Framework.",
  "submitted_at": "2025-10-31T12:00:00Z"
}
```

---

### Questions

#### List Questions for a Session
**Endpoint:** `GET /api/questions/?class_session=1`  
**Authentication:** Required

**Response (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "class_session": 1,
      "session_title": "Introduction to Django REST Framework",
      "text": "What is Django REST Framework?",
      "question_type": "multiple_choice",
      "option1": "A web framework",
      "option2": "An API toolkit",
      "option3": "A database",
      "option4": "A testing tool"
    }
  ]
}
```

**Note:** `correct_option` is hidden for non-admin users.

---

### Responses

#### Submit Quiz Response
**Endpoint:** `POST /api/responses/`  
**Authentication:** Required

**For Multiple Choice:**
```json
{
  "attendee": 1,
  "question": 1,
  "selected_option": 2
}
```

**For Text Response:**
```json
{
  "attendee": 1,
  "question": 5,
  "text_response": "Django REST Framework is a powerful toolkit for building Web APIs."
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "attendee": 1,
  "attendee_name": "John Doe",
  "question": 1,
  "question_text": "What is Django REST Framework?",
  "selected_option": 2,
  "text_response": null,
  "is_correct": true
}
```

---

## ⚛️ React Integration Examples

### Setup: API Service Class

Create `src/services/api.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

class APIService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add token to requests automatically
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Handle token refresh on 401 errors
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
              refresh: refreshToken,
            });

            const { access } = response.data;
            localStorage.setItem('access_token', access);

            originalRequest.headers.Authorization = `Bearer ${access}`;
            return this.api(originalRequest);
          } catch (refreshError) {
            // Redirect to login
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async register(userData) {
    const response = await this.api.post('/auth/register/', userData);
    return response.data;
  }

  async login(username, password) {
    const response = await this.api.post('/auth/token/', { username, password });
    const { access, refresh } = response.data;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    return response.data;
  }

  async getProfile() {
    const response = await this.api.get('/auth/profile/');
    return response.data;
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Sessions
  async getSessions(params = {}) {
    const response = await this.api.get('/sessions/', { params });
    return response.data;
  }

  async getSessionById(id) {
    const response = await this.api.get(`/sessions/${id}/`);
    return response.data;
  }

  async getActiveSessions() {
    const response = await this.api.get('/sessions/active_sessions/');
    return response.data;
  }

  async verifySessionCode(sessionCode) {
    const response = await this.api.post('/sessions/verify_code/', {
      session_code: sessionCode,
    });
    return response.data;
  }

  async createSession(sessionData) {
    const response = await this.api.post('/sessions/', sessionData);
    return response.data;
  }

  // Attendees
  async registerAttendee(attendeeData) {
    const response = await this.api.post('/attendees/', attendeeData);
    return response.data;
  }

  async getMyRegistrations(email) {
    const response = await this.api.get('/attendees/my_registrations/', {
      params: { email },
    });
    return response.data;
  }

  // Reviews/Feedback
  async submitFeedback(feedbackData) {
    const response = await this.api.post('/reviews/', feedbackData);
    return response.data;
  }

  // Questions
  async getQuestions(sessionId) {
    const response = await this.api.get('/questions/', {
      params: { class_session: sessionId },
    });
    return response.data;
  }

  // Responses
  async submitResponse(responseData) {
    const response = await this.api.post('/responses/', responseData);
    return response.data;
  }

  async getMyResponses(email) {
    const response = await this.api.get('/responses/my_responses/', {
      params: { email },
    });
    return response.data;
  }

  // Progress
  async getMyProgress(email) {
    const response = await this.api.get('/progress/my_progress/', {
      params: { email },
    });
    return response.data;
  }
}

export default new APIService();
```

---

### Example 1: Login Component

```jsx
import React, { useState } from 'react';
import api from '../services/api';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await api.login(username, password);
      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        {error && <div className="alert alert-error">{error}</div>}
        
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
}

export default LoginPage;
```

---

### Example 2: Session List Component

```jsx
import React, { useState, useEffect } from 'react';
import api from '../services/api';

function SessionList() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const data = await api.getSessions();
      setSessions(data.results);
    } catch (err) {
      setError('Failed to load sessions');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="alert alert-error">{error}</div>;

  return (
    <div className="session-list">
      <h2>Available Sessions</h2>
      {sessions.map((session) => (
        <div key={session.id} className="session-card">
          <h3>{session.title}</h3>
          <p>Teacher: {session.teacher}</p>
          <p>Code: <strong>{session.session_code}</strong></p>
          <p>
            {session.is_active ? (
              <span className="badge badge-success">Active Now</span>
            ) : (
              <span className="badge badge-secondary">Upcoming</span>
            )}
          </p>
          <p>Attendees: {session.attendee_count}</p>
        </div>
      ))}
    </div>
  );
}

export default SessionList;
```

---

### Example 3: Registration Component

```jsx
import React, { useState } from 'react';
import api from '../services/api';

function AttendeeRegistration() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    session_code: '',
  });
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Verify session code first
      const verifyResult = await api.verifySessionCode(formData.session_code);
      
      if (!verifyResult.valid) {
        setError(verifyResult.message);
        setLoading(false);
        return;
      }

      // Register attendee
      const result = await api.registerAttendee(formData);
      setSuccess(true);
      console.log('Registration successful:', result);
      
      // Redirect after 2 seconds
      setTimeout(() => {
        window.location.href = '/quiz';
      }, 2000);
      
    } catch (err) {
      const errorMsg = err.response?.data?.session_code?.[0] 
        || err.response?.data?.email?.[0]
        || 'Registration failed. Please try again.';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="alert alert-success">
        Registration successful! Redirecting to quiz...
      </div>
    );
  }

  return (
    <div className="registration-form">
      <h2>Register for Session</h2>
      <form onSubmit={handleSubmit}>
        {error && <div className="alert alert-error">{error}</div>}

        <div className="form-group">
          <label>Name *</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Email *</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Phone (10 digits) *</label>
          <input
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            pattern="[0-9]{10}"
            required
          />
        </div>

        <div className="form-group">
          <label>Session Code *</label>
          <input
            type="text"
            name="session_code"
            value={formData.session_code}
            onChange={handleChange}
            maxLength="10"
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
    </div>
  );
}

export default AttendeeRegistration;
```

---

### Example 4: Feedback/Review Component

```jsx
import React, { useState } from 'react';
import api from '../services/api';

function FeedbackForm({ attendeeId }) {
  const [content, setContent] = useState('');
  const [feedbackType, setFeedbackType] = useState('review');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await api.submitFeedback({
        attendee: attendeeId,
        content: content,
        feedback_type: feedbackType,
      });
      
      setSubmitted(true);
      setContent('');
      
    } catch (err) {
      setError('Failed to submit feedback. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="alert alert-success">
        Thank you for your feedback! 🎉
      </div>
    );
  }

  return (
    <div className="feedback-form">
      <h2>Submit Feedback</h2>
      <form onSubmit={handleSubmit}>
        {error && <div className="alert alert-error">{error}</div>}

        <div className="form-group">
          <label>Feedback Type</label>
          <select
            value={feedbackType}
            onChange={(e) => setFeedbackType(e.target.value)}
          >
            <option value="review">General Review</option>
            <option value="quiz">Quiz Feedback</option>
          </select>
        </div>

        <div className="form-group">
          <label>Your Feedback *</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows="6"
            placeholder="Share your thoughts about the workshop..."
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Submit Feedback'}
        </button>
      </form>
    </div>
  );
}

export default FeedbackForm;
```

---

### Example 5: Quiz Component with API

```jsx
import React, { useState, useEffect } from 'react';
import api from '../services/api';

function QuizPage({ sessionId, attendeeId }) {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [textAnswer, setTextAnswer] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const data = await api.getQuestions(sessionId);
      setQuestions(data.results);
    } catch (err) {
      setError('Failed to load questions');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async () => {
    const currentQuestion = questions[currentQuestionIndex];
    setLoading(true);

    try {
      const responseData = {
        attendee: attendeeId,
        question: currentQuestion.id,
      };

      if (currentQuestion.question_type === 'multiple_choice') {
        responseData.selected_option = selectedOption;
      } else {
        responseData.text_response = textAnswer;
      }

      await api.submitResponse(responseData);

      // Move to next question or finish
      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
        setSelectedOption(null);
        setTextAnswer('');
      } else {
        setSubmitted(true);
      }
    } catch (err) {
      setError('Failed to submit answer');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading quiz...</div>;
  if (error) return <div className="alert alert-error">{error}</div>;
  if (submitted) {
    return (
      <div className="alert alert-success">
        <h2>Quiz Completed! 🎉</h2>
        <p>Thank you for participating.</p>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];

  return (
    <div className="quiz-container">
      <div className="quiz-progress">
        Question {currentQuestionIndex + 1} of {questions.length}
      </div>

      <div className="question-card">
        <h3>{currentQuestion.text}</h3>

        {currentQuestion.question_type === 'multiple_choice' ? (
          <div className="options">
            {[1, 2, 3, 4].map((optionNum) => {
              const optionText = currentQuestion[`option${optionNum}`];
              if (!optionText) return null;

              return (
                <label key={optionNum} className="option-label">
                  <input
                    type="radio"
                    name="answer"
                    value={optionNum}
                    checked={selectedOption === optionNum}
                    onChange={() => setSelectedOption(optionNum)}
                  />
                  {optionText}
                </label>
              );
            })}
          </div>
        ) : (
          <textarea
            value={textAnswer}
            onChange={(e) => setTextAnswer(e.target.value)}
            placeholder="Type your answer here..."
            rows="5"
          />
        )}

        <button
          onClick={handleSubmitAnswer}
          disabled={
            loading ||
            (currentQuestion.question_type === 'multiple_choice' && !selectedOption) ||
            (currentQuestion.question_type === 'text_response' && !textAnswer)
          }
        >
          {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'Submit Quiz'}
        </button>
      </div>
    </div>
  );
}

export default QuizPage;
```

---

## 🚨 Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "field_name": ["Error message"],
  "session_code": ["Invalid session code."]
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

### React Error Handling Example

```javascript
const handleAPICall = async () => {
  try {
    const result = await api.someMethod();
    // Handle success
  } catch (error) {
    if (error.response) {
      // Server responded with error
      const status = error.response.status;
      const data = error.response.data;

      switch (status) {
        case 400:
          // Validation error
          console.error('Validation errors:', data);
          break;
        case 401:
          // Not authenticated
          window.location.href = '/login';
          break;
        case 403:
          // Not authorized
          alert('You do not have permission');
          break;
        case 404:
          // Not found
          alert('Resource not found');
          break;
        case 500:
          // Server error
          alert('Server error. Please try again later.');
          break;
        default:
          alert('An error occurred');
      }
    } else if (error.request) {
      // Request made but no response
      alert('Network error. Please check your connection.');
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
  }
};
```

---

## 🧪 Testing with Swagger UI

### Access Swagger UI
Navigate to: `http://127.0.0.1:8000/api/swagger/`

### Steps to Test:

1. **Authenticate:**
   - Scroll to `/api/auth/token/` endpoint
   - Click "Try it out"
   - Enter username and password
   - Execute
   - Copy the `access` token
   - Click "Authorize" button at top
   - Enter: `Bearer <your_token>`

2. **Test Endpoints:**
   - Click any endpoint
   - Click "Try it out"
   - Fill in parameters
   - Click "Execute"
   - View response

3. **No Auth Required:**
   - Registration endpoints
   - Session listing
   - Feedback submission

---

## 📦 React Project Setup

### Install Dependencies

```bash
npm install axios
# or
yarn add axios
```

### Environment Variables

Create `.env`:
```
REACT_APP_API_URL=http://127.0.0.1:8000/api
```

### CORS Configuration (Django)

Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

Install:
```bash
pip install django-cors-headers
```

---

## 🔗 Quick Reference

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/auth/register/` | POST | ❌ | Register user |
| `/api/auth/token/` | POST | ❌ | Login |
| `/api/auth/token/refresh/` | POST | ❌ | Refresh token |
| `/api/auth/profile/` | GET | ✅ | Get profile |
| `/api/sessions/` | GET | ❌ | List sessions |
| `/api/sessions/` | POST | ✅ Admin | Create session |
| `/api/sessions/active_sessions/` | GET | ❌ | Active sessions |
| `/api/sessions/verify_code/` | POST | ❌ | Verify code |
| `/api/attendees/` | POST | ❌ | Register attendee |
| `/api/attendees/my_registrations/` | GET | ✅ | My registrations |
| `/api/reviews/` | POST | ❌ | Submit feedback |
| `/api/questions/` | GET | ✅ | Get questions |
| `/api/responses/` | POST | ✅ | Submit response |

---

## 📞 Support

For issues or questions:
- Check Swagger UI: `http://127.0.0.1:8000/api/swagger/`
- Check ReDoc: `http://127.0.0.1:8000/api/redoc/`
- View API overview: `http://127.0.0.1:8000/api/`

---

**Last Updated:** October 31, 2025
