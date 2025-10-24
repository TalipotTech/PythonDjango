# 🔧 Email Not Working After System Shutdown - QUICK FIX

## ⚡ **THE PROBLEM**

After shutting down your computer, emails stop sending because:
- Environment variables from `setup_smtp.ps1` were **temporary**
- They disappeared when you shut down
- Django reverts to saving emails as files instead of sending them

## ✅ **THE FIX (2 Minutes)**

### **Run This Command Once:**

```powershell
.\setup_smtp_permanent.ps1
```

This interactive script will:
1. Ask for your Gmail address
2. Ask for your App Password
3. Set **permanent** environment variables
4. Make them survive system restarts

### **After Running the Script:**

1. **Close ALL terminals and VS Code**
2. **Reopen VS Code**
3. **Verify it worked:**
   ```powershell
   python check_smtp_status.py
   ```

You should see: ✅ EVERYTHING IS WORKING!

---

## 🎯 **Quick Commands**

```powershell
# 1. Set permanent SMTP configuration (run once)
.\setup_smtp_permanent.ps1

# 2. Check if configuration is working
python check_smtp_status.py

# 3. Test email sending
python test_email_config.py

# 4. Start Django server
python manage.py runserver
```

---

## 🔍 **How to Know If It's Working**

### **✅ Working (SMTP enabled):**
```
python check_smtp_status.py

✅ SUCCESS! All SMTP environment variables are set!
📧 Email System Status: READY
   - Emails will be sent via Gmail SMTP
```

### **❌ Not Working (File backend):**
```
python check_smtp_status.py

⚠️  WARNING: SMTP configuration is incomplete!
📧 Email System Status: USING FILE BACKEND
   - Emails will be saved to 'sent_emails' folder
```

---

## 📝 **What Changed**

### **Before (Temporary):**
- Run `setup_smtp.ps1` every time you start your computer
- Variables lost on shutdown
- Had to remember to run script before Django

### **After (Permanent):**
- Run `setup_smtp_permanent.ps1` **once**
- Variables survive restarts
- Django always uses SMTP automatically

---

## 🆘 **Troubleshooting**

### **"Script asks for Gmail credentials"**
✅ This is normal! Enter:
1. Your Gmail address (e.g., `ensateadoor22@gmail.com`)
2. Your 16-character App Password (get from: https://myaccount.google.com/apppasswords)

### **"Still showing file backend after setup"**
1. Close **ALL** PowerShell/Terminal windows
2. Close VS Code **completely**
3. Reopen VS Code
4. Run `python check_smtp_status.py` again

### **"Don't have an App Password"**
1. Go to: https://myaccount.google.com/apppasswords
2. Enable 2-Factor Authentication first (if not already)
3. Generate a new App Password
4. Copy the 16-character code (no spaces)
5. Run `setup_smtp_permanent.ps1` with this password

### **"Can't find setup_smtp_permanent.ps1"**
Make sure you're in the project directory:
```powershell
cd g:\Sandra\PYTHONDJANGO\PythonDjango
.\setup_smtp_permanent.ps1
```

---

## 📊 **Files You Have**

| File | Purpose | When to Use |
|------|---------|-------------|
| `setup_smtp_permanent.ps1` | ⭐ **Set permanent config** | Run ONCE to fix shutdown issue |
| `check_smtp_status.py` | Check if SMTP is configured | Run anytime to verify status |
| `test_email_config.py` | Test actual email sending | Run to send a test email |
| `setup_smtp.ps1` | Set temporary config | ❌ Don't use (old method) |

---

## 🎯 **Complete Workflow**

```powershell
# 1. One-time setup (fix the shutdown issue)
.\setup_smtp_permanent.ps1
# Enter Gmail: ensateadoor22@gmail.com
# Enter App Password: [your-16-char-password]

# 2. Close VS Code completely and reopen

# 3. Verify it worked
python check_smtp_status.py
# Should show: ✅ EVERYTHING IS WORKING!

# 4. Test email
python test_email_config.py
# Enter a test email address to send to

# 5. Start Django
python manage.py runserver

# 6. Done! Emails will now work forever (even after restart)
```

---

## ✨ **Benefits**

✅ **Set once, works forever**  
✅ **Survives system restarts**  
✅ **No need to remember to run scripts**  
✅ **Works automatically when Django starts**  
✅ **Safe and secure (variables stored in your user profile)**

---

## 🔒 **Security Note**

Your App Password is stored as a **user environment variable** on your Windows account. This means:
- ✅ Only your Windows user can access it
- ✅ Other users on the same computer cannot see it
- ✅ It's stored securely by Windows
- ⚠️ Never commit `.env` files or share your App Password

---

## 📞 **Still Having Issues?**

Run these commands and share the output:

```powershell
# Check environment variables
Get-ChildItem Env: | Where-Object {$_.Name -like "*SMTP*"}

# Check Django configuration
python check_smtp_status.py

# Check detailed Django settings
python test_email_config.py
```

---

**Last Updated**: October 23, 2025  
**Status**: ✅ Ready to use
