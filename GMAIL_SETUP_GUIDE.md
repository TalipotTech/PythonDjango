# 📧 Gmail SMTP Setup Guide

## ✅ Current Status
Your Django project is configured to send emails to: **parvathyparu0015@gmail.com**

## ⚠️ ACTION REQUIRED
You need to get a **Gmail App Password** to make email sending work!

---

## 🔐 Step 1: Get Gmail App Password (5 minutes)

### Option A: Quick Link Method
1. **Visit this link**: https://myaccount.google.com/apppasswords
2. You'll be asked to sign in to your Google account (parvathyparu0015@gmail.com)
3. If you see "App passwords", great! Click **"Select app"** → Choose **"Mail"** → **"Other"** → Type "Django Quiz"
4. Click **"Generate"**
5. You'll see a **16-character code** like: `abcd efgh ijkl mnop`
6. **Copy this code** (remove spaces)

### Option B: Manual Method
1. Go to: https://myaccount.google.com/
2. Click **"Security"** (left sidebar)
3. Enable **"2-Step Verification"** if not already enabled
4. Scroll down to find **"App passwords"**
5. Create new app password for "Mail" → "Other" → "Django Quiz"
6. Copy the 16-character code

---

## 🛠️ Step 2: Update settings.py

Open `questionnaire_project/settings.py` and find this line:

```python
EMAIL_HOST_PASSWORD = 'PASTE-YOUR-16-CHAR-APP-PASSWORD-HERE'
```

Replace with your actual app password (no spaces):

```python
EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'  # Your real 16-char code
```

**⚠️ Security Note**: Don't share this password with anyone!

---

## 🚀 Step 3: Restart Django Server

After updating the password:

1. Stop the current server (press `Ctrl+C` in terminal)
2. Start it again:
   ```powershell
   python manage.py runserver
   ```

---

## ✅ Step 4: Test Email Sending

1. Visit: http://127.0.0.1:8000/
2. Click **"Join Event Now"** on any session
3. Enter your email: **parvathyparu0015@gmail.com**
4. Click **"Send Code to My Email"**
5. **Check your Gmail inbox!** 📬
   - Subject: "Your Quiz Session Code"
   - Contains: Session code, teacher name, session title

---

## 🔍 Troubleshooting

### Problem: "SMTPAuthenticationError: Username and Password not accepted"
**Solution**: Your app password is incorrect or has spaces
- Remove all spaces from the 16-character code
- Make sure you're using **App Password**, not your regular Gmail password

### Problem: "SMTPException: STARTTLS extension not supported"
**Solution**: Check your settings:
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### Problem: Email goes to Spam folder
**Solution**: This is normal for first few emails. Mark as "Not Spam" in Gmail.

### Problem: Still no email after 2 minutes
**Solution**: 
1. Check your Gmail spam folder
2. Check Django terminal for error messages
3. Make sure 2-Step Verification is enabled on your Google account

---

## 🔄 Switch Back to Console Mode (Development Only)

If you want emails to print to terminal instead (for testing), change `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Comment this out
```

---

## 📊 What Gets Sent via Email

When a user requests a session code, they receive this email:

**Subject**: Your Quiz Session Code  
**From**: Quiz Portal <parvathyparu0015@gmail.com>  
**To**: User's email address

**Email Content**:
```
Hello [User Name],

Your session code for "[Session Title]" is:

🔑 [SESSION-CODE]

Teacher: [Teacher Name]

Please keep this code safe. You'll need it to join the quiz.

To continue:
1. Enter this code on the verification page
2. Complete your registration
3. Start the quiz!

Good luck! 🎯

---
Quiz Portal Team
```

---

## ✨ Success Indicators

You'll know it's working when:
- ✅ No error messages in Django terminal
- ✅ Email arrives in your Gmail inbox within 10-30 seconds
- ✅ Email contains the correct session code
- ✅ User can copy code and proceed to registration

---

## 📝 Quick Checklist

- [ ] 2-Step Verification enabled on Google account
- [ ] App Password generated (16 characters)
- [ ] App Password added to `settings.py` (no spaces)
- [ ] Django server restarted
- [ ] Test email sent successfully
- [ ] Email received in Gmail inbox

---

## 🎯 Current Configuration

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'parvathyparu0015@gmail.com'
EMAIL_HOST_PASSWORD = 'PASTE-YOUR-16-CHAR-APP-PASSWORD-HERE'  # ⚠️ UPDATE THIS!
DEFAULT_FROM_EMAIL = 'Quiz Portal <parvathyparu0015@gmail.com>'
```

---

## ❓ Need Help?

If you're still having issues:
1. Check the Django terminal for error messages
2. Verify your App Password is correct (16 characters, no spaces)
3. Make sure 2-Step Verification is enabled
4. Try generating a new App Password

---

**Last Updated**: Implementation complete, awaiting App Password configuration
