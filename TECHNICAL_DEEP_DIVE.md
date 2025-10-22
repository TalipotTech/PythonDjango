# 🔧 Quiz Portal - Complete Technical Explanation

## 📚 Table of Contents
1. [System Architecture](#system-architecture)
2. [Authentication & Security](#authentication--security)
3. [Session Management](#session-management)
4. [Quiz Flow Deep Dive](#quiz-flow-deep-dive)
5. [Database Schema](#database-schema)
6. [URL Routing](#url-routing)
7. [Views Logic](#views-logic)
8. [Template Rendering](#template-rendering)
9. [JavaScript Functionality](#javascript-functionality)
10. [Email System](#email-system)

---

## 1. System Architecture

### **Django Project Structure**
```
questionnaire_project/          # Main project folder
├── settings.py                 # Configuration (DB, email, timezone)
├── urls.py                     # Root URL routing
├── wsgi.py                     # Web server gateway
└── asgi.py                     # Async server gateway

survey/                         # Main application
├── models.py                   # Database models (ORM)
├── views.py                    # Business logic (controllers)
├── urls.py                     # App-specific routing
├── forms.py                    # Form validation
├── admin.py                    # Django admin config
├── email_utils.py              # Email functions
├── api_views.py                # REST API endpoints
├── templates/                  # HTML templates
│   └── survey/
│       ├── home.html
│       ├── quiz.html
│       ├── admin_dashboard.html
│       └── ... (20+ templates)
├── static/
│   ├── css/
│   │   └── style.css           # Global styles
│   └── js/
│       └── autofill.js         # Auto-fill functionality
└── migrations/                 # Database version control
    ├── 0001_initial.py
    ├── 0011_attendee_created_at...
    └── ...
```

### **Request-Response Cycle**

```
1. Browser Request
   ↓
   http://127.0.0.1:8000/quiz/
   ↓
2. Django URL Resolver (urls.py)
   ↓
   Matches pattern: path('quiz/', views.quiz_view, name='quiz')
   ↓
3. View Function (views.py)
   ↓
   - Check authentication (session)
   - Query database (models.py)
   - Process business logic
   - Prepare context data
   ↓
4. Template Rendering (quiz.html)
   ↓
   - Django template engine
   - Insert dynamic data
   - Loop through questions
   - Render HTML
   ↓
5. HTTP Response
   ↓
   Sends HTML back to browser
   ↓
6. Browser displays page
```

---

## 2. Authentication & Security

### **Password Hashing System**

#### **How Passwords Are Stored:**
```python
# When student registers or sets password:
from django.contrib.auth.hashers import make_password

plain_password = "mypassword123"
hashed = make_password(plain_password)

# Result stored in database:
# "pbkdf2_sha256$600000$randomsalt$hashvalue..."
#      ^            ^         ^           ^
#   Algorithm   Iterations  Salt    Encrypted hash
```

#### **How Login Works:**
```python
# When student logs in:
from django.contrib.auth.hashers import check_password

# User enters password
entered_password = "mypassword123"

# Get stored hash from database
stored_hash = attendee.password  # "pbkdf2_sha256$600000$..."

# Compare securely
if check_password(entered_password, stored_hash):
    # ✅ Correct password
    # Login successful
else:
    # ❌ Wrong password
    # Show error
```

#### **Why This Is Secure:**
1. **One-Way Hash**: Cannot decrypt to get original password
2. **Salt**: Random data added to prevent rainbow table attacks
3. **600,000 Iterations**: Makes brute-force attacks extremely slow
4. **PBKDF2-SHA256**: Industry-standard algorithm (used by banks)

### **Session Management**

#### **How Sessions Work:**
```python
# When student logs in successfully:
request.session['attendee_id'] = attendee.id
request.session['class_session_id'] = session.id
request.session['class_title'] = session.title

# Django automatically:
# 1. Creates unique session ID (e.g., "abc123xyz...")
# 2. Stores session data in django_session table
# 3. Sends session ID to browser as cookie

# Browser Cookie:
# sessionid=abc123xyz789...
```

#### **Session Validation in Views:**
```python
def quiz_view(request):
    # Check if student is logged in
    attendee_id = request.session.get('attendee_id')
    
    if not attendee_id:
        # Not logged in → redirect to login
        return redirect('submit_response')
    
    # Logged in → continue with quiz
    attendee = Attendee.objects.get(id=attendee_id)
    # ... rest of quiz logic
```

#### **Session Lifecycle:**
```
1. Student Logs In
   ↓
   Session Created
   sessionid cookie → Browser
   Session data → Database
   
2. Student Navigates Pages
   ↓
   Browser sends sessionid with each request
   Django loads session data
   Identifies student
   
3. Student Logs Out or Session Expires
   ↓
   request.session.flush()
   Session deleted from database
   Cookie cleared from browser
```

---

## 3. Session Management (Class Sessions)

### **Session Code Generation**

```python
# In models.py - ClassSession.generate_session_code()

import random
import string

def generate_session_code(self):
    """Generate unique 8-character alphanumeric code"""
    while True:
        # Generate random code: uppercase letters + digits
        # Example: "A3X9K2L7"
        code = ''.join(random.choices(
            string.ascii_uppercase + string.digits,  # A-Z, 0-9
            k=8  # 8 characters
        ))
        
        # Check if code already exists
        if not ClassSession.objects.filter(session_code=code).exists():
            # Unique code found!
            return code
        # If exists, loop continues and generates new code
```

**Why This Works:**
- **62^8 = 218 trillion** possible combinations (A-Z, a-z, 0-9)
- Collision chance: Almost impossible
- Auto-generated on session creation

### **Session State Detection**

```python
# In views.py - home view

from django.utils import timezone

now = timezone.localtime(timezone.now())  # Current time

for session in ClassSession.objects.all():
    if now < session.start_time:
        # Session hasn't started yet
        session.status = 'future'
        session.countdown = session.start_time - now
        
    elif session.start_time <= now <= session.end_time:
        # Session is currently active
        session.status = 'active'
        session.countdown = session.end_time - now
        
    else:  # now > session.end_time
        # Session has ended
        session.status = 'expired'
```

**Real Example:**
```
Session: "Python Quiz - John Smith"
Start: 2025-10-17 14:00:00
End:   2025-10-17 16:00:00

Current Time: 2025-10-17 13:30:00
Status: 'future' (starts in 30 minutes)

Current Time: 2025-10-17 14:30:00
Status: 'active' (1.5 hours remaining)

Current Time: 2025-10-17 16:30:00
Status: 'expired' (ended 30 minutes ago)
```

---

## 4. Quiz Flow Deep Dive

### **Complete Student Journey (Code Level)**

#### **Step 1: Home Page**
```python
# views.py - home()

def home(request):
    now = timezone.localtime(timezone.now())
    
    # Get sessions that are currently running
    current_sessions = ClassSession.objects.filter(
        start_time__lte=now,  # Started
        end_time__gte=now     # Not ended
    ).order_by('end_time')
    
    # Get sessions that will start in future
    future_sessions = ClassSession.objects.filter(
        start_time__gt=now
    ).order_by('start_time')
    
    # Calculate countdown for each
    for session in current_sessions:
        time_diff = session.end_time - now
        session.countdown_seconds = int(time_diff.total_seconds())
    
    return render(request, 'survey/home.html', {
        'current_sessions': current_sessions,
        'future_sessions': future_sessions,
    })
```

**Template Rendering:**
```html
<!-- home.html -->
{% for session in current_sessions %}
    <div class="event-card">
        <h3>{{ session.title }}</h3>
        <p>Teacher: {{ session.teacher }}</p>
        <span class="badge">{{ session.session_code }}</span>
        
        <!-- JavaScript countdown -->
        <div id="countdown-{{ session.id }}" 
             data-seconds="{{ session.countdown_seconds }}">
        </div>
        
        <a href="{% url 'session_confirm' session.id %}">
            Attend →
        </a>
    </div>
{% endfor %}
```

#### **Step 2: Session Code Entry**
```python
# views.py - session_code_entry()

def session_code_entry(request):
    if request.method == 'POST':
        # Get code from form
        session_code = request.POST.get('session_code', '').strip().upper()
        
        try:
            # Find session with this code
            session = ClassSession.objects.get(session_code=session_code)
            
            # Check if session is still valid
            now = timezone.localtime(timezone.now())
            if now > session.end_time:
                # Session expired
                messages.error(request, 'Session has ended')
                return render(request, 'survey/session_code_entry.html')
            
            # Valid code - store in session
            request.session['pending_session_id'] = session.id
            request.session['pending_session_code'] = session_code
            
            # Move to next step
            return redirect('participant_identify')
            
        except ClassSession.DoesNotExist:
            # Invalid code
            messages.error(request, 'Invalid session code')
    
    return render(request, 'survey/session_code_entry.html')
```

#### **Step 3: Participant Identification**
```python
# views.py - participant_identify()

def participant_identify(request):
    if request.method == 'POST':
        phone = request.POST.get('phone').strip()
        name = request.POST.get('name').strip()
        
        # Check if participant exists
        attendee = Attendee.objects.filter(
            phone=phone,
            name__iexact=name  # Case-insensitive match
        ).first()
        
        if attendee:
            # Existing user - go to login
            request.session['identified_attendee_id'] = attendee.id
            return redirect('participant_login')
        else:
            # New user - go to registration
            request.session['new_participant_phone'] = phone
            request.session['new_participant_name'] = name
            return redirect('participant_register')
```

**Why This Step?**
- Determines if user is new or returning
- Prevents duplicate accounts
- Routes to appropriate next page

#### **Step 4A: New User Registration**
```python
# views.py - participant_register()

def participant_register(request):
    if request.method == 'POST':
        # Get form data
        name = request.session.get('new_participant_name')
        phone = request.session.get('new_participant_phone')
        email = request.POST.get('email')
        age = request.POST.get('age')
        place = request.POST.get('place')
        password = request.POST.get('password')
        
        # Create new attendee
        from django.contrib.auth.hashers import make_password
        
        attendee = Attendee.objects.create(
            name=name,
            phone=phone,
            email=email,
            age=int(age) if age else None,
            place=place,
            password=make_password(password),  # Hash password!
            class_session=session
        )
        
        # Auto-login after registration
        request.session['attendee_id'] = attendee.id
        request.session['class_session_id'] = session.id
        
        # Optional: Send welcome email
        # from .email_utils import send_welcome_email
        # send_welcome_email(attendee.email, attendee.name)
        
        messages.success(request, f'Welcome {attendee.name}!')
        return redirect('session_home')
```

#### **Step 4B: Existing User Login**
```python
# views.py - participant_login()

def participant_login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        attendee_id = request.session.get('identified_attendee_id')
        
        attendee = Attendee.objects.get(id=attendee_id)
        
        # Verify password
        from django.contrib.auth.hashers import check_password
        
        if check_password(password, attendee.password):
            # ✅ Correct password
            
            # Update attendee's session
            attendee.class_session = session
            attendee.save()
            
            # Login
            request.session['attendee_id'] = attendee.id
            request.session['class_session_id'] = session.id
            
            return redirect('session_home')
        else:
            # ❌ Wrong password
            messages.error(request, 'Incorrect password')
```

#### **Step 5: Session Home (Waiting Room)**
```python
# views.py - session_home()

def session_home(request):
    attendee_id = request.session.get('attendee_id')
    class_session_id = request.session.get('class_session_id')
    
    attendee = Attendee.objects.get(id=attendee_id)
    session = ClassSession.objects.get(id=class_session_id)
    
    now = timezone.localtime(timezone.now())
    
    # Get or create quiz progress tracker
    quiz_progress, created = QuizProgress.objects.get_or_create(
        attendee=attendee,
        class_session=session
    )
    
    # Get progress statistics
    progress_stats = quiz_progress.get_progress_stats()
    # Returns: {
    #   'total': 10,
    #   'answered': 3,
    #   'pending': 7,
    #   'percentage': 30.0
    # }
    
    # Determine session status
    if now < session.start_time:
        status = 'waiting'
        countdown = session.start_time - now
    elif now <= session.end_time:
        status = 'active'
        countdown = session.end_time - now
    else:
        status = 'expired'
        countdown = None
    
    return render(request, 'survey/session_home.html', {
        'attendee': attendee,
        'class_session': session,
        'status': status,
        'countdown': countdown,
        'progress_stats': progress_stats,
    })
```

**Session Home Template:**
```html
<!-- session_home.html -->
<h1>{{ class_session.title }}</h1>
<p>Teacher: {{ class_session.teacher }}</p>

{% if status == 'waiting' %}
    <div class="alert alert-warning">
        ⏳ Quiz starts in: <span id="countdown"></span>
    </div>
    <button disabled>Start Quiz (Not Yet Started)</button>
    
{% elif status == 'active' %}
    <div class="alert alert-success">
        ✅ Quiz is Active! Time remaining: <span id="countdown"></span>
    </div>
    <div class="progress-stats">
        Progress: {{ progress_stats.answered }}/{{ progress_stats.total }}
        ({{ progress_stats.percentage }}%)
    </div>
    <a href="{% url 'quiz' %}" class="btn btn-primary">
        {% if progress_stats.answered > 0 %}
            Continue Quiz →
        {% else %}
            Start Quiz →
        {% endif %}
    </a>
    
{% else %}
    <div class="alert alert-danger">
        ⏰ Quiz has ended
    </div>
    <a href="{% url 'student_dashboard' %}">View Results</a>
{% endif %}
```

#### **Step 6: Taking the Quiz**
```python
# views.py - quiz_view()

def quiz_view(request):
    attendee_id = request.session.get('attendee_id')
    class_session_id = request.session.get('class_session_id')
    
    # Security checks
    if not attendee_id or not class_session_id:
        return redirect('submit_response')
    
    attendee = Attendee.objects.get(id=attendee_id)
    class_session = ClassSession.objects.get(id=class_session_id)
    
    now = timezone.localtime(timezone.now())
    
    # Time validation
    if now < class_session.start_time:
        return render(request, 'survey/expired.html', {
            'message': '⏳ Quiz Not Yet Started'
        })
    
    if now > class_session.end_time:
        return render(request, 'survey/expired.html', {
            'message': '⏰ Session Expired'
        })
    
    # Get or create progress tracker
    quiz_progress, created = QuizProgress.objects.get_or_create(
        attendee=attendee,
        class_session=class_session
    )
    
    # Get only unanswered questions
    unanswered_questions = quiz_progress.get_unanswered_questions()
    
    # Check if already completed
    if quiz_progress.is_fully_completed and not unanswered_questions.exists():
        return render(request, 'survey/already_submitted.html')
    
    # === POST REQUEST: Submit Answers ===
    if request.method == "POST":
        saved_count = 0
        
        for question in unanswered_questions:
            if question.question_type == 'text_response':
                # Handle text response
                key = f"text_question_{question.id}"
                text_answer = request.POST.get(key, '').strip()
                
                if text_answer:
                    Response.objects.create(
                        attendee=attendee,
                        question=question,
                        text_response=text_answer
                    )
                    saved_count += 1
                    
            else:
                # Handle multiple choice
                key = f"question_{question.id}"
                selected_option = request.POST.get(key)
                
                if selected_option:
                    Response.objects.create(
                        attendee=attendee,
                        question=question,
                        selected_option=int(selected_option)
                    )
                    saved_count += 1
        
        # Update progress
        quiz_progress.update_completion_status()
        
        # Check if more questions remain
        remaining = quiz_progress.get_unanswered_questions()
        
        if remaining.exists():
            messages.success(request, 
                f"Saved {saved_count} answer(s)! {remaining.count()} remaining.")
            return redirect('quiz')
        else:
            # All done!
            return render(request, 'survey/thank_you.html')
    
    # === GET REQUEST: Display Quiz ===
    
    # Record start time
    if not attendee.quiz_started_at:
        attendee.quiz_started_at = now
        attendee.save()
    
    # Calculate remaining time
    time_elapsed = (now - attendee.quiz_started_at).total_seconds()
    session_duration = (class_session.end_time - class_session.start_time).total_seconds()
    time_remaining = max(0, session_duration - time_elapsed)
    
    # Auto-submit if time ran out
    if time_remaining <= 0:
        quiz_progress.is_fully_completed = True
        quiz_progress.save()
        return render(request, 'survey/already_submitted.html', {
            'message': 'Time expired! Quiz auto-submitted.'
        })
    
    progress_stats = quiz_progress.get_progress_stats()
    
    return render(request, 'survey/quiz.html', {
        'questions': unanswered_questions,
        'attendee': attendee,
        'class_session': class_session,
        'progress_stats': progress_stats,
        'time_remaining_seconds': int(time_remaining),
    })
```

**Quiz Template:**
```html
<!-- quiz.html -->
<div class="quiz-header">
    <div class="timer" id="timer" data-seconds="{{ time_remaining_seconds }}">
        Time: <span id="time-display">--:--</span>
    </div>
    <div class="progress">
        {{ progress_stats.answered }}/{{ progress_stats.total }} answered
        ({{ progress_stats.percentage }}%)
    </div>
</div>

<form method="POST">
    {% csrf_token %}
    
    {% for question in questions %}
        <div class="question-card">
            <h3>Question {{ forloop.counter }}: {{ question.text }}</h3>
            
            {% if question.question_type == 'multiple_choice' %}
                <!-- Multiple Choice -->
                <div class="options">
                    <label>
                        <input type="radio" name="question_{{ question.id }}" value="1">
                        {{ question.option1 }}
                    </label>
                    <label>
                        <input type="radio" name="question_{{ question.id }}" value="2">
                        {{ question.option2 }}
                    </label>
                    <label>
                        <input type="radio" name="question_{{ question.id }}" value="3">
                        {{ question.option3 }}
                    </label>
                    <label>
                        <input type="radio" name="question_{{ question.id }}" value="4">
                        {{ question.option4 }}
                    </label>
                </div>
                
            {% else %}
                <!-- Text Response -->
                <textarea name="text_question_{{ question.id }}" 
                          rows="4" 
                          placeholder="Type your answer here..."></textarea>
            {% endif %}
        </div>
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">
        Submit Answers
    </button>
</form>

<script>
// Timer countdown
let seconds = {{ time_remaining_seconds }};
const timerDisplay = document.getElementById('time-display');

setInterval(() => {
    if (seconds <= 0) {
        alert('Time is up! Submitting quiz...');
        document.querySelector('form').submit();
        return;
    }
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    timerDisplay.textContent = 
        `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    
    seconds--;
}, 1000);
</script>
```

---

## 5. Database Schema

### **Model Relationships**

```
┌─────────────────┐
│     Admin       │
│─────────────────│
│ • username      │
│ • password      │
│ • email         │
└─────────────────┘

┌─────────────────┐         ┌─────────────────┐
│  ClassSession   │1      * │   Question      │
│─────────────────│◄────────┤─────────────────│
│ • title         │         │ • text          │
│ • teacher       │         │ • question_type │
│ • start_time    │         │ • option1-4     │
│ • end_time      │         │ • correct_opt   │
│ • session_code  │         └─────────────────┘
└─────────────────┘                   │
        │1                             │1
        │                              │
        │*                             │*
┌─────────────────┐         ┌─────────────────┐
│    Attendee     │1      * │    Response     │
│─────────────────│◄────────┤─────────────────│
│ • name          │         │ • selected_opt  │
│ • email         │         │ • text_response │
│ • phone         │         └─────────────────┘
│ • password      │
│ • age           │
│ • place         │
│ • created_at    │
│ • updated_at    │
└─────────────────┘
        │1
        │
        │*
┌─────────────────┐
│  QuizProgress   │
│─────────────────│
│ • attendee_id   │
│ • session_id    │
│ • is_completed  │
│ • last_updated  │
└─────────────────┘
```

### **SQL Queries (Behind the Scenes)**

#### **When you do:**
```python
attendee = Attendee.objects.get(id=5)
```

**Django generates:**
```sql
SELECT * FROM survey_attendee WHERE id = 5;
```

#### **When you do:**
```python
questions = Question.objects.filter(class_session=session).order_by('id')
```

**Django generates:**
```sql
SELECT * FROM survey_question 
WHERE class_session_id = 3 
ORDER BY id ASC;
```

#### **When you do:**
```python
Response.objects.create(
    attendee=attendee,
    question=question,
    selected_option=2
)
```

**Django generates:**
```sql
INSERT INTO survey_response (attendee_id, question_id, selected_option)
VALUES (5, 12, 2);
```

#### **Complex Query Example:**
```python
# Get all responses for a session with student names
responses = Response.objects.filter(
    question__class_session=session
).select_related('attendee', 'question')
```

**Django generates:**
```sql
SELECT 
    survey_response.*,
    survey_attendee.name,
    survey_question.text
FROM survey_response
INNER JOIN survey_attendee ON survey_response.attendee_id = survey_attendee.id
INNER JOIN survey_question ON survey_response.question_id = survey_question.id
WHERE survey_question.class_session_id = 3;
```

### **QuizProgress Model Logic**

```python
class QuizProgress(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    is_fully_completed = models.BooleanField(default=False)
    
    def get_answered_question_ids(self):
        """Return list of question IDs student has answered"""
        return list(Response.objects.filter(
            attendee=self.attendee,
            question__class_session=self.class_session
        ).values_list('question_id', flat=True))
        
        # Example return: [1, 3, 5, 8, 10]
    
    def get_unanswered_questions(self):
        """Return queryset of questions not yet answered"""
        answered_ids = self.get_answered_question_ids()
        
        return Question.objects.filter(
            class_session=self.class_session
        ).exclude(id__in=answered_ids).order_by('id')
        
        # SQL: SELECT * FROM survey_question 
        #      WHERE class_session_id = X 
        #      AND id NOT IN (1, 3, 5, 8, 10)
        #      ORDER BY id
    
    def get_progress_stats(self):
        """Calculate statistics"""
        total = Question.objects.filter(
            class_session=self.class_session
        ).count()
        
        answered = len(self.get_answered_question_ids())
        pending = total - answered
        percentage = round((answered / total * 100) if total > 0 else 0, 1)
        
        return {
            'total': total,        # 10
            'answered': answered,  # 7
            'pending': pending,    # 3
            'percentage': percentage  # 70.0
        }
    
    def update_completion_status(self):
        """Mark as complete if all questions answered"""
        stats = self.get_progress_stats()
        self.is_fully_completed = (stats['pending'] == 0 and stats['total'] > 0)
        self.save()
```

**How This Enables Dynamic Questions:**

```
Scenario: Admin adds new question during quiz

Before:
- Total questions: 10
- Student answered: 10
- is_fully_completed: True
- Status: "All done!"

Admin adds Question #11

After:
- Total questions: 11
- Student answered: 10 (for questions 1-10)
- get_unanswered_questions(): Returns Question #11
- is_fully_completed: False (automatically)
- Status: "1 new question available!"

Student can now answer Question #11
```

---

## 6. URL Routing

### **How URLs Map to Views**

```python
# questionnaire_project/urls.py (Root URLs)

from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect /admin to custom admin login
    path('admin/', RedirectView.as_view(pattern_name='admin_login')),
    
    # Django's built-in admin (moved to /django-admin/)
    path('django-admin/', admin.site.urls),
    
    # Include all survey app URLs
    path('', include('survey.urls')),
]
```

```python
# survey/urls.py (App URLs)

from django.urls import path
from . import views, api_views

urlpatterns = [
    # ===== PUBLIC PAGES =====
    path('', views.home, name='home'),
    path('session-code-entry/', views.session_code_entry, name='session_code_entry'),
    path('participant/identify/', views.participant_identify, name='participant_identify'),
    path('participant/register/', views.participant_register, name='participant_register'),
    path('participant/login/', views.participant_login, name='participant_login'),
    
    # ===== STUDENT PAGES (Login Required) =====
    path('session-home/', views.session_home, name='session_home'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-logout/', views.student_logout, name='student_logout'),
    path('submit-review/', views.submit_review, name='submit_review'),
    
    # ===== ADMIN PAGES =====
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    
    # Session Management
    path('admin/session/<int:session_id>/', views.admin_session_view, name='admin_session_view'),
    path('admin/session/create/', views.admin_session_create, name='admin_session_create'),
    path('admin/session/<int:session_id>/edit/', views.admin_session_edit, name='admin_session_edit'),
    path('admin/session/<int:session_id>/delete/', views.admin_session_delete, name='admin_session_delete'),
    
    # Question Management
    path('admin/session/<int:session_id>/add-question/', views.admin_question_add, name='admin_question_add'),
    path('admin/question/<int:question_id>/edit/', views.admin_question_edit, name='admin_question_edit'),
    path('admin/question/<int:question_id>/delete/', views.admin_question_delete, name='admin_question_delete'),
    
    # Attendee Management
    path('admin/attendee/<int:attendee_id>/', views.admin_attendee_view, name='admin_attendee_view'),
    path('admin/attendee/<int:attendee_id>/edit/', views.admin_attendee_edit, name='admin_attendee_edit'),
    path('admin/attendee/<int:attendee_id>/delete/', views.admin_attendee_delete, name='admin_attendee_delete'),
    
    # ===== API ENDPOINTS =====
    path('api/check-participant/', api_views.check_participant_exists, name='api_check_participant'),
]
```

### **URL Pattern Matching**

When browser requests: `http://127.0.0.1:8000/quiz/`

```
1. Django checks questionnaire_project/urls.py
   ↓
   path('', include('survey.urls'))  ← Matches! (empty string matches anything)
   ↓
2. Django checks survey/urls.py
   ↓
   path('quiz/', views.quiz_view, name='quiz')  ← Matches!
   ↓
3. Django calls views.quiz_view(request)
   ↓
4. View returns HttpResponse
```

### **URL Reversing (Dynamic URLs)**

```python
# In views - redirect using name
return redirect('admin_dashboard')

# Django looks up URL pattern with name='admin_dashboard'
# Generates: /admin-dashboard/

# With parameters
return redirect('admin_session_view', session_id=5)

# Django generates: /admin/session/5/
```

```html
<!-- In templates - URL tag -->
<a href="{% url 'quiz' %}">Start Quiz</a>
<!-- Generates: <a href="/quiz/">Start Quiz</a> -->

<a href="{% url 'admin_session_view' session.id %}">View Session</a>
<!-- If session.id = 5, generates: <a href="/admin/session/5/">View Session</a> -->
```

---

## 7. Views Logic

### **View Decorators (Future Enhancement)**

```python
# Custom decorator to check if student is logged in
def student_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('attendee_id'):
            messages.error(request, 'Please login first')
            return redirect('student_login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Usage:
@student_login_required
def quiz_view(request):
    # Only runs if student is logged in
    pass
```

### **Message Framework**

```python
from django.contrib import messages

# In view
messages.success(request, 'Registration successful!')
messages.error(request, 'Invalid session code')
messages.warning(request, 'Quiz will start soon')
messages.info(request, 'You have 3 questions remaining')
```

```html
<!-- In template (base.html) -->
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

**How It Works:**
1. View sets message: `messages.success(request, 'Done!')`
2. Message stored in session
3. Template displays it on next page load
4. Message automatically deleted after display

---

## 8. Template Rendering

### **Template Inheritance**

```html
<!-- base.html (Parent Template) -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Quiz Portal{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}?v=4.0">
    {% block extra_head %}{% endblock %}
</head>
<body>
    <header>
        <nav>
            <!-- Navigation -->
        </nav>
    </header>
    
    <main>
        {% block content %}
        <!-- Child templates inject content here -->
        {% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2025 Quiz Portal</p>
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

```html
<!-- quiz.html (Child Template) -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Quiz - {{ class_session.title }}{% endblock %}

{% block extra_head %}
<style>
    .quiz-timer { position: fixed; top: 10px; right: 10px; }
</style>
{% endblock %}

{% block content %}
    <h1>{{ class_session.title }}</h1>
    <!-- Quiz content here -->
{% endblock %}

{% block extra_js %}
<script>
    // Timer JavaScript
</script>
{% endblock %}
```

### **Django Template Tags**

#### **Variables:**
```html
{{ attendee.name }}           → "John Doe"
{{ class_session.title }}     → "Python Quiz"
{{ progress_stats.percentage }} → "75.0"
```

#### **Filters:**
```html
{{ attendee.name|upper }}                  → "JOHN DOE"
{{ session.start_time|date:"M d, Y" }}    → "Oct 17, 2025"
{{ question.text|truncatewords:10 }}       → "First 10 words..."
{{ score|floatformat:2 }}                  → "85.50"
```

#### **Control Structures:**
```html
{% if status == 'active' %}
    <button>Start Quiz</button>
{% elif status == 'waiting' %}
    <p>Quiz starts soon...</p>
{% else %}
    <p>Quiz has ended</p>
{% endif %}

{% for question in questions %}
    <div class="question">
        {{ forloop.counter }}. {{ question.text }}
    </div>
{% empty %}
    <p>No questions available</p>
{% endfor %}
```

#### **Special Variables:**
```html
{% for item in list %}
    {{ forloop.counter }}      → 1, 2, 3, ...
    {{ forloop.counter0 }}     → 0, 1, 2, ...
    {{ forloop.first }}        → True on first iteration
    {{ forloop.last }}         → True on last iteration
{% endfor %}
```

---

## 9. JavaScript Functionality

### **Countdown Timer**

```javascript
// In home.html
<script>
function startCountdown(elementId, totalSeconds) {
    const element = document.getElementById(elementId);
    let seconds = totalSeconds;
    
    const interval = setInterval(() => {
        if (seconds <= 0) {
            clearInterval(interval);
            element.innerHTML = '<span class="expired">Expired</span>';
            return;
        }
        
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        let display = '';
        if (days > 0) display += `${days}d `;
        if (hours > 0) display += `${hours}h `;
        display += `${minutes}m ${secs}s`;
        
        element.textContent = display;
        seconds--;
    }, 1000);
}

// Start countdown for each session
document.querySelectorAll('[data-countdown]').forEach(el => {
    const seconds = parseInt(el.dataset.countdown);
    startCountdown(el.id, seconds);
});
</script>
```

### **Auto-Fill API Call**

```javascript
// In autofill.js
let debounceTimer;

function checkParticipant(value, field) {
    clearTimeout(debounceTimer);
    
    debounceTimer = setTimeout(async () => {
        const response = await fetch('/api/check-participant/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ [field]: value })
        });
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.exists) {
                // Auto-fill form fields
                document.getElementById('name').value = data.name;
                document.getElementById('email').value = data.email;
                document.getElementById('phone').value = data.phone;
                
                // Show success notification
                showToast('✅ Details auto-filled!');
            }
        }
    }, 500); // Wait 500ms after typing stops
}

// Event listeners
document.getElementById('email').addEventListener('input', (e) => {
    checkParticipant(e.target.value, 'email');
});

document.getElementById('phone').addEventListener('input', (e) => {
    checkParticipant(e.target.value, 'phone');
});
```

### **Form Validation**

```javascript
// In base.html
<script>
// Add loading state to forms
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner"></span> Loading...';
        }
    });
});

// Confirm delete actions
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        if (!confirm('Are you sure you want to delete this?')) {
            e.preventDefault();
        }
    });
});
</script>
```

---

## 10. Email System

### **Email Configuration**

```python
# settings.py

# Development: Console backend (prints to terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production: SMTP backend (real emails)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'app-password-here'

DEFAULT_FROM_EMAIL = 'Quiz Portal <noreply@quizportal.com>'
```

### **Email Utility Functions**

```python
# email_utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_session_code_email(email, name, session_code, session_title, teacher):
    """Send session code to student"""
    
    subject = f"Your Session Code: {session_code}"
    
    # Plain text version
    text_message = f"""
    Hello {name},
    
    You have been registered for: {session_title}
    Teacher: {teacher}
    
    Your session code is: {session_code}
    
    Use this code to login and take your quiz.
    
    Best regards,
    Quiz Portal Team
    """
    
    # HTML version
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .code {{ 
                font-size: 24px; 
                font-weight: bold; 
                color: #4CAF50;
                padding: 10px;
                background: #f5f5f5;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <h2>Hello {name},</h2>
        <p>You have been registered for:</p>
        <h3>{session_title}</h3>
        <p>Teacher: {teacher}</p>
        <p>Your session code is:</p>
        <div class="code">{session_code}</div>
        <p>Use this code to login and take your quiz.</p>
        <hr>
        <p style="color: #888;">Best regards,<br>Quiz Portal Team</p>
    </body>
    </html>
    """
    
    try:
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
```

### **Calling Email Function**

```python
# In views.py - participant_register()

# After creating attendee
from .email_utils import send_session_code_email

send_session_code_email(
    email=attendee.email,
    name=attendee.name,
    session_code=session.session_code,
    session_title=session.title,
    teacher=session.teacher
)
```

### **Console Output Example**

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Your Session Code: ABC12XYZ
From: Quiz Portal <noreply@quizportal.com>
To: john@example.com
Date: Fri, 17 Oct 2025 14:30:00 -0000
Message-ID: <123456789@localhost>

Hello John Doe,

You have been registered for: Python Quiz
Teacher: John Smith

Your session code is: ABC12XYZ

Use this code to login and take your quiz.

Best regards,
Quiz Portal Team
```

---

## 11. Admin Dashboard

### **Statistics Calculation**

```python
# In admin_dashboard view

# Total counts
total_attendees = Attendee.objects.count()
# SQL: SELECT COUNT(*) FROM survey_attendee;

total_sessions = ClassSession.objects.count()
# SQL: SELECT COUNT(*) FROM survey_classsession;

total_questions = Question.objects.count()
# SQL: SELECT COUNT(*) FROM survey_question;

total_responses = Response.objects.count()
# SQL: SELECT COUNT(*) FROM survey_response;

# Session status
from django.utils import timezone
now = timezone.localtime(timezone.now())

active_sessions = ClassSession.objects.filter(
    start_time__lte=now,
    end_time__gte=now
).count()

# SQL: SELECT COUNT(*) FROM survey_classsession
#      WHERE start_time <= '2025-10-17 14:30:00'
#      AND end_time >= '2025-10-17 14:30:00';
```

### **Search Functionality**

```python
# In admin_dashboard view

from django.db.models import Q

search_query = request.GET.get('search', '').strip()

if search_query:
    # Search attendees by name, email, or phone
    attendees = Attendee.objects.filter(
        Q(name__icontains=search_query) | 
        Q(email__icontains=search_query) |
        Q(phone__icontains=search_query)
    )
    
    # SQL: SELECT * FROM survey_attendee
    #      WHERE name LIKE '%search%'
    #      OR email LIKE '%search%'
    #      OR phone LIKE '%search%';
```

---

## 12. Performance Optimizations

### **Database Indexing**

```python
# In models.py - Attendee

class Meta:
    indexes = [
        models.Index(fields=['email']),   # Fast email lookups
        models.Index(fields=['phone']),   # Fast phone lookups
    ]
```

**What This Does:**
- Creates database index on email column
- Searches by email are 10-100x faster
- Especially important for auto-fill API

### **Query Optimization**

```python
# ❌ BAD: N+1 Query Problem
responses = Response.objects.all()
for response in responses:
    print(response.attendee.name)    # Extra DB query each time!
    print(response.question.text)    # Another query!

# Total queries: 1 + 2N (N = number of responses)

# ✅ GOOD: Use select_related()
responses = Response.objects.all().select_related('attendee', 'question')
for response in responses:
    print(response.attendee.name)    # No extra query!
    print(response.question.text)    # No extra query!

# Total queries: 1 (single JOIN query)
```

---

## 13. Security Measures

### **CSRF Protection**

```html
<!-- All POST forms must include: -->
<form method="POST">
    {% csrf_token %}
    <!-- Django generates hidden input:
    <input type="hidden" name="csrfmiddlewaretoken" value="abc123...">
    -->
    <!-- Form fields -->
</form>
```

**How It Works:**
1. Django generates unique token for each user session
2. Token stored in cookie and form
3. On POST, Django compares both tokens
4. If mismatch → Request rejected (CSRF attack prevented)

### **SQL Injection Prevention**

```python
# ❌ DANGEROUS (Don't do this!)
query = f"SELECT * FROM attendee WHERE name = '{user_input}'"
# If user_input = "'; DROP TABLE attendee; --"
# SQL becomes: SELECT * FROM attendee WHERE name = ''; DROP TABLE attendee; --'

# ✅ SAFE (Django ORM automatically escapes)
Attendee.objects.filter(name=user_input)
# Django parameterizes: SELECT * FROM attendee WHERE name = ?
# Binds user_input safely
```

### **XSS Prevention**

```html
<!-- Django auto-escapes HTML in templates -->
{{ user_input }}

<!-- If user_input = "<script>alert('XSS')</script>" -->
<!-- Django renders: &lt;script&gt;alert('XSS')&lt;/script&gt; -->
<!-- Browser displays text, doesn't execute script -->

<!-- To allow HTML (careful!): -->
{{ trusted_html|safe }}
```

---

## 🎯 Summary

### **Core Technologies**
- **Django ORM**: Database abstraction (no raw SQL needed)
- **Django Templates**: Dynamic HTML generation
- **Session Framework**: User state management
- **PBKDF2-SHA256**: Password hashing
- **CSRF Middleware**: Form security
- **Timezone Support**: Accurate time management

### **Key Concepts**
1. **MVC Pattern**: Models (data), Views (logic), Templates (presentation)
2. **ORM**: Python code → SQL queries automatically
3. **Sessions**: Track logged-in users without Django User model
4. **Progress Tracking**: QuizProgress model enables dynamic questions
5. **Security**: Password hashing, CSRF tokens, input escaping
6. **Time Management**: Timezone-aware datetime calculations

### **Data Flow**
```
User Browser → Django URL Router → View Function → Database Query
                                        ↓
                                   Business Logic
                                        ↓
                                  Template Engine
                                        ↓
                                   HTML Response → Browser
```

**This is a complete, production-ready quiz management system!** 🚀

The architecture is scalable, secure, and maintainable. Each component has a specific responsibility, making it easy to extend and debug.
