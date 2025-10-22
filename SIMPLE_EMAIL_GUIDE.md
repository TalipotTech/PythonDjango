# 📧 SIMPLE EMAIL SETUP - How to Get Your Session Code

## ✅ **EASIEST METHOD** - No Gmail Password Needed!

Your system is now configured to save emails as files in a folder. This means:
- ✅ No Gmail App Password needed
- ✅ No complicated setup
- ✅ Works immediately
- ✅ Session codes are saved in files you can open

---

## 🎯 How to Use (3 Simple Steps)

### **Step 1: Request Session Code**
1. Go to: http://127.0.0.1:8000/
2. Click **"Join Event Now"** on any quiz session
3. Enter ANY email address (example: `test@example.com`)
4. Click **"Send Code to My Email"**

---

### **Step 2: Find Your Session Code**
1. Look in your project folder: `g:\Sandra\PYTHONDJANGO\PythonDjango\`
2. You'll see a new folder called **`sent_emails`**
3. Open that folder
4. You'll see files like: `20251017-123456-12345.log`
5. **Open the newest file** with Notepad (double-click it)

---

### **Step 3: Copy the Session Code**
Inside the file, you'll see something like this:

```
Content-Type: text/plain; charset="utf-8"
Subject: Your Quiz Session Code
From: Quiz Portal <noreply@quizportal.com>
To: test@example.com

Hello User,

Your session code for "Python Quiz" is:

🔑 ABC123

Teacher: Sandra
...
```

**Copy the code** (like `ABC123`) and use it on the website!

---

## 📁 What You'll See

```
PythonDjango/
├── sent_emails/          ← NEW FOLDER (emails saved here)
│   ├── 20251017-123001.log
│   ├── 20251017-123045.log
│   └── 20251017-123112.log
├── manage.py
├── db.sqlite3
└── ...
```

Each file is one email. The newest file has your session code!

---

## ✨ Complete Workflow

```
1. Visit http://127.0.0.1:8000/
   ↓
2. Click "Join Event Now"
   ↓
3. Enter email: test@example.com
   ↓
4. Click "Send Code"
   ↓
5. Open folder: sent_emails/
   ↓
6. Open newest file with Notepad
   ↓
7. Copy session code (like ABC123)
   ↓
8. Paste code on website
   ↓
9. Click "Join Session"
   ↓
10. Register with auto-filled info
    ↓
11. Login and attend quiz! 🎉
```

---

## 🎯 Try It Now!

1. Visit: http://127.0.0.1:8000/
2. Click "Join Event Now"
3. Enter any email
4. Check the `sent_emails` folder!

---

## 💡 Advantages of This Method

✅ **No Gmail setup needed** - Works immediately  
✅ **No passwords** - No App Password required  
✅ **Easy to test** - Just open files with Notepad  
✅ **Perfect for development** - See all emails sent  
✅ **No internet needed** - Works offline  

---

## 🔄 Want Real Emails Instead?

If you want emails sent to your actual Gmail inbox later, I can help you set up Gmail SMTP. But for now, this file-based system is the **simplest and fastest** way to test!

---

## 📝 Quick Reference

**Email folder location**: `g:\Sandra\PYTHONDJANGO\PythonDjango\sent_emails\`

**How to read**: Open `.log` files with Notepad

**Session code location**: Look for the line after "Your session code for"

---

**Ready to test? Visit http://127.0.0.1:8000/ and try it!** 🚀
