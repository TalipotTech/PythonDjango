# 🚀 Email Integration & Auto-Fill Implementation Guide

## ✅ What's Been Implemented

### 1. **Auto-Generate Session Codes** ✓
- Session codes are automatically generated when creating a new session
- 8-character alphanumeric codes (e.g., `A5K9M2X7`)
- Unique validation ensures no duplicates
- Located in `models.py` → `ClassSession.generate_session_code()`

### 2. **Password Encryption** ✓
- All passwords are hashed using Django's `make_password()` (PBKDF2 by default)
- Passwords are **never stored in plain text**
- Admin **cannot see** raw passwords (they're encrypted in database)
- Password verification uses `check_password()` for security

### 3. **Unique Email & Phone** ✓
- Email and phone numbers are now unique fields
- Prevents duplicate registrations
- Enables auto-fill functionality
- Database indexes added for fast lookups

### 4. **Email Utility Functions** ✓
Created `survey/email_utils.py` with:
- `send_session_code_email()` - Sends session code to participants
- `send_welcome_email()` - Sends welcome email to new users
- Beautiful HTML email templates
- Fallback plain text versions

### 5. **Auto-Fill API Endpoint** ✓
Created `survey/api_views.py` with:
- `/api/check-participant/` endpoint
- Checks if email/phone exists in database
- Returns participant details for auto-fill
- AJAX-compatible JSON responses

---

## 📋 What Needs To Be Done Next

### Step 1: Run Database Migrations

The models have been updated with unique constraints. You need to migrate:

```powershell
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

**⚠️ Important:** If you have existing data with duplicate emails/phones, the migration will fail. You'll need to:

**Option A: Fresh Start (Recommended for Development)**
```powershell
# Delete database
del db.sqlite3

# Remove migrations
del survey\migrations\0*.py

# Recreate everything
python manage.py makemigrations survey
python manage.py migrate
python create_admin.py
```

**Option B: Clean Duplicates First**
```python
# Run this in Django shell: python manage.py shell
from survey.models import Attendee
from django.db.models import Count

# Find duplicate emails
duplicates = Attendee.objects.values('email').annotate(count=Count('email')).filter(count__gt=1)
for dup in duplicates:
    attendees = Attendee.objects.filter(email=dup['email'])
    # Keep first, delete rest
    for att in attendees[1:]:
        att.delete()

# Find duplicate phones
duplicates = Attendee.objects.values('phone').annotate(count=Count('phone')).filter(count__gt=1)
for dup in duplicates:
    attendees = Attendee.objects.filter(phone=dup['phone'])
    # Keep first, delete rest
    for att in attendees[1:]:
        att.delete()
```

---

### Step 2: Configure Email Backend

#### For Development (Console - Already Configured):
Emails will print to console. No setup needed.

#### For Production (Gmail):

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Go to Google Account → Security → 2-Step Verification
   - Scroll to "App passwords"
   - Generate password for "Mail" / "Other (Custom name)"
   - Copy the 16-character password

3. **Update `settings.py`:**

```python
# Replace the console backend with:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-actual-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'  # The app password from step 2
DEFAULT_FROM_EMAIL = 'Quiz Portal <your-actual-email@gmail.com>'
```

#### For Other Email Providers:

**Outlook/Hotmail:**
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

**Yahoo:**
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

---

### Step 3: Update Registration View to Send Emails

Add this to your `participant_register` view in `views.py`:

```python
# At the top of views.py
from .email_utils import send_session_code_email, send_welcome_email

# In participant_register view, after creating attendee:
def participant_register(request):
    # ... existing code ...
    
    if request.method == 'POST':
        # ... create attendee ...
        
        attendee = Attendee.objects.create(
            # ... fields ...
        )
        
        # 🆕 Send welcome email
        send_welcome_email(attendee.email, attendee.name)
        
        # 🆕 Send session code email
        send_session_code_email(
            attendee.email,
            attendee.name,
            session.session_code,
            session.title,
            session.teacher
        )
        
        # Log them in
        request.session['attendee_id'] = attendee.id
        # ... rest of code ...
```

---

### Step 4: Add Auto-Fill JavaScript

Create a new file `survey/static/js/autofill.js`:

```javascript
// Auto-fill participant details when email or phone is entered
document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('id_email');
    const phoneInput = document.getElementById('id_phone');
    const nameInput = document.getElementById('id_name');
    const ageInput = document.getElementById('id_age');
    const placeInput = document.getElementById('id_place');
    
    function checkParticipant(field, value) {
        if (!value) return;
        
        const data = {};
        data[field] = value;
        
        fetch('/api/check-participant/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                // Auto-fill the form
                if (nameInput) nameInput.value = data.data.name;
                if (emailInput) emailInput.value = data.data.email;
                if (phoneInput) phoneInput.value = data.data.phone;
                if (ageInput && data.data.age) ageInput.value = data.data.age;
                if (placeInput && data.data.place) placeInput.value = data.data.place;
                
                // Show message
                showMessage('Welcome back! Your details have been filled automatically.', 'success');
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    // Check on blur (when user leaves field)
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            checkParticipant('email', this.value);
        });
    }
    
    if (phoneInput) {
        phoneInput.addEventListener('blur', function() {
            checkParticipant('phone', this.value);
        });
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    function showMessage(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        alertDiv.style.cssText = 'position: fixed; top: 80px; right: 20px; z-index: 9999; padding: 1rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);';
        
        if (type === 'success') {
            alertDiv.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            alertDiv.style.color = 'white';
        }
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
});
```

---

### Step 5: Include JavaScript in Template

Update `survey/templates/survey/submit.html` (or participant_register.html):

```html
{% extends 'base.html' %}
{% load static %}

{% block extra_head %}
<script src="{% static 'js/autofill.js' %}" defer></script>
{% endblock %}

{% block content %}
<!-- Your form here -->
{% endblock %}
```

---

## 🧪 Testing the Features

### Test 1: Email Sending (Console)
```powershell
# Start server
python manage.py runserver

# Register a new participant
# Check terminal - you should see email output
```

### Test 2: Auto-Fill
```
1. Register a participant with email: test@example.com
2. Logout
3. Start registration again
4. Enter email: test@example.com
5. Tab out of email field
6. Watch form auto-fill!
```

### Test 3: Password Encryption
```powershell
# Django shell
python manage.py shell

from survey.models import Attendee
att = Attendee.objects.first()
print(att.password)
# Should see: pbkdf2_sha256$600000$... (hashed, not plain text)
```

### Test 4: Session Code Auto-Generation
```
1. Login as admin
2. Create new session
3. Leave session_code blank
4. Save
5. Session code automatically generated!
```

---

## 📧 Email Templates Preview

### Session Code Email:
```
Subject: Your Session Code for Python Fundamentals

Hello John Doe! 👋

Your unique session code is:

🔑 A5K9M2X7

Keep this code safe! You'll need it to join the quiz session.
```

### Welcome Email:
```
Subject: Welcome to Quiz Portal!

Hello John Doe!

Thank you for registering with Quiz Portal. 
Your account has been created successfully!
```

---

## 🔒 Security Features

### Password Security:
- ✅ PBKDF2-SHA256 hashing (Django default)
- ✅ 600,000 iterations
- ✅ Unique salt per password
- ✅ Admin cannot decrypt passwords
- ✅ Check password with `check_password()` function

### Email Security:
- ✅ TLS encryption for Gmail SMTP
- ✅ App passwords (not real Gmail password)
- ✅ No credentials in version control
- ✅ Email validation before sending

### API Security:
- ✅ CSRF token required
- ✅ POST requests only
- ✅ JSON validation
- ✅ Rate limiting recommended (add django-ratelimit)

---

## 🐛 Troubleshooting

### Problem: Migration fails with "duplicate key value"
**Solution:** You have duplicate emails/phones. See Step 1, Option B above.

### Problem: Emails not sending
**Check:**
1. Is EMAIL_BACKEND configured correctly?
2. Are Gmail credentials correct?
3. Is 2FA enabled and App Password generated?
4. Check terminal for error messages

### Problem: Auto-fill not working
**Check:**
1. Is `/api/check-participant/` in urls.py?
2. Is JavaScript file included in template?
3. Check browser console for errors (F12)
4. Are field IDs matching (`id_email`, `id_phone`, etc.)?

### Problem: Admin can see passwords
**This should NOT happen.** If you see plain text:
- Check that `make_password()` is being called
- Check database - should see `pbkdf2_sha256$...`
- If plain text, re-save user with hashed password

---

## 📚 Additional Features You Can Add

### 1. Email Verification
```python
# Add to Attendee model
email_verified = models.BooleanField(default=False)
verification_token = models.CharField(max_length=100, blank=True)
```

### 2. Password Reset via Email
```python
def send_password_reset_email(email):
    # Generate reset token
    # Send email with reset link
    pass
```

### 3. SMS Integration (Twilio)
```python
# pip install twilio
from twilio.rest import Client

def send_sms_code(phone, code):
    client = Client(account_sid, auth_token)
    client.messages.create(
        to=phone,
        from_='+1234567890',
        body=f'Your session code: {code}'
    )
```

### 4. QR Code for Session
```python
# pip install qrcode
import qrcode

def generate_session_qr(session_code):
    qr = qrcode.make(session_code)
    qr.save(f'static/qr/{session_code}.png')
```

---

## ✅ Completion Checklist

- [ ] Run migrations (Step 1)
- [ ] Configure email backend (Step 2)
- [ ] Update registration view to send emails (Step 3)
- [ ] Add auto-fill JavaScript (Step 4)
- [ ] Include JavaScript in templates (Step 5)
- [ ] Test email sending
- [ ] Test auto-fill functionality
- [ ] Verify password encryption
- [ ] Test session code auto-generation
- [ ] Update documentation for users

---

## 🎉 Summary

You now have:
1. ✅ Auto-generated session codes
2. ✅ Email integration (ready to configure)
3. ✅ Auto-fill participant details
4. ✅ Encrypted passwords
5. ✅ Email-based participant lookup

**Next steps:** Follow the implementation steps above to activate all features!

Need help? Check the troubleshooting section or ask for assistance! 🚀
