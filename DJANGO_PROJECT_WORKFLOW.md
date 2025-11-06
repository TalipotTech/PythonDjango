# 🎯 Django Quiz Workshop System - Complete Workflow Documentation

**Project:** Ensate Workshops Quiz System  
**Framework:** Django + Django REST Framework  
**Last Updated:** October 31, 2025

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [User Roles & Access](#user-roles--access)
3. [Complete User Workflows](#complete-user-workflows)
4. [Admin Workflows](#admin-workflows)
5. [Database Models](#database-models)
6. [URL Routes](#url-routes)
7. [Features & Capabilities](#features--capabilities)
8. [Email Integration](#email-integration)
9. [API Endpoints](#api-endpoints)
10. [Security Features](#security-features)

---

## 🌐 System Overview

### Purpose
A comprehensive workshop management system that allows:
- **Admins** to create sessions, manage questions, track attendance
- **Students/Attendees** to register, take quizzes, submit feedback
- **Public Users** to view active sessions and register

### Tech Stack
- **Backend:** Django 4.x
- **Database:** SQLite (default) - can be switched to PostgreSQL/MySQL
- **Authentication:** Django Sessions + JWT for API
- **Email:** SMTP (Gmail/custom) for notifications
- **API:** Django REST Framework with Swagger documentation
- **Frontend:** Django Templates (HTML/CSS/JavaScript)

### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      Django Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   Templates  │      │    Views     │      │   Models  │ │
│  │  (Frontend)  │◄────►│   (Logic)    │◄────►│    (DB)   │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│         │                      │                     │       │
│         │                      │                     │       │
│         ▼                      ▼                     ▼       │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   Static     │      │  Middleware  │      │    API    │ │
│  │  (CSS/JS)    │      │  (Security)  │      │   (REST)  │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 👥 User Roles & Access

### 1. **Public User (No Authentication)**
**Can Access:**
- ✅ Homepage with session listings
- ✅ View active/upcoming sessions
- ✅ Register for sessions
- ✅ Submit feedback/reviews
- ✅ REST API (limited endpoints)

**Cannot Access:**
- ❌ Admin dashboard
- ❌ Student dashboard
- ❌ Quiz interface (requires registration)

---

### 2. **Student/Attendee (Session-based Authentication)**
**Can Access:**
- ✅ Student login (email/password)
- ✅ Student dashboard (view registered sessions)
- ✅ Take quizzes for registered sessions
- ✅ Submit responses
- ✅ View quiz progress
- ✅ Submit feedback

**Authentication:**
- Auto-generated password during registration
- Stored in `Attendee.plain_password` for admin viewing
- Hashed in `Attendee.password` for authentication

---

### 3. **Admin (Full Access)**
**Can Access:**
- ✅ Admin dashboard with analytics
- ✅ Create/Edit/Delete sessions
- ✅ Add/Edit/Delete questions
- ✅ View all attendees and responses
- ✅ View feedback/reviews
- ✅ Track attendance and progress
- ✅ Export data
- ✅ Full REST API access

**Authentication:**
- Custom admin login (not Django admin)
- Stored in `Admin` model
- Password hashing with Django's built-in system

---

## 🔄 Complete User Workflows

### Workflow 1: **Public User Discovers & Registers for Session**

```
┌─────────────────────────────────────────────────────────────┐
│                   1. Visit Homepage                          │
│                   URL: /                                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         2. Browse Active/Upcoming Sessions                   │
│         - See session title, teacher, countdown             │
│         - See attendee count                                 │
│         - Each session shows "Join Session" button          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         3. Click "Join Session"                              │
│         Redirects to: /session/<id>/request-code/           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         4. Enter Email to Receive Session Code              │
│         - Email sent via SMTP                                │
│         - Session code stored in email session               │
│         - Redirects to: /session/<id>/verify-code/          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         5. Enter Session Code                                │
│         - Validates code against ClassSession.session_code   │
│         - Checks if session is active (within time range)    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ├───── Valid Code ────►┌──────────────────────────┐
                         │                       │ Check if email exists    │
                         │                       │ in database              │
                         │                       └────────┬─────────────────┘
                         │                                │
                         │                    ┌───────────┴────────────┐
                         │                    │                        │
                         │              Email Exists            Email New
                         │                    │                        │
                         │                    ▼                        ▼
                         │         ┌──────────────────┐    ┌──────────────────┐
                         │         │  Existing User   │    │   New User       │
                         │         │  Login Page      │    │   Registration   │
                         │         │  /new/login/     │    │   /new/register/ │
                         │         └────────┬─────────┘    └────────┬─────────┘
                         │                  │                        │
                         │                  │   Enter Password       │  Fill Form:
                         │                  │   (from previous       │  - Name
                         │                  │    registration)       │  - Email (prefilled)
                         │                  │                        │  - Phone
                         │                  └────────┬───────────────┘
                         │                           │
                         │                           ▼
                         │               ┌────────────────────────┐
                         │               │ Auto-generate Password │
                         │               │ Send welcome email     │
                         │               │ Create Attendee record │
                         │               └────────┬───────────────┘
                         │                        │
                         ▼                        ▼
┌─────────────────────────────────────────────────────────────┐
│         6. Redirect to Session Confirmation                  │
│         URL: /session/<id>/confirm/                         │
│         Shows: Session details, quiz info, start button      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         7. Click "Start Quiz"                                │
│         Redirects to: /quiz/                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         8. Take Quiz (Question by Question)                  │
│         - Show question with options/text input              │
│         - Track progress in QuizProgress model               │
│         - 15-minute timer per attempt                        │
│         - Submit each answer to /submit/                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         9. Submit Final Answer                               │
│         - Mark as completed in Attendee.has_submitted        │
│         - Update QuizProgress.is_fully_completed             │
│         - Redirect to: /thank-you/                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         10. Thank You Page                                   │
│         - Show completion message                            │
│         - Option to submit feedback: /submit-review/         │
└─────────────────────────────────────────────────────────────┘
```

---

### Workflow 2: **Alternative Registration Flow (Direct Entry)**

```
┌─────────────────────────────────────────────────────────────┐
│         1. Visit Homepage                                    │
│         Click "Join with Code" button                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         2. Enter Session Code Directly                       │
│         URL: /join/                                         │
│         - User already has session code                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         3. Identify User (Email Entry)                       │
│         URL: /identify/                                     │
│         - Enter email                                        │
│         - Check if user exists                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                ┌────────┴────────┐
                │                 │
          User Exists       User New
                │                 │
                ▼                 ▼
    ┌──────────────────┐  ┌──────────────────┐
    │ Login Page       │  │ Registration     │
    │ /participant/    │  │ /participant/    │
    │ login/           │  │ register/        │
    └────────┬─────────┘  └────────┬─────────┘
             │                      │
             └──────────┬───────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         4. Continue to Quiz                                  │
│         (Same as Workflow 1, step 7-10)                     │
└─────────────────────────────────────────────────────────────┘
```

---

### Workflow 3: **Student Login & Dashboard**

```
┌─────────────────────────────────────────────────────────────┐
│         1. Student Login                                     │
│         URL: /student-login/                                │
│         - Enter email & password                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         2. Student Dashboard                                 │
│         URL: /student-dashboard/                            │
│         Shows:                                               │
│         - All registered sessions                            │
│         - Quiz completion status                             │
│         - Progress for each session                          │
│         - "Continue Quiz" or "View Results" buttons          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         3. Session Home (for specific session)               │
│         URL: /session-home/                                 │
│         - View session details                               │
│         - See quiz progress                                  │
│         - Start/Continue quiz button                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         4. Take/Continue Quiz                                │
│         (Same as Workflow 1, step 8-10)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Admin Workflows

### Workflow 4: **Admin Session Management**

```
┌─────────────────────────────────────────────────────────────┐
│         1. Admin Login                                       │
│         URL: /admin-login/                                  │
│         - Enter admin username & password                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         2. Admin Dashboard                                   │
│         URL: /admin-dashboard/                              │
│         Shows:                                               │
│         - Total sessions (active/upcoming/past)              │
│         - Total attendees                                    │
│         - Total questions & responses                        │
│         - Recent feedback                                    │
│         - Analytics & statistics                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         3. Session Management Options                        │
│         ┌──────────────────────────────────────────────┐    │
│         │ A. Create New Session                         │    │
│         │    URL: /manage/session/create/               │    │
│         │    - Enter title, teacher, start/end times    │    │
│         │    - Auto-generates session code              │    │
│         └──────────────────────────────────────────────┘    │
│         ┌──────────────────────────────────────────────┐    │
│         │ B. View Session Details                       │    │
│         │    URL: /manage/session/<id>/view/            │    │
│         │    - See all attendees                        │    │
│         │    - See all questions                        │    │
│         │    - See responses & statistics               │    │
│         │    - Download attendee list                   │    │
│         └──────────────────────────────────────────────┘    │
│         ┌──────────────────────────────────────────────┐    │
│         │ C. Edit Session                               │    │
│         │    URL: /manage/session/<id>/edit/            │    │
│         │    - Update session details                   │    │
│         └──────────────────────────────────────────────┘    │
│         ┌──────────────────────────────────────────────┐    │
│         │ D. Delete Session                             │    │
│         │    URL: /manage/session/<id>/delete/          │    │
│         │    - Cascades delete to attendees, responses  │    │
│         └──────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

### Workflow 5: **Admin Question Management**

```
┌─────────────────────────────────────────────────────────────┐
│         1. Add Questions to Session                          │
│         URL: /manage/session/<id>/question/add/             │
│         ┌──────────────────────────────────────────────┐    │
│         │ Question Type: Multiple Choice                │    │
│         │ - Enter question text                         │    │
│         │ - Enter 4 options                             │    │
│         │ - Select correct option (1-4)                 │    │
│         └──────────────────────────────────────────────┘    │
│         ┌──────────────────────────────────────────────┐    │
│         │ Question Type: Text Response                  │    │
│         │ - Enter question text                         │    │
│         │ - No options needed                           │    │
│         └──────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         2. Edit Question                                     │
│         URL: /manage/question/<id>/edit/                    │
│         - Modify question text, options, correct answer      │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         3. Delete Question                                   │
│         URL: /manage/question/<id>/delete/                  │
│         - Removes question and all related responses         │
└─────────────────────────────────────────────────────────────┘
```

---

### Workflow 6: **Admin Attendee Management**

```
┌─────────────────────────────────────────────────────────────┐
│         1. View Attendee Details                             │
│         URL: /manage/attendee/<id>/view/                    │
│         Shows:                                               │
│         - Personal info (name, email, phone, age, place)     │
│         - Registered sessions                                │
│         - Quiz responses with correctness                    │
│         - Progress statistics                                │
│         - Plain password (for support)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         2. Edit Attendee                                     │
│         URL: /manage/attendee/<id>/edit/                    │
│         - Update attendee information                        │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         3. Delete Attendee                                   │
│         URL: /manage/attendee/<id>/delete/                  │
│         - Removes attendee and all responses                 │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         4. Bulk Delete Attendees                             │
│         URL: /manage/attendees/bulk-delete/                 │
│         - Select multiple attendees                          │
│         - Delete in one operation                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 Database Models

### **1. Admin**
```python
Fields:
- id (Primary Key)
- username (unique)
- password (hashed)
- email (unique)
- created_at

Purpose: Store admin credentials for dashboard access
```

---

### **2. ClassSession**
```python
Fields:
- id (Primary Key)
- title
- teacher
- start_time (DateTime)
- end_time (DateTime)
- session_code (8-char unique code, auto-generated)

Purpose: Represent workshop/quiz sessions
Relationships:
- Has many Attendees (ForeignKey)
- Has many Questions (ForeignKey)
```

---

### **3. Attendee**
```python
Fields:
- id (Primary Key)
- name
- phone (10 digits)
- email
- age (optional)
- place (optional)
- class_session (ForeignKey to ClassSession)
- has_submitted (Boolean)
- quiz_started_at (DateTime, nullable)
- password (hashed, for login)
- plain_password (plaintext, for admin viewing - WARNING: security risk)
- created_at
- updated_at

Purpose: Store participant/student information
Relationships:
- Belongs to ClassSession
- Has many Responses
- Has many QuizProgress records
- Has many SessionAttendance records
- Has many Reviews
```

---

### **4. Question**
```python
Fields:
- id (Primary Key)
- text (question text)
- question_type ('multiple_choice' or 'text_response')
- option1 (for multiple choice)
- option2 (for multiple choice)
- option3 (for multiple choice)
- option4 (for multiple choice)
- correct_option (1-4, for multiple choice)
- class_session (ForeignKey to ClassSession)

Purpose: Store quiz questions
Relationships:
- Belongs to ClassSession
- Has many Responses
```

---

### **5. Response**
```python
Fields:
- id (Primary Key)
- attendee (ForeignKey to Attendee)
- question (ForeignKey to Question)
- selected_option (1-4, for multiple choice)
- text_response (for text questions)

Computed Property:
- is_correct (compares selected_option with question.correct_option)

Purpose: Store quiz answers
Relationships:
- Belongs to Attendee
- Belongs to Question
```

---

### **6. QuizProgress**
```python
Fields:
- id (Primary Key)
- attendee (ForeignKey to Attendee)
- class_session (ForeignKey to ClassSession)
- last_answered_at (auto-updated)
- is_fully_completed (Boolean)

Unique Together: (attendee, class_session)

Methods:
- get_answered_question_ids()
- get_unanswered_questions()
- get_progress_stats()
- update_completion_status()

Purpose: Track which questions student has answered
```

---

### **7. SessionAttendance**
```python
Fields:
- id (Primary Key)
- attendee (ForeignKey to Attendee)
- class_session (ForeignKey to ClassSession)
- joined_at (auto-added)
- has_submitted (Boolean)

Unique Together: (attendee, class_session)

Purpose: Track session attendance history (multi-session support)
Relationships:
- Belongs to Attendee
- Belongs to ClassSession
```

---

### **8. Review**
```python
Fields:
- id (Primary Key)
- attendee (ForeignKey to Attendee)
- content (TextField)
- submitted_at (auto-added)
- feedback_type ('quiz' or 'review')

Purpose: Store feedback and reviews from attendees
Relationships:
- Belongs to Attendee
```

---

### **9. HitCounter**
```python
Fields:
- id (Primary Key)
- ip_address (GenericIPAddressField)
- user_agent
- path (URL path)
- method (GET, POST, etc.)
- timestamp (auto-added)
- session_key
- user (ForeignKey to User, nullable)

Methods:
- get_total_hits()
- get_unique_visitors()
- get_hits_today()
- get_popular_pages()

Purpose: Track website analytics and page visits
```

---

## 🛣️ URL Routes

### **Public Routes (No Authentication)**
| URL Pattern | View | Purpose |
|-------------|------|---------|
| `/` | `home` | Homepage with session listings |
| `/join/` | `session_code_entry` | Enter session code directly |
| `/identify/` | `participant_identify` | Identify existing vs new user |
| `/participant/register/` | `participant_register` | Register new attendee |
| `/participant/login/` | `participant_login` | Login existing attendee |
| `/session/<id>/request-code/` | `request_session_code` | Request session code via email |
| `/session/<id>/verify-code/` | `verify_session_code` | Verify entered code |
| `/session/<id>/confirm/` | `session_confirm` | Session confirmation page |
| `/new/register/` | `new_participant_register` | New workflow registration |
| `/new/login/` | `new_participant_login` | New workflow login |

---

### **Student Routes (Session Authentication Required)**
| URL Pattern | View | Purpose |
|-------------|------|---------|
| `/student-login/` | `student_login` | Student login page |
| `/student-logout/` | `student_logout` | Student logout |
| `/student-dashboard/` | `student_dashboard` | Student dashboard |
| `/session-home/` | `session_home` | Specific session home |
| `/quiz/` | `quiz_view` | Quiz interface |
| `/submit/` | `submit_response` | Submit quiz answer |
| `/thank-you/` | `thank_you_view` | Thank you page |
| `/already-submitted/` | `already_submitted` | Already submitted warning |
| `/submit-review/` | `submit_review` | Submit feedback |

---

### **Admin Routes (Admin Authentication Required)**
| URL Pattern | View | Purpose |
|-------------|------|---------|
| `/admin-login/` | `admin_login` | Admin login |
| `/admin-logout/` | `admin_logout` | Admin logout |
| `/admin-dashboard/` | `admin_dashboard` | Admin dashboard |
| `/manage/session/create/` | `admin_session_create` | Create session |
| `/manage/session/<id>/view/` | `admin_session_view` | View session details |
| `/manage/session/<id>/edit/` | `admin_session_edit` | Edit session |
| `/manage/session/<id>/delete/` | `admin_session_delete` | Delete session |
| `/manage/session/<id>/question/add/` | `admin_question_add` | Add question |
| `/manage/question/<id>/edit/` | `admin_question_edit` | Edit question |
| `/manage/question/<id>/delete/` | `admin_question_delete` | Delete question |
| `/manage/attendee/<id>/view/` | `admin_attendee_view` | View attendee |
| `/manage/attendee/<id>/edit/` | `admin_attendee_edit` | Edit attendee |
| `/manage/attendee/<id>/delete/` | `admin_attendee_delete` | Delete attendee |
| `/manage/review/<id>/delete/` | `admin_review_delete` | Delete review |
| `/manage/attendees/bulk-delete/` | `admin_bulk_delete_attendees` | Bulk delete |
| `/manage/reviews/bulk-delete/` | `admin_bulk_delete_reviews` | Bulk delete reviews |

---

### **API Routes (REST API)**
| URL Pattern | Method | Auth | Purpose |
|-------------|--------|------|---------|
| `/api/` | GET | ❌ | API overview |
| `/api/swagger/` | GET | ❌ | Swagger UI |
| `/api/redoc/` | GET | ❌ | ReDoc documentation |
| `/api/auth/register/` | POST | ❌ | User registration |
| `/api/auth/token/` | POST | ❌ | Get JWT token |
| `/api/auth/token/refresh/` | POST | ❌ | Refresh JWT |
| `/api/auth/profile/` | GET/PUT | ✅ | User profile |
| `/api/sessions/` | GET/POST | ❌/✅ | List/create sessions |
| `/api/sessions/<id>/` | GET/PUT/DELETE | ❌/✅ | Session CRUD |
| `/api/sessions/active_sessions/` | GET | ❌ | Active sessions |
| `/api/sessions/verify_code/` | POST | ❌ | Verify session code |
| `/api/attendees/` | GET/POST | ✅/❌ | List/register attendees |
| `/api/attendees/<id>/` | GET/PUT/DELETE | ✅ | Attendee CRUD |
| `/api/questions/` | GET/POST | ✅ | List/create questions |
| `/api/responses/` | GET/POST | ✅ | List/submit responses |
| `/api/reviews/` | GET/POST | ✅/❌ | List/submit reviews |
| `/api/progress/` | GET | ✅ | Quiz progress |
| `/api/attendance/` | GET | ✅ | Session attendance |
| `/api/stats/dashboard/` | GET | ✅ Admin | Dashboard stats |

---

## ✨ Features & Capabilities

### **1. Multi-Session Support**
- Attendees can register for multiple sessions
- Each session has unique questions
- Progress tracked separately per session
- SessionAttendance model tracks all sessions attended

---

### **2. Flexible Question System**
- **Multiple Choice Questions:**
  - 4 options (option1, option2, option3, option4)
  - Correct answer tracked (1-4)
  - Automatic grading (is_correct property)

- **Text Response Questions:**
  - Open-ended answers
  - No correct/incorrect (for feedback/essays)
  - Stored in text_response field

---

### **3. Quiz Timer & Progress Tracking**
- **15-minute timer** per quiz attempt
- Timer starts when quiz begins (quiz_started_at)
- QuizProgress tracks:
  - Questions answered
  - Questions remaining
  - Completion percentage
  - Last answered time

---

### **4. Smart Registration Flow**
Two registration workflows:
- **Workflow A:** Email → Session Code → Register/Login
- **Workflow B:** Session Code → Email → Register/Login

Auto-detects existing users and routes accordingly.

---

### **5. Auto-fill Feature**
JavaScript (`autofill.js`) auto-fills registration forms:
- Detects email/phone entry
- Checks database via `/api/check-participant/`
- Pre-fills: name, age, place if user exists
- Visual feedback (green highlight)

---

### **6. Email Notifications**
SMTP integration for:
- Session code delivery
- Welcome emails with auto-generated password
- Registration confirmations
- Custom email templates

---

### **7. Admin Analytics Dashboard**
Real-time statistics:
- Total sessions (active/upcoming/past)
- Total attendees
- Total questions & responses
- Total reviews
- Unique visitors (via HitCounter)
- Recent activity feed
- Popular pages

---

### **8. Security Features**
- **Password Hashing:** Django's `make_password()` / `check_password()`
- **CSRF Protection:** Django middleware
- **Session Management:** Secure session handling
- **JWT Authentication:** For API access
- **Admin Authorization:** `@user_passes_test` decorators
- **SQL Injection Protection:** Django ORM

⚠️ **Security Warning:** `plain_password` field stores unencrypted passwords for admin viewing - should be removed in production.

---

### **9. Hit Counter & Analytics**
Middleware tracks:
- Every page visit
- IP addresses
- User agents (browser/device)
- URL paths
- Timestamps
- Unique visitors

Statistics available:
- Total hits
- Hits today
- Popular pages
- Unique visitor count

---

### **10. REST API with Swagger**
Full REST API for external integrations:
- Swagger UI documentation (`/api/swagger/`)
- ReDoc alternative (`/api/redoc/`)
- JWT authentication
- Filtering, searching, pagination
- Comprehensive serializers

---

## 📧 Email Integration

### **SMTP Configuration**
Located in: `questionnaire_project/settings.py`

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### **Email Functions**
1. **`send_session_code_smtp()`** - Send session code to user
2. **`send_welcome_email_smtp()`** - Send welcome email with password
3. **Fallback to `email_utils.py`** if SMTP fails

### **Email Templates**
- Session code with session details
- Welcome email with login credentials
- Custom HTML templates supported

---

## 🔐 Security Features

### **1. Authentication Methods**
- **Admin:** Custom login with `Admin` model
- **Student:** Email + auto-generated password
- **API:** JWT Bearer token

### **2. Authorization Decorators**
```python
@user_passes_test(lambda u: u.is_authenticated and u.is_staff)
def admin_view(request):
    # Admin only
    
@login_required
def student_view(request):
    # Authenticated users only
```

### **3. Session Security**
- Session-based authentication for web
- JWT for API (15-min access, 7-day refresh)
- CSRF tokens on all forms
- Secure cookie settings

### **4. Input Validation**
- Form validation (Django Forms)
- Model validators (RegexValidator for phone)
- Serializer validation (DRF)
- XSS protection (Django templates auto-escape)

---

## 🎯 Key Features Summary

| Feature | Status | Notes |
|---------|--------|-------|
| Session Management | ✅ | Create, edit, delete sessions |
| Auto Session Codes | ✅ | 8-character unique codes |
| Multi-Session Support | ✅ | Attendees can join multiple sessions |
| Flexible Questions | ✅ | Multiple choice + text response |
| Quiz Timer | ✅ | 15-minute limit per attempt |
| Progress Tracking | ✅ | Track answered/unanswered questions |
| Auto-fill Forms | ✅ | JavaScript-based autofill |
| Email Integration | ✅ | SMTP for notifications |
| Admin Dashboard | ✅ | Analytics and management |
| Student Dashboard | ✅ | View sessions and progress |
| Feedback System | ✅ | Reviews and quiz feedback |
| REST API | ✅ | Full CRUD with Swagger docs |
| Hit Counter | ✅ | Analytics and visitor tracking |
| Bulk Operations | ✅ | Bulk delete for attendees/reviews |
| Responsive Design | ✅ | Mobile-friendly templates |

---

## 📊 Data Flow Example

### **Complete Quiz Submission Flow:**

```
1. Student logs in → Session stored in Django session
2. Selects session → Redirected to /session-home/
3. Clicks "Start Quiz" → quiz_started_at timestamp saved
4. First question displayed → Loaded from Question model
5. Submits answer → POST to /submit/
   ↓
6. Backend validates answer:
   - Creates Response record
   - Updates QuizProgress
   - Checks if all questions answered
   ↓
7. If more questions → Show next question
8. If last question → Mark has_submitted = True
9. Redirect to /thank-you/
10. Option to submit review → Creates Review record
```

---

## 🚀 Quick Start Commands

### **Run Django Server:**
```bash
python manage.py runserver
```

### **Access Points:**
- Homepage: http://127.0.0.1:8000/
- Admin Login: http://127.0.0.1:8000/admin-login/
- Student Login: http://127.0.0.1:8000/student-login/
- API Swagger: http://127.0.0.1:8000/api/swagger/
- Django Admin: http://127.0.0.1:8000/admin/

### **Create Admin User (via script):**
```bash
python create_admin.py
```

### **Test Email Configuration:**
```bash
python test_email_config.py
```

---

## 📝 Summary

This Django Quiz Workshop System provides a comprehensive solution for managing online workshops with:

✅ **Public-facing registration** with smart user detection  
✅ **Secure authentication** for students and admins  
✅ **Flexible quiz system** with multiple question types  
✅ **Progress tracking** and multi-session support  
✅ **Admin dashboard** with full CRUD operations  
✅ **REST API** for external integrations  
✅ **Email notifications** via SMTP  
✅ **Analytics** with hit counter and statistics  

**Perfect for:** Educational workshops, training sessions, online courses, feedback collection, and assessment management.

---

**Documentation Version:** 1.0  
**Last Updated:** October 31, 2025  
**Django Version:** 4.x  
**Python Version:** 3.8+
