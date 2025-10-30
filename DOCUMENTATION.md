# Ensate Workshops - Quiz Management System
## Complete Project Documentation

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)
![Python](https://img.shields.io/badge/Python-3.13+-yellow.svg)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Installation & Setup](#installation--setup)
5. [User Roles & Workflows](#user-roles--workflows)
6. [Core Features Documentation](#core-features-documentation)
7. [REST API Documentation](#rest-api-documentation)
8. [Database Schema](#database-schema)
9. [Configuration](#configuration)
10. [Testing Guide](#testing-guide)
11. [Deployment](#deployment)
12. [Troubleshooting](#troubleshooting)
13. [Contributing](#contributing)

---

## 🎯 Project Overview

**Ensate Workshops** is a comprehensive Django-based quiz and survey management system designed for educational workshops, training sessions, and online assessments. It provides a complete platform for managing quiz sessions, tracking student progress, and analyzing results.

### Key Highlights

- **Multi-Session Support**: Create and manage unlimited quiz sessions with unique session codes
- **Flexible Question System**: Support for multiple-choice and text-response questions
- **Real-Time Progress Tracking**: Monitor student progress and completion status
- **Email Integration**: Automated email notifications with Gmail SMTP support
- **RESTful API**: Complete JWT-authenticated REST API for mobile/external applications
- **Admin Dashboard**: Comprehensive admin interface for managing all aspects
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5
- **Hit Counter**: Track page visits and analytics

---

## ✨ Features

### For Students
- ✅ **Email-Based Registration** - Secure registration with session code verification
- ✅ **Smart Login System** - Auto-detects returning users
- ✅ **Session Home Dashboard** - View session details, countdown timers, and progress
- ✅ **Flexible Quiz System** - Answer questions in any order, save partial progress
- ✅ **Multi-Session Support** - Join and complete multiple sessions
- ✅ **Real-Time Timer** - Dynamic countdown timer (5 minutes per question)
- ✅ **Progress Tracking** - See answered/pending questions and completion percentage
- ✅ **Feedback System** - Submit quiz feedback and general reviews
- ✅ **Personal Dashboard** - View scores, responses, and submission history

### For Admins
- ✅ **Powerful Admin Dashboard** - Statistics, search, and filtering
- ✅ **Session Management** - Create/edit/delete quiz sessions
- ✅ **Question Management** - Add multiple-choice and text-response questions
- ✅ **Student Management** - View student details, responses, and scores
- ✅ **Analytics** - Track attendance, completion rates, and performance
- ✅ **Bulk Operations** - Delete multiple records at once
- ✅ **Review Management** - View and manage student feedback
- ✅ **Hit Counter Analytics** - Track page visits and user behavior

### Technical Features
- 🔐 **Secure Authentication** - Password hashing with Django's PBKDF2
- 📧 **Email Integration** - Gmail SMTP with fallback to file backend
- 🔌 **REST API** - Full-featured API with JWT authentication
- 🌐 **CORS Support** - Enable cross-origin requests for external apps
- 📊 **Progress Persistence** - Resume incomplete quizzes anytime
- ⏱️ **Timezone Support** - Proper timezone handling (Asia/Kolkata)
- 🎨 **Modern UI** - Bootstrap 5 with custom CSS
- 📱 **Responsive Design** - Works on all devices

---

## 🏗️ System Architecture

### Project Structure

```
PythonDjango/
├── questionnaire_project/      # Django project settings
│   ├── settings.py            # Configuration (DB, email, API)
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI server config
│   └── asgi.py                # ASGI server config
│
├── survey/                     # Main application
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── forms.py               # Django forms
│   ├── urls.py                # App URL routing
│   ├── admin.py               # Django admin config
│   ├── middleware.py          # Custom middleware
│   ├── email_utils.py         # Email utilities
│   ├── smtp_email.py          # SMTP email functions
│   │
│   ├── api_views.py           # AJAX API views
│   ├── rest_api_views.py      # REST API ViewSets
│   ├── serializers.py         # DRF serializers
│   ├── api_urls.py            # REST API routing
│   │
│   ├── templates/             # HTML templates
│   │   ├── base.html
│   │   └── survey/            # App templates
│   │       ├── home.html
│   │       ├── admin_*.html
│   │       ├── student_*.html
│   │       └── ...
│   │
│   ├── static/                # Static assets
│   │   ├── css/
│   │   └── js/
│   │
│   ├── migrations/            # Database migrations
│   └── management/            # Custom management commands
│
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management script
├── requirements_api.txt       # Python dependencies
└── Documentation Files        # Various .md guides
```

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 5.2.6 |
| **Database** | SQLite3 (development) / PostgreSQL (production) |
| **REST API** | Django REST Framework 3.14 |
| **Authentication** | JWT (Simple JWT 5.3) |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Email** | Django Email + Gmail SMTP |
| **Server** | Django Development Server / Gunicorn |

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.13+ installed
- Git (optional)
- Gmail account (for email features)

### Step 1: Clone/Download Project

```bash
# Option 1: Clone with Git
git clone https://github.com/TalipotTech/PythonDjango.git
cd PythonDjango

# Option 2: Download ZIP and extract
```

### Step 2: Create Virtual Environment

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install base Django packages
pip install django==5.2.6

# Install REST API packages (optional but recommended)
pip install -r requirements_api.txt
```

**What gets installed:**
- Django REST Framework
- Simple JWT (for token authentication)
- Django CORS Headers
- Django Filter

### Step 4: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create admin account
python create_admin.py
```

Follow the prompts to create your first admin user.

### Step 5: Run Development Server

```bash
python manage.py runserver
```

Visit **http://localhost:8000** in your browser.

### Step 6: Email Configuration (Optional)

**Option 1: File Backend (Default - No Setup Required)**
- Emails saved to `sent_emails/` folder
- Open files with Notepad to view session codes

**Option 2: Gmail SMTP (Recommended for Production)**

1. Generate Gmail App Password:
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Generate App Password for "Mail"

2. Run setup script:
```bash
.\setup_smtp_permanent.ps1
```

3. Enter your Gmail and App Password when prompted.

---

## 👥 User Roles & Workflows

### Student Workflow

```mermaid
graph TD
    A[Visit Homepage] --> B{Returning User?}
    B -->|No| C[Click Session]
    B -->|Yes| D[Login with Password]
    C --> E[Enter Email]
    E --> F[Receive Session Code]
    F --> G[Verify Code]
    G --> H[Register: Name, Phone, Password]
    D --> I[Session Home]
    H --> I
    I --> J{Quiz Status?}
    J -->|Active| K[Start Quiz]
    J -->|Not Started| L[Wait for Countdown]
    J -->|Expired| M[View Results]
    K --> N[Answer Questions]
    N --> O{All Complete?}
    O -->|No| P[Save Progress & Return Later]
    O -->|Yes| Q[Submit Quiz]
    Q --> R[View Score & Feedback]
```

### Admin Workflow

```mermaid
graph TD
    A[Admin Login] --> B[Admin Dashboard]
    B --> C[Create Session]
    C --> D[Add Questions]
    D --> E[Generate Session Code]
    E --> F[Share with Students]
    F --> G[Monitor Progress]
    G --> H{Session Active?}
    H -->|Yes| I[Add More Questions]
    H -->|No| J[View Results]
    J --> K[Export Data]
    I --> G
```

---

## 📚 Core Features Documentation

### 1. Multi-Session Dynamic Quiz System

#### Features
- **Unlimited Sessions**: Create multiple concurrent sessions
- **Unique Session Codes**: Auto-generated 8-character codes
- **Time-Bound Access**: Sessions have start and end times
- **Live Countdowns**: Real-time countdown timers on all pages

#### Creating a Session (Admin)

1. Login to Admin Dashboard
2. Click "Create New Session"
3. Fill in details:
   - **Title**: Session name (e.g., "Python Workshop - Day 1")
   - **Teacher**: Instructor name
   - **Start Time**: When quiz becomes available
   - **End Time**: When quiz closes
4. Click "Save" - session code auto-generated

#### Joining a Session (Student)

**Method 1: Via Homepage**
1. Click on session card
2. Click "Request Session Code"
3. Enter email → Receive code via email
4. Enter session code
5. Register/Login
6. Access quiz

**Method 2: Direct Code Entry**
1. Click "Have a code? Enter it here"
2. Enter session code
3. Identify as new/returning user
4. Register/Login
5. Access quiz

### 2. Flexible Question System

#### Question Types

**Multiple Choice**
- 4 options per question
- 1 correct answer
- Auto-graded
- Score calculated automatically

**Text Response**
- Open-ended questions
- Student types answer
- Not auto-graded
- For feedback/opinions

#### Adding Questions (Admin)

1. Navigate to session view
2. Click "Add Question"
3. Select question type
4. Fill in:
   - **Question Text**: The question
   - **Options**: For multiple choice (4 options)
   - **Correct Answer**: Mark the correct option
5. Click "Add Question"

#### Dynamic Question Addition

**Key Feature**: Questions can be added even while students are taking the quiz!

- Students see **only unanswered questions**
- New questions appear automatically
- Progress tracked per student
- Students can return to answer new questions

### 3. Progress Tracking & Resume

#### How It Works

1. **QuizProgress Model** tracks each student's progress per session
2. **Response Model** stores individual answers
3. **SessionAttendance** tracks which sessions a student joined

#### Progress Statistics

For each student-session combination:
- ✅ Total questions in session
- ✅ Questions answered
- ✅ Questions pending
- ✅ Completion percentage
- ✅ Is fully completed?

#### Resuming a Quiz

Students can:
- Close browser and return later
- Answer questions in any order
- Save partial progress
- Return to complete remaining questions

**Scenario**: Admin adds 5 more questions while student is online
- Student sees 5 new questions
- Previous answers preserved
- Progress updates automatically

### 4. Email Integration

#### Features

- Welcome emails on registration
- Session code delivery
- Password reset (future)
- Quiz submission confirmation

#### Email Backends

**File Backend (Default)**
- No configuration needed
- Emails saved to `sent_emails/` folder
- Great for development

**SMTP Backend (Production)**
- Gmail SMTP integration
- Real email delivery
- Uses App Passwords for security

#### Setup SMTP Email

```powershell
# Run setup script
.\setup_smtp_permanent.ps1

# Enter when prompted:
# - Your Gmail address
# - App Password (not your regular password)
```

#### Email Functions

Located in `survey/email_utils.py`:

```python
send_welcome_email(email, name)
send_session_code_email(email, name, session_code, session_title, teacher)
```

### 5. Session Home Dashboard

#### For Students

The session home page shows:

**Session Status**
- ⏳ **Waiting**: Quiz not started yet (shows countdown)
- ✅ **Active**: Quiz is live (shows time remaining)
- 🔴 **Expired**: Quiz ended (shows results)

**Progress Panel**
- Total questions
- Answered questions
- Pending questions
- Completion percentage
- Visual progress bar

**Actions**
- Start Quiz (if active)
- Resume Quiz (if partially complete)
- View Results (if expired)
- Logout

**Dynamic Countdown**
- Days, hours, minutes, seconds
- Updates every second via JavaScript
- Redirects automatically when quiz goes live

### 6. Quiz Timer System

#### Time Calculation

**Formula**: 5 minutes per question

- Session has 10 questions = 50 minutes total
- Session has 20 questions = 100 minutes total

**Timer starts** when student clicks "Start Quiz"

#### Timer Features

- ⏱️ Displays remaining time in HH:MM:SS format
- 🔄 Updates every second
- ⚠️ Warning when < 5 minutes remaining
- 🛑 Auto-submits when time expires

#### Timer Implementation

```javascript
// In quiz.html template
var timeRemaining = {{ time_remaining_seconds }};

setInterval(function() {
    timeRemaining--;
    updateTimerDisplay();
    
    if (timeRemaining <= 0) {
        alert("Time's up! Quiz auto-submitted.");
        document.getElementById('quiz-form').submit();
    }
}, 1000);
```

### 7. Admin Dashboard

#### Overview Section

**Statistics Cards**
- Total Sessions (with status breakdown)
- Total Students
- Total Questions
- Total Responses
- Total Reviews

**Search & Filter**
- Search by name, email, phone, content
- Filter by:
  - All / Sessions / Students / Reviews
  - Active / Inactive / Finished (for sessions)

#### Sessions Section

**Displays**:
- Session title & teacher
- Start/End times
- Session code
- Status badge (Active/Inactive/Finished)
- Number of attendees
- Number of questions

**Actions**:
- View session details
- Edit session
- Add questions
- Delete session

#### Students Section

**Displays**:
- Name, email, phone
- Current session
- Registration date
- Submit status
- All attended sessions

**Actions**:
- View student details (all sessions, scores, responses)
- Edit student info
- Delete student
- Bulk delete

#### Reviews Section

**Displays**:
- Student name
- Review content (excerpt)
- Submission date
- Feedback type (Quiz/General)

**Actions**:
- View full review
- Delete review
- Bulk delete

### 8. Student Dashboard

#### Personal Information
- Name, email, phone
- Registration date

#### Session History
Shows all attended sessions with:
- Session title
- Score (% for multiple-choice questions)
- Total responses
- Completion status

#### Detailed Responses
For each session:
- **Multiple Choice Answers**: Question, selected answer, correct answer, result (✓/✗)
- **Text Responses**: Question and typed answer

#### Reviews
- All reviews submitted by the student
- Timestamps

---

## 🔌 REST API Documentation

### API Overview

The system includes a comprehensive RESTful API with JWT authentication for building mobile apps or integrating with external systems.

**Base URL**: `http://localhost:8000/api/`

**Authentication**: JWT Bearer Token

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response**:
```json
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "message": "User registered successfully. Please login to get your access token."
}
```

#### Login (Get Token)
```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password123"
}
```

**Response**:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Get User Profile
```http
GET /api/auth/profile/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Session Endpoints

#### List All Sessions
```http
GET /api/sessions/
Authorization: Bearer <token>
```

**Query Parameters**:
- `?search=python` - Search by title/teacher
- `?teacher=John` - Filter by teacher
- `?ordering=-start_time` - Sort by start time (descending)

#### Get Active Sessions
```http
GET /api/sessions/active_sessions/
```

Returns sessions that are currently active (start_time ≤ now ≤ end_time).

#### Verify Session Code
```http
POST /api/sessions/verify_code/
Content-Type: application/json

{
    "session_code": "ABC12345"
}
```

**Response**:
```json
{
    "valid": true,
    "message": "Session code is valid",
    "session": {
        "id": 5,
        "title": "Python Workshop",
        "session_code": "ABC12345",
        "start_time": "2025-10-28T10:00:00+05:30",
        "end_time": "2025-10-28T12:00:00+05:30"
    }
}
```

### Attendee Endpoints

#### Register Attendee
```http
POST /api/attendees/
Content-Type: application/json

{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "9876543210",
    "password": "securepass123",
    "class_session": 5
}
```

#### Get My Registrations
```http
GET /api/attendees/my_registrations/?email=jane@example.com
Authorization: Bearer <token>
```

### Question Endpoints

#### List Questions for Session
```http
GET /api/questions/?class_session=5
Authorization: Bearer <token>
```

#### Create Question (Admin Only)
```http
POST /api/questions/
Authorization: Bearer <token>
Content-Type: application/json

{
    "text": "What is Python?",
    "question_type": "multiple_choice",
    "option1": "A programming language",
    "option2": "A snake",
    "option3": "A framework",
    "option4": "A database",
    "correct_option": 1,
    "class_session": 5
}
```

### Response Endpoints

#### Submit Response
```http
POST /api/responses/
Authorization: Bearer <token>
Content-Type: application/json

{
    "attendee": 3,
    "question": 12,
    "selected_option": 1
}
```

For text response:
```json
{
    "attendee": 3,
    "question": 13,
    "text_response": "My answer here..."
}
```

#### Get My Responses
```http
GET /api/responses/my_responses/?email=jane@example.com
Authorization: Bearer <token>
```

### Progress Endpoints

#### Get My Progress
```http
GET /api/progress/my_progress/?email=jane@example.com
Authorization: Bearer <token>
```

**Response**:
```json
[
    {
        "id": 1,
        "attendee": {
            "id": 3,
            "name": "Jane Smith"
        },
        "class_session": {
            "id": 5,
            "title": "Python Workshop"
        },
        "is_fully_completed": false,
        "progress_stats": {
            "total": 10,
            "answered": 7,
            "pending": 3,
            "percentage": 70.0
        },
        "last_answered_at": "2025-10-28T11:30:00+05:30"
    }
]
```

### Admin Endpoints

#### Dashboard Statistics (Admin Only)
```http
GET /api/stats/dashboard/
Authorization: Bearer <token>
```

**Response**:
```json
{
    "sessions": {
        "total": 15,
        "active": 3,
        "upcoming": 5,
        "past": 7
    },
    "attendees": {
        "total": 250
    },
    "content": {
        "questions": 180,
        "responses": 2400,
        "reviews": 120
    },
    "traffic": {
        "total_hits": 5420,
        "unique_visitors": 312
    }
}
```

### API Testing with cURL

```bash
# Get active sessions
curl http://localhost:8000/api/sessions/active_sessions/

# Login
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","password":"pass123"}'

# Get protected resource
curl http://localhost:8000/api/attendees/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## 🗄️ Database Schema

### Core Models

#### Admin
```python
- username (CharField, unique)
- password (CharField, hashed)
- email (EmailField, unique)
- created_at (DateTimeField)
```

#### ClassSession
```python
- title (CharField)
- teacher (CharField)
- start_time (DateTimeField)
- end_time (DateTimeField)
- session_code (CharField, unique, auto-generated)
```

#### Attendee
```python
- name (CharField)
- phone (CharField, 10 digits)
- email (EmailField)
- age (PositiveIntegerField, optional)
- place (CharField, optional)
- class_session (ForeignKey → ClassSession)
- has_submitted (BooleanField)
- quiz_started_at (DateTimeField)
- password (CharField, hashed)
- plain_password (CharField)  # For admin viewing only
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

#### Question
```python
- text (TextField)
- question_type (CharField: 'multiple_choice' | 'text_response')
- option1-4 (CharField, nullable)
- correct_option (IntegerField, nullable)
- class_session (ForeignKey → ClassSession)
```

#### Response
```python
- attendee (ForeignKey → Attendee)
- question (ForeignKey → Question)
- selected_option (IntegerField, nullable)
- text_response (TextField, nullable)

# Property
- is_correct → boolean (for multiple choice)
```

#### QuizProgress
```python
- attendee (ForeignKey → Attendee)
- class_session (ForeignKey → ClassSession)
- last_answered_at (DateTimeField)
- is_fully_completed (BooleanField)

# Methods
- get_answered_question_ids() → list
- get_unanswered_questions() → QuerySet
- get_progress_stats() → dict
- update_completion_status() → bool
```

#### SessionAttendance
```python
- attendee (ForeignKey → Attendee)
- class_session (ForeignKey → ClassSession)
- joined_at (DateTimeField)
- has_submitted (BooleanField)
```

#### Review
```python
- attendee (ForeignKey → Attendee)
- content (TextField)
- submitted_at (DateTimeField)
- feedback_type (CharField: 'quiz' | 'review')
```

#### HitCounter
```python
- ip_address (GenericIPAddressField)
- user_agent (TextField)
- path (CharField)
- method (CharField)
- timestamp (DateTimeField)
- session_key (CharField)
- user (ForeignKey → User, nullable)

# Class Methods
- get_total_hits() → int
- get_unique_visitors() → int
- get_hits_today() → int
- get_popular_pages(limit) → QuerySet
```

### Relationships

```
ClassSession (1) ───< (N) Attendee
ClassSession (1) ───< (N) Question
ClassSession (1) ───< (N) QuizProgress
ClassSession (1) ───< (N) SessionAttendance

Attendee (1) ───< (N) Response
Attendee (1) ───< (N) Review
Attendee (1) ───< (N) QuizProgress
Attendee (1) ───< (N) SessionAttendance

Question (1) ───< (N) Response
```

---

## ⚙️ Configuration

### Settings Overview

Located in `questionnaire_project/settings.py`

#### Timezone
```python
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
```

#### Email Configuration
```python
# Default: File backend
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'sent_emails'

# SMTP (via environment variables)
SMTP_HOST = os.environ.get('SMTP_HOST')  # smtp.gmail.com
EMAIL_PORT = int(os.environ.get('SMTP_PORT', 587))
EMAIL_USE_TLS = True
```

#### REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'PAGE_SIZE': 20,
}
```

#### JWT Settings
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}
```

#### CORS
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
]
CORS_ALLOW_CREDENTIALS = True
```

### Environment Variables

Create `.env` file (optional):
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=True
SMTP_USE_SSL=False

SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Custom Middleware

**HitCountMiddleware** (`survey/middleware.py`)
- Tracks all page requests
- Records IP, user agent, path, timestamp
- Excludes admin and static files

---

## 🧪 Testing Guide

### Manual Testing

#### Test Student Registration Flow
1. Visit homepage
2. Click on a session
3. Click "Request Session Code"
4. Enter email → Check `sent_emails/` folder
5. Copy session code from email file
6. Enter code on verification page
7. Fill registration form
8. Verify login successful

#### Test Quiz Functionality
1. Login as student
2. Check session home countdown
3. Start quiz
4. Answer some questions
5. Close browser
6. Reopen and login
7. Verify progress saved
8. Complete remaining questions
9. Check score on dashboard

#### Test Admin Functions
1. Login to admin dashboard
2. Create new session
3. Add 5 questions (mix of types)
4. Edit a question
5. Delete a question
6. View student details
7. Test search and filters
8. Delete a review

### API Testing

**Using the API test script:**

```bash
python test_rest_api.py
```

This tests:
- Authentication (register, login, token refresh)
- Session CRUD operations
- Attendee registration
- Question creation
- Response submission
- Progress tracking

### Unit Tests

Run Django tests:
```bash
python manage.py test survey
```

### Load Testing

For production readiness:
```bash
# Install locust
pip install locust

# Create locustfile.py
# Run load test
locust -f locustfile.py
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set strong `SECRET_KEY`
- [ ] Configure production email backend
- [ ] Enable HTTPS
- [ ] Set up static files serving
- [ ] Configure CORS properly
- [ ] Set up database backups
- [ ] Enable logging
- [ ] Use environment variables

### Deploy to Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set SMTP_HOST=smtp.gmail.com
heroku config:set SMTP_USER=your@gmail.com
heroku config:set SMTP_PASSWORD=your-app-password

# Push to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create admin
heroku run python create_admin.py
```

### Deploy to Railway

1. Connect GitHub repository
2. Add environment variables in Railway dashboard
3. Railway auto-detects Django and deploys
4. Run migrations via Railway CLI

### Deploy to DigitalOcean

1. Create Droplet (Ubuntu 22.04)
2. SSH into server
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```
4. Clone repository
5. Set up virtual environment
6. Install packages
7. Configure Gunicorn
8. Set up Nginx reverse proxy
9. Configure SSL with Let's Encrypt

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: "No module named 'rest_framework'"
**Solution**: Install REST API packages
```bash
pip install -r requirements_api.txt
```

#### Issue: Session code not appearing
**Solution**: Check `sent_emails/` folder if using file backend

#### Issue: Time not showing correctly
**Solution**: Verify timezone in settings.py
```python
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
```

#### Issue: Students can't access quiz
**Solution**: 
- Check session start/end times
- Verify session code is correct
- Ensure student is logged in

#### Issue: Quiz timer not working
**Solution**:
- Check JavaScript console for errors
- Ensure `quiz_started_at` is set for attendee
- Verify time calculation in view

#### Issue: Progress not saving
**Solution**:
- Check browser console for errors
- Verify form submission
- Check database for Response records

#### Issue: Email not sending (SMTP)
**Solution**:
1. Verify Gmail App Password (not regular password)
2. Check SMTP environment variables
3. Ensure 2-Step Verification enabled on Gmail
4. Check firewall/antivirus blocking port 587

#### Issue: CORS errors in API
**Solution**: Add frontend URL to `CORS_ALLOWED_ORIGINS` in settings.py

### Debug Mode

Enable detailed errors:
```python
# settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Database Issues

Reset database:
```bash
# Backup first!
python manage.py dumpdata > backup.json

# Delete database
rm db.sqlite3

# Recreate
python manage.py migrate
python create_admin.py
```

---

## 📖 Additional Resources

### Documentation Files

The project includes comprehensive guides:

- **ADMIN_USER_GUIDE.md** - Admin dashboard guide
- **DASHBOARD_GUIDE.md** - Student dashboard guide
- **SESSION_CODE_SYSTEM_GUIDE.md** - Session code workflow
- **MULTI_SESSION_DYNAMIC_QUIZ_SYSTEM.md** - Multi-session feature
- **FLEXIBLE_QUESTION_SYSTEM.md** - Question management
- **GMAIL_SETUP_GUIDE.md** - Email configuration
- **REST_API_DOCUMENTATION.md** - API reference
- **REST_API_QUICK_START.md** - API getting started
- **TIMEZONE_FIX.md** - Timezone configuration

### Quick Reference Guides

- **QUICK_REFERENCE_ADMIN.md** - Admin quick commands
- **QUICK_REFERENCE_NEW_FEATURES.md** - Feature summary
- **QUICK_START_FLEXIBLE_QUESTIONS.md** - Question setup

### Implementation Reports

- **FINAL_IMPLEMENTATION_REPORT.md** - Complete feature list
- **NEW_WORKFLOW_IMPLEMENTATION.md** - Registration flow
- **QUIZ_TIMER_IMPLEMENTATION.md** - Timer system
- **ATTENDANCE_TRACKING_COMPLETE.md** - Attendance feature

---

## 🤝 Contributing

### How to Contribute

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature-name`
6. Create Pull Request

### Coding Standards

- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings to functions
- Write unit tests for new features
- Update documentation

### Reporting Issues

When reporting bugs, include:
- Django version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/screenshots

---

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

---

## 👨‍💻 Credits

**Developed by**: Sandra/TalipotTech
**Repository**: https://github.com/TalipotTech/PythonDjango
**Version**: 2.0
**Last Updated**: October 2025

---

## 📞 Support

For questions or support:
- Create an issue on GitHub
- Check existing documentation files
- Review troubleshooting section

---

## 🎯 Roadmap

### Upcoming Features

- [ ] Email template customization
- [ ] Export results to Excel/PDF
- [ ] Question categories/tags
- [ ] Randomized question order
- [ ] Question bank/pool
- [ ] Certificate generation
- [ ] Mobile app (React Native)
- [ ] Video explanations for questions
- [ ] Discussion forum
- [ ] Leaderboard

### Under Consideration

- Integration with LMS platforms
- AI-powered question suggestions
- Voice-based quiz mode
- Proctoring features
- Team/group quizzes

---

## 📊 Statistics

**Lines of Code**: ~5,000+
**Models**: 9
**Views**: 30+
**Templates**: 25+
**API Endpoints**: 50+
**Features**: 50+

---

**Thank you for using Ensate Workshops Quiz System!** 🎉

If you find this helpful, please star ⭐ the repository on GitHub.
