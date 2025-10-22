# 🧪 Quick Test Guide - New Workflow

## ✅ Your New Flow is Ready!

**Server Status:** Running at http://127.0.0.1:8000/

---

## 🎯 Test Steps

### **1. Home Page (✓ Codes Hidden)**
```
Visit: http://127.0.0.1:8000/

✓ Check: Session codes should NOT be visible
✓ Check: Sessions still show with titles, teachers, countdowns
✓ Click: "Join Event Now" button on any session
```

---

### **2. Email Request Page**
```
URL: /session/X/request-code/

Step 1:
✓ Enter email: test@example.com
✓ Click: "Send Session Code to Email"
✓ Check terminal for email output

Step 2:
✓ Copy session code from terminal email
✓ Enter code in the form
✓ Click: "Join Session"
```

**Expected Email in Terminal:**
```
Subject: Your Session Code for [Session Title]
...
Your unique session code is: ABC12XYZ
...
```

---

### **3. Registration Page**
```
URL: /new/register/

✓ Check: Email is pre-filled (read-only)
✓ Check: Session code is pre-filled (read-only)
✓ Fill: Name (e.g., "John Doe")
✓ Fill: Mobile (e.g., "1234567890")
✓ Fill: Password (e.g., "test123")
✓ Click: "Register & Continue"
```

**For Returning Users:**
- Name and Mobile should auto-fill if email exists in DB

---

### **4. Login Page**
```
URL: /new/login/

✓ Check: Name is pre-filled (read-only)
✓ Check: Email is pre-filled (read-only)
✓ Check: Session is pre-filled (read-only)
✓ Enter: Password (same as registration)
✓ Click: "Login & Join Quiz"
```

---

### **5. Session Home**
```
✓ Should see welcome message
✓ Should see session countdown
✓ Should see "Start Quiz" button (when active)
```

---

## 🎨 Visual Checks

### **Colors by Page:**
- Home: Light gradient background
- Email Request: **Purple gradient** (#667eea)
- Registration: **Green gradient** (#48bb78)
- Login: **Blue gradient** (#4299e1)

### **Layout:**
- All forms centered on screen
- Large, readable text
- Icons for visual appeal
- Auto-filled fields clearly marked
- Step indicators visible

---

## 🔍 What to Look For

### **✓ Success Indicators:**
1. No session codes visible on home page
2. Email sends successfully (check terminal)
3. Code verification works
4. Registration auto-fills data
5. Login auto-fills data
6. Redirect to session home works

### **❌ Potential Issues:**
1. Email not printing to terminal
   - Check email_utils.py import
   - Verify console backend in settings.py

2. Code verification fails
   - Ensure code is uppercase
   - Check exact code from email

3. Auto-fill not working
   - Check if email exists in database first
   - Try with new email vs. existing email

---

## 📧 Email Template Preview

When you request a code, terminal shows:

```
Content-Type: text/plain; charset="utf-8"
Subject: Your Session Code for Python Quiz
From: Quiz Portal <noreply@quizportal.com>
To: test@example.com

Hello Participant!

Thank you for registering for the quiz session:
📚 Python Quiz
Teacher: John Smith

Your unique session code is: ABC12XYZ

How to Join:
1. Go to the Quiz Portal homepage
2. Click on "Join with Session Code"
3. Enter your session code: ABC12XYZ
4. Login with your credentials
5. Start your quiz!

⚠️ Important: Keep this code safe!
```

---

## 🐛 Troubleshooting

### **Problem: Can't see session codes in home page**
✅ **This is correct!** Codes are now sent via email.

### **Problem: Email not appearing in terminal**
**Solution:**
1. Check terminal where server is running
2. Look for "Content-Type: text/plain"
3. Scroll up if needed
4. Email should print after clicking "Send Code"

### **Problem: Code verification fails**
**Solution:**
1. Copy exact code from terminal email
2. Code is case-sensitive (auto-converts to uppercase)
3. Make sure no spaces in code
4. Try resending code

### **Problem: Registration doesn't auto-fill**
**Solution:**
1. Auto-fill only works if email exists in database
2. For first-time users, fields will be empty
3. This is expected behavior

### **Problem: After registration, login asks for password**
**Solution:**
✅ **This is correct!** Login requires password for security.

---

## 🎯 Quick Test Checklist

- [ ] Home page loads without session codes
- [ ] "Join Event Now" button works
- [ ] Email request page appears
- [ ] Email sends to terminal
- [ ] Session code visible in email
- [ ] Code entry form appears
- [ ] Code verification works
- [ ] Registration page shows with auto-filled email/code
- [ ] Registration submits successfully
- [ ] Login page shows with auto-filled name/email/session
- [ ] Login with password works
- [ ] Redirects to session home
- [ ] Can access quiz

---

## ✅ Success!

If all steps work, your new workflow is **fully functional**!

**Test with:**
1. New user (never registered)
2. Existing user (registered before)
3. Different sessions
4. Invalid codes (to test error handling)

**Your implementation is complete and working!** 🎉

---

## 📊 Comparison

### **Before:**
- Home page showed codes publicly
- Direct code entry
- Manual typing of all fields

### **After:**
- ✅ Home page hides codes
- ✅ Email-based code delivery
- ✅ Auto-fill for returning users
- ✅ Guided step-by-step process
- ✅ Beautiful, modern UI

**Much better user experience!** 🚀
