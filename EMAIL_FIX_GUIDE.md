# 🔧 Email Integration Fix Guide

## 📋 **Current Status**

Your email system is **working** but in **development mode**:
- ✅ Emails are being generated correctly
- ✅ Email templates are working fine
- ❌ Emails are saved to files (`sent_emails/` folder) instead of being sent
- ❌ No SMTP configuration found

## 🎯 **The Problem**

Your Django app is using the **file-based email backend** (development mode), which saves emails to files instead of actually sending them. To send real emails, you need to configure **SMTP** (Gmail).

---

## 🚀 **Quick Fix (3 Steps)**

### **Step 1: Get Gmail App Password**

1. Go to your Gmail account
2. Enable **2-Factor Authentication** if not already enabled:
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process

3. Generate an **App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - Copy the **16-character password** (it looks like: `abcd efgh ijkl mnop`)
   - Remove spaces: `abcdefghijklmnop`

### **Step 2: Configure SMTP**

1. Open `setup_smtp.ps1` in your project folder
2. Edit these lines with YOUR information:
   ```powershell
   $YOUR_EMAIL = "ensateadoor22@gmail.com"        # Your Gmail address
   $YOUR_APP_PASSWORD = "uzfkmbjygspdgork"     # Your App Password (no spaces!)
   ```

3. Save the file

### **Step 3: Run the Setup**

1. Open PowerShell in your project directory
2. Run:
   ```powershell
   .\setup_smtp.ps1
   ```
3. You should see: ✅ SMTP Configuration Set!

4. **In the SAME PowerShell window**, start your Django server:
   ```powershell
   python manage.py runserver
   ```

---

## ✅ **Test Your Email**

After setting up SMTP, test it:

```powershell
python test_email_config.py
```

Follow the prompts to send a test email.

---

## 🔍 **Verify It's Working**

1. **In Django**: When users request a session code, they should receive an actual email
2. **Check Gmail**: Look in the recipient's inbox (and spam folder)
3. **No more files**: Emails won't be saved to `sent_emails/` folder anymore

---

## 🛠️ **Make It Permanent (Optional)**

The setup script sets environment variables for the current PowerShell session only. To make them permanent:

1. Open PowerShell as Administrator
2. Run these commands (replace with your actual values):

```powershell
[System.Environment]::SetEnvironmentVariable("SMTP_HOST", "smtp.gmail.com", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_PORT", "587", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_USER", "ensateadoor22@gmail.com", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_PASSWORD", "uzfkmbjygspdgork", "User")
[System.Environment]::SetEnvironmentVariable("SMTP_USE_TLS", "True", "User")
[System.Environment]::SetEnvironmentVariable("SENDER_EMAIL", "ensateadoor22@gmail.com", "User")
```

3. Restart VS Code and your terminal for changes to take effect

---

## ⚠️ **Troubleshooting**

### **Email Not Sending?**

1. **Check App Password**: 
   - Make sure you're using an App Password, not your regular Gmail password
   - Remove all spaces from the password

2. **Check 2FA**: 
   - Ensure 2-Factor Authentication is enabled on Gmail
   - App Passwords only work with 2FA enabled

3. **Check Internet**: 
   - Ensure you have internet connection
   - Try pinging `smtp.gmail.com`

4. **Check Gmail Security**:
   - Sometimes Gmail blocks sign-ins from "less secure apps"
   - Go to: https://myaccount.google.com/lesssecureapps
   - Make sure it's turned ON

### **Still Using File Backend?**

If emails are still going to files:
1. Check that environment variables are set: `Get-ChildItem Env: | Where-Object {$_.Name -like "*SMTP*"}`
2. Restart Django server **in the same PowerShell window** where you ran `setup_smtp.ps1`
3. Run `python test_email_config.py` to verify

### **"Authentication Failed" Error?**

- Double-check your Gmail address
- Verify the App Password is correct (no spaces!)
- Make sure 2FA is enabled
- Try generating a new App Password

---

## 📚 **How It Works**

Your Django app has **two email backends**:

1. **File Backend** (default, development):
   - Saves emails to `sent_emails/` folder
   - No actual email sent
   - Good for testing without SMTP

2. **SMTP Backend** (production):
   - Sends real emails via Gmail
   - Requires SMTP configuration
   - Activated when `SMTP_HOST` environment variable is set

The code in `settings.py` automatically switches between them based on environment variables.

---

## 📝 **Quick Reference**

| Command | Purpose |
|---------|---------|
| `.\setup_smtp.ps1` | Configure SMTP for current session |
| `python test_email_config.py` | Test email configuration |
| `python manage.py runserver` | Start Django with email enabled |
| `Get-ChildItem Env:` | View environment variables |

---

## 🎉 **Success Indicators**

You'll know it's working when:
- ✅ Test script shows "SMTP Backend Configured!"
- ✅ Test email arrives in inbox
- ✅ Session codes are emailed to users (not saved to files)
- ✅ No errors in Django console when sending emails

---

## 💡 **Tips**

1. **Security**: Never commit your App Password to Git!
2. **Development**: Use file backend for testing (no setup needed)
3. **Production**: Use SMTP backend with environment variables
4. **Testing**: Always test with a real email address first

---

## 📞 **Need Help?**

If you're still having issues:
1. Run `python test_email_config.py` and share the output
2. Check Django console for error messages
3. Verify your Gmail account settings
4. Make sure you're using PowerShell (not CMD)

---

**Last Updated**: October 23, 2025
