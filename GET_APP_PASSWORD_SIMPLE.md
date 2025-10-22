# 🔑 How to Get Gmail App Password (Easy Steps)

## ⚠️ IMPORTANT: Without this password, emails won't be sent!

---

## 📋 Simple 5-Step Process

### **Step 1: Open This Link**
Click here: **https://myaccount.google.com/apppasswords**

Or manually go to:
1. https://myaccount.google.com/
2. Click "Security" on the left
3. Scroll down to find "App passwords"

---

### **Step 2: Sign In**
- Sign in with your Gmail: **parvathyparu0015@gmail.com**
- Use your normal Gmail password

---

### **Step 3: Check 2-Step Verification**

**If you see**: "App passwords"
- ✅ Great! Continue to Step 4

**If you see**: "2-Step Verification is off"
- ❌ You need to enable it first!
- Click "Turn on 2-Step Verification"
- Follow these steps:
  1. Enter your phone number
  2. Receive SMS code
  3. Enter the code
  4. Click "Turn On"
- Then go back to: https://myaccount.google.com/apppasswords

---

### **Step 4: Generate App Password**

On the App Passwords page:

1. **Select app**: Choose "Mail" from dropdown
2. **Select device**: Choose "Other (Custom name)"
3. Type name: **"Django Quiz Portal"**
4. Click the **"Generate"** button

You'll see a **yellow box** with a password like this:

```
┌─────────────────────────┐
│  abcd efgh ijkl mnop    │
└─────────────────────────┘
```

---

### **Step 5: Copy and Use the Password**

1. **Copy the 16 characters** (you can click the small copy icon)
2. **Remove all spaces**: `abcd efgh ijkl mnop` → `abcdefghijklmnop`
3. Open your file: `questionnaire_project/settings.py`
4. Find line 132:
   ```python
   EMAIL_HOST_PASSWORD = 'your-app-password-here'
   ```
5. Replace with your password:
   ```python
   EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'
   ```
6. **Save the file** (Ctrl+S)

---

## ✅ Done! Now Test It

1. Visit: http://127.0.0.1:8000/
2. Click "Join Event Now"
3. Enter your email: **parvathyparu0015@gmail.com**
4. Click "Send Code to My Email"
5. **Check your Gmail inbox!** 📬 (wait 10-30 seconds)

The email will have:
- Subject: "Your Quiz Session Code"
- From: "Quiz Portal"
- Contains your session code

---

## 🔍 Troubleshooting

### Problem: "I can't find App Passwords"
**Solution**: You need to enable 2-Step Verification first
- Go to: https://myaccount.google.com/security
- Turn on "2-Step Verification"
- Then App Passwords will appear

---

### Problem: "Invalid credentials" error in terminal
**Solution**: Check these things:
1. Make sure you copied the password correctly (no spaces)
2. Make sure you're using APP PASSWORD, not your regular Gmail password
3. Try generating a new App Password

---

### Problem: Email not arriving
**Solution**: 
1. Wait 1-2 minutes (sometimes Gmail is slow)
2. Check your **Spam folder**
3. Check terminal for error messages
4. Make sure you saved the settings.py file

---

## 📊 Current Settings

Your `settings.py` should look like this:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'parvathyparu0015@gmail.com'
EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'  # Your 16-char password (no spaces)
DEFAULT_FROM_EMAIL = 'Quiz Portal <parvathyparu0015@gmail.com>'
```

---

## 🎯 Visual Guide

```
You → Enter email on website
     ↓
Django → Connects to Gmail SMTP
     ↓
Gmail → Checks your App Password
     ↓
Gmail → Sends email with session code
     ↓
You → Receive email in inbox 📬
     ↓
You → Copy session code from email
     ↓
You → Enter code and continue registration
```

---

## ⏰ How Long Does This Take?

- Enable 2-Step Verification: **2 minutes**
- Generate App Password: **30 seconds**
- Update settings.py: **30 seconds**
- **Total: About 3 minutes!**

---

## 💡 Quick Links

- **Get App Password**: https://myaccount.google.com/apppasswords
- **Enable 2-Step**: https://myaccount.google.com/security
- **Gmail Help**: https://support.google.com/accounts/answer/185833

---

## 🎉 After You Add the Password

Django will automatically reload and start sending real emails!

You'll know it's working when:
- ✅ No error in terminal
- ✅ Email arrives in Gmail inbox within 30 seconds
- ✅ Email contains session code
- ✅ You can copy code and proceed

---

**Need help?** Let me know which step you're stuck on! 😊
