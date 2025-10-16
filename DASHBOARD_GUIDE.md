# 🎯 Dashboard System Guide

This Django application now has **TWO separate dashboards** - one for administrators and one for students!

---

## 🔐 Admin Dashboard

### Access URL
```
http://127.0.0.1:8000/admin-login/
```

### Default Credentials
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** admin@example.com

### Features
The admin dashboard (`/admin-dashboard/`) provides:

✅ **Statistics Overview**
- Total number of attendees
- Total class sessions
- Total questions across all sessions
- Total quiz responses submitted

✅ **Session Management**
- View all class sessions
- See teacher names and schedules
- Track number of attendees per session
- Action buttons for view/edit/delete (placeholders ready for implementation)

✅ **Attendee Monitoring**
- List of recent attendees (last 10)
- Email and phone contact information
- Session enrollment details
- Submission status (Submitted ✓ or Pending ⏳)

✅ **Review System**
- View recent student feedback
- See who submitted reviews and when
- Quick overview of student opinions

### Navigation When Logged In as Admin
- 🏠 Home
- 📊 Dashboard (Admin Dashboard)
- 🚪 Logout (Admin)

---

## 👤 Student Dashboard

### Access URL
Students login at:
```
http://127.0.0.1:8000/student-login/
```

After login, they can access their dashboard at:
```
http://127.0.0.1:8000/student-dashboard/
```

### Features
The student dashboard (`/student-dashboard/`) provides:

✅ **Personal Information**
- Name, email, phone
- Age and location (if provided)
- Enrolled class session details

✅ **Quiz Status**
- Quiz completion indicator
- Total questions available
- Number of responses submitted
- **Score calculation** (correct answers / total questions)
- Percentage score display

✅ **Detailed Results** (if quiz submitted)
- Question-by-question breakdown
- Your selected answer vs. correct answer
- Visual indicators (✓ Correct / ✗ Incorrect)
- Color-coded response cards (green = correct, red = incorrect)

✅ **Feedback Section**
- Submit feedback/review for the session
- View previously submitted feedback
- Timestamp of submission

### Navigation When Logged In as Student
- 🏠 Home
- 📚 My Dashboard (Student Dashboard)
- 📝 Quiz
- 🚪 Logout

---

## 🚀 Quick Start Guide

### For New Students (First Time):
1. Go to http://127.0.0.1:8000/submit/
2. Fill out the registration form (name, phone, email, session required)
3. Set a password (optional but recommended)
4. Submit → You'll be taken to the quiz
5. After submitting quiz, click "My Dashboard" in the navigation

### For Returning Students:
1. Go to http://127.0.0.1:8000/student-login/
2. Enter your name, password, and select your class session
3. Click Login → View your dashboard or take quiz

### For Administrators:
1. Go to http://127.0.0.1:8000/admin-login/
2. Enter username: `admin`, password: `admin123`
3. Click Login → View admin dashboard
4. Monitor all students, sessions, and responses

---

## 🔒 Security Features

✅ **Session-Based Authentication**
- Admin and student sessions are separate
- Auto-logout redirects to appropriate login pages
- Session data cleared on logout

✅ **Access Control**
- Admin dashboard requires admin login
- Student dashboard requires student login
- Unauthorized access redirects to login pages

✅ **Password Security**
- All passwords hashed using Django's `make_password()`
- Passwords never stored in plain text
- Secure password verification with `check_password()`

---

## 📊 Database Models

### New Admin Model
```python
class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Hashed
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Student Sessions Store:
- `attendee_id` - Student identifier
- `class_session_id` - Enrolled session
- `class_title` - Session name

### Admin Sessions Store:
- `admin_id` - Admin identifier
- `admin_username` - Admin username
- `is_admin` - Boolean flag (True)

---

## 🎨 UI/UX Features

### Admin Dashboard Design
- Purple gradient header with welcome message
- 4 colorful statistic cards with icons
- Modern data tables with hover effects
- Responsive grid layout (adapts to mobile)
- Review cards with left border accent
- Professional color scheme (purple, green, blue, orange)

### Student Dashboard Design
- Personal info card with organized fields
- Session details card with teacher and schedule
- Status cards (completed/pending) with different colors
- Detailed response breakdown with color coding
- Score display with percentage
- Feedback section with submission history

---

## 🛠️ Adding More Admins

To create additional admin users:

1. **Using Python script:**
```python
from django.contrib.auth.hashers import make_password
from survey.models import Admin

Admin.objects.create(
    username="newadmin",
    password=make_password("securepassword"),
    email="newadmin@example.com"
)
```

2. **Using Django shell:**
```bash
py -3 manage.py shell
```
Then paste the code above.

3. **Using Django admin panel:**
- Go to http://127.0.0.1:8000/admin/
- Login with superuser credentials
- Navigate to Survey → Admins → Add Admin

---

## 📱 Responsive Design

Both dashboards are fully responsive:
- **Desktop:** Multi-column grid layout
- **Tablet:** Adjusted spacing and smaller grids
- **Mobile:** Single-column layout, full-width cards

---

## 🔄 URL Routes

### Public Routes
- `/` - Home page
- `/submit/` - Student registration
- `/student-login/` - Student login page
- `/admin-login/` - Admin login page

### Protected Student Routes (requires student login)
- `/student-dashboard/` - Student dashboard
- `/quiz/` - Take quiz
- `/submit-review/` - Submit feedback
- `/student-logout/` - Logout

### Protected Admin Routes (requires admin login)
- `/admin-dashboard/` - Admin dashboard
- `/admin-logout/` - Admin logout

---

## 🎯 Next Steps / Enhancement Ideas

1. **Admin Features:**
   - Implement edit/delete functionality for sessions
   - Add ability to create new sessions from dashboard
   - Export attendee/response data to CSV
   - View individual student details
   - Send email notifications

2. **Student Features:**
   - Edit profile information
   - Retake quiz functionality
   - Download certificate/score report
   - Session schedule calendar view

3. **Both:**
   - Real-time notifications
   - Advanced analytics and charts
   - Search and filter capabilities
   - Password reset functionality
   - Two-factor authentication

---

## 📞 Support

For issues or questions:
- Check that migrations are applied: `py -3 manage.py migrate`
- Verify server is running: `py -3 manage.py runserver`
- Clear browser cache if styling doesn't load
- Check browser console for JavaScript errors

---

## ✅ Testing Checklist

**Admin Dashboard:**
- [ ] Can login with admin credentials
- [ ] See correct statistics
- [ ] View list of sessions
- [ ] View list of attendees
- [ ] See recent reviews
- [ ] Logout works and redirects properly

**Student Dashboard:**
- [ ] Can login with student credentials
- [ ] See personal information
- [ ] View session details
- [ ] See quiz status (pending or completed)
- [ ] View responses if quiz submitted
- [ ] See score percentage
- [ ] Submit feedback
- [ ] Logout works properly

**Navigation:**
- [ ] Correct nav links appear for admin
- [ ] Correct nav links appear for student
- [ ] Guest users see login/register options
- [ ] No unauthorized access to protected pages

---

**Enjoy your new dashboard system! 🎉**
