# 🔧 **Fixing Email Configuration After System Shutdown**

## 🎯 **The Problem**

After shutting down your system, the email configuration stops working because:
- ❌ Environment variables set by `setup_smtp.ps1` are **temporary** (session-only)
- ❌ When you close PowerShell or restart your computer, they're **lost**
- ❌ Django falls back to file-based backend (emails saved to files instead of sent)

## ✅ **The Solution - Make SMTP Settings Permanent**

You have **3 options** to fix this:

---

## **OPTION 1: Set Permanent Environment Variables (RECOMMENDED)**

This makes the settings persist across system restarts.

### **Step 1: Open PowerShell as Administrator**
1. Press `Windows + X`
2. Click **"Windows PowerShell (Admin)"** or **"Terminal (Admin)"**

### **Step 2: Run These Commands**

Copy and paste these commands **one by one** (replace with your actual Gmail credentials):

```powershell
[System.Environment]::SetEnvironmentVariable("SMTP_HOST", "smtp.gmail.com", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_PORT", "587", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_USER", "ensateadoor22@gmail.com", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_PASSWORD", "uzfkmbjygspdgork", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_USE_TLS", "True", "User")
[System.Environment]::SetEnvironmentVariable("SENDER_EMAIL", "ensateadoor22@gmail.com", "User")
```

### **Step 3: Verify Installation**

```powershell
# Check if variables are set
Get-ChildItem Env: | Where-Object {$_.Name -like "*SMTP*"}
```

You should see all 5 SMTP variables listed.

### **Step 4: Restart Your Applications**
1. **Close ALL PowerShell/Terminal windows**
2. **Close VS Code completely**
3. **Reopen VS Code**
4. Open a new terminal
5. Run Django: `python manage.py runserver`

### **Step 5: Test It**

```powershell
python test_email_config.py
```

You should now see "SMTP Backend Configured!" instead of "File-based Backend".

---

## **OPTION 2: Create a .env File (Alternative Method)**

This stores settings in a file that Django loads automatically.

### **Step 1: Install python-decouple**

```powershell
pip install python-decouple
```

### **Step 2: Create `.env` File**

Create a file named `.env` (yes, just `.env` with no extension before it) in your project root:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=ensateadoor22@gmail.com
SMTP_PASSWORD=uzfkmbjygspdgork
SMTP_USE_TLS=True
SMTP_USE_SSL=False
SENDER_EMAIL=ensateadoor22@gmail.com
```

### **Step 3: Update settings.py**

Add this at the top of `questionnaire_project/settings.py`:

```python
from decouple import config

# Then replace the SMTP configuration section with:
SMTP_HOST = config('SMTP_HOST', default=None)
if SMTP_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('SMTP_HOST')
    EMAIL_PORT = config('SMTP_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('SMTP_USER', default='')
    EMAIL_HOST_PASSWORD = config('SMTP_PASSWORD', default='')
    EMAIL_USE_TLS = config('SMTP_USE_TLS', default=True, cast=bool)
    EMAIL_USE_SSL = config('SMTP_USE_SSL', default=False, cast=bool)
```

### **Step 4: Add `.env` to `.gitignore`**

**IMPORTANT**: Never commit your `.env` file to Git!

Create or update `.gitignore`:
```
.env
*.env
```

---

## **OPTION 3: Run setup_smtp.ps1 Every Time (Quick Fix)**

If you don't want to make permanent changes, just run the setup script **each time** after system restart:

```powershell
# In your project directory:
.\setup_smtp.ps1

# Then immediately run Django in the SAME terminal:
python manage.py runserver
```

**Pros**: Quick and easy  
**Cons**: Must do this every time you restart your computer or open a new terminal

---

## 🧪 **Testing Your Configuration**

After applying any option above, test with:

```powershell
python test_email_config.py
```

**Expected Output (when working):**
```
✅ SMTP Backend Configured!
   Host: smtp.gmail.com
   Port: 587
   User: ensateadoor22@gmail.com
   Password: ********
   Use TLS: True
```

**Bad Output (when NOT working):**
```
⚠️  File-based Backend (Development Mode)
   Emails are saved to: sent_emails
```

---

## 🔍 **Troubleshooting**

### **"Still using file-based backend after setup!"**

**Solution**: Restart everything!
1. Close all terminals
2. Close VS Code
3. Reopen VS Code
4. Open new terminal
5. Test again

### **"Environment variables not found!"**

**Check if they're set:**
```powershell
Get-ChildItem Env: | Where-Object {$_.Name -like "*SMTP*"}
```

**If empty**, the variables weren't set. Try Option 1 again with PowerShell as **Administrator**.

### **"Can't send email - Authentication failed"**

**Causes:**
1. Wrong Gmail App Password
2. 2-Factor Authentication not enabled
3. Using regular Gmail password instead of App Password

**Solution:**
1. Go to https://myaccount.google.com/apppasswords
2. Generate a NEW App Password
3. Update the environment variable or `.env` file
4. Restart Django

### **"Module 'decouple' not found" (Option 2 only)**

**Solution:**
```powershell
pip install python-decouple
```

---

## 📊 **Comparison of Methods**

| Method | Persistence | Ease of Use | Security | Best For |
|--------|-------------|-------------|----------|----------|
| **Option 1** | ✅ Permanent | Medium | Good | Production use |
| **Option 2** | ✅ Permanent | Easy | Best | Teams/Multiple devs |
| **Option 3** | ❌ Temporary | Very Easy | Good | Quick testing |

---

## ✅ **Recommended Workflow**

**For Development (your case):**
1. Use **Option 1** (Permanent Environment Variables)
2. Set them once and forget about it
3. Email will work every time you restart

**For Team Projects:**
1. Use **Option 2** (.env file)
2. Share a `.env.example` file (without passwords) with your team
3. Each developer creates their own `.env` file

**For Quick Testing:**
1. Use **Option 3** (run setup script each time)
2. Good for temporary setups

---

## 🎯 **Quick Command Reference**

```powershell
# Set permanent environment variables (Option 1)
[System.Environment]::SetEnvironmentVariable("SMTP_HOST", "smtp.gmail.com", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_PORT", "587", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_USER", "your-email@gmail.com", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_PASSWORD", "your-app-password", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_USE_TLS", "True", "User")
[System.Environment]::SetEnvironmentVariable("SENDER_EMAIL", "your-email@gmail.com", "User")

# Verify variables are set
Get-ChildItem Env: | Where-Object {$_.Name -like "*SMTP*"}

# Test email configuration
python test_email_config.py

# Run Django server
python manage.py runserver
```

---

## 🚀 **Next Steps**

1. Choose which option you want to use (I recommend **Option 1**)
2. Follow the steps for that option
3. Test with `python test_email_config.py`
4. Restart your computer to verify it persists
5. Test again after restart

---

**Last Updated**: October 23, 2025
