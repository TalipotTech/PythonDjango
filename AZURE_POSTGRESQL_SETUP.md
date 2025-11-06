# 🔥 Azure PostgreSQL Setup Guide for Your Django Project

## ✅ Your Azure Database Info

**Server Details:**
- **Server Name:** ensatepgserver
- **Endpoint:** ensatepgserver.postgres.database.azure.com
- **Location:** South India
- **PostgreSQL Version:** 17.6
- **Admin User:** pgAdmin
- **Configuration:** Burstable B2s (2 vCores, 4 GiB RAM, 32 GiB storage)

---

## 🔧 Step-by-Step Setup

### **Step 1: Add Firewall Rule in Azure ⚠️ IMPORTANT**

You need to click **"Connect"** button in Azure Portal (as shown in your screenshot):

1. In Azure Portal, click the blue **"Connect"** button
2. Click **"Add this firewall rule"** to allow your IP (117.241.76.186)
3. Wait a few seconds for the rule to apply

**OR manually add firewall rule:**
1. Go to **Networking** (left sidebar)
2. Click **"Add current client IP address"** or **"Add firewall rule"**
3. Add your IP: `117.241.76.186`
4. Click **Save**

---

### **Step 2: Get Your Database Password**

You need the password you set when creating the database. If you forgot it:

1. In Azure Portal, go to your database
2. Click **"Reset password"** (top menu)
3. Enter a new password and save it

---

### **Step 3: Update Your .env File**

I've created a `.env` file for you. Now edit it:

```powershell
notepad .env
```

Replace `YOUR_PASSWORD_HERE` with your actual database password:

```env
DATABASE_URL=postgresql://pgAdmin:YOUR_ACTUAL_PASSWORD@ensatepgserver.postgres.database.azure.com:5432/postgres?sslmode=require
```

**⚠️ Important:** 
- Make sure there are NO SPACES in the connection string
- If password has special characters like `@`, `#`, `&`, you need to URL-encode them:
  - `@` → `%40`
  - `#` → `%23`
  - `&` → `%26`
  - `!` → `%21`

---

### **Step 4: Test Connection**

```powershell
# Navigate to your project
cd g:\Sandra\PYTHONDJANGO\PythonDjango

# Test database connection
C:/Python313/python.exe manage.py check --database default
```

---

### **Step 5: Run Migrations**

```powershell
# Create all necessary tables in Azure PostgreSQL
C:/Python313/python.exe manage.py migrate
```

---

### **Step 6: Create Superuser (Admin)**

```powershell
C:/Python313/python.exe manage.py createsuperuser
```

Follow the prompts to create an admin account.

---

### **Step 7: (Optional) Migrate Existing Data**

If you have data in your local SQLite database:

```powershell
# 1. Backup SQLite data
C:/Python313/python.exe manage.py dumpdata > backup_data.json

# 2. Load into Azure PostgreSQL (after migrations)
C:/Python313/python.exe manage.py loaddata backup_data.json
```

---

## 🔍 Verify Connection

Check which database you're using:

```powershell
C:/Python313/python.exe -c "from decouple import config; print(config('DATABASE_URL', default='Using SQLite'))"
```

---

## 🚀 Start Your Server

```powershell
C:/Python313/python.exe manage.py runserver
```

Your Django app will now use **Azure PostgreSQL in the cloud**! ☁️

---

## 🛠️ Troubleshooting

### Error: "could not connect to server"
**Solution:** Add firewall rule in Azure (Step 1)

### Error: "password authentication failed"
**Solution:** Reset password in Azure Portal and update `.env`

### Error: "SSL connection required"
**Solution:** Already included `?sslmode=require` in the connection string

### Error: "FATAL: database does not exist"
**Solution:** Azure creates a default `postgres` database. Use that or create a new one:
```sql
CREATE DATABASE quizportal;
```
Then update DATABASE_URL to use `/quizportal` instead of `/postgres`

---

## 🔒 Security Best Practices

✅ **DO:**
- Keep `.env` file secret (already in `.gitignore`)
- Use strong passwords (16+ characters)
- Enable Azure firewall rules (only your IP)
- Use SSL/TLS (already configured)

❌ **DON'T:**
- Commit `.env` to GitHub
- Share database credentials publicly
- Allow all IPs (0.0.0.0/0) in firewall

---

## 💰 Azure PostgreSQL Costs

**Your Current Plan:** Burstable B2s
- **Cost:** ~$30-40/month
- **Free Credit:** If you're on Azure free trial, you get $200 credit for 30 days

**💡 Tip:** For development, you can downgrade to B1ms (1 vCore, 2 GiB RAM) to save costs.

---

## 📊 Monitor Your Database

In Azure Portal:
1. **Monitoring** → View CPU, Memory, Storage usage
2. **Activity log** → See all operations
3. **Metrics** → Database connections, queries

---

## 🎯 Quick Reference

**Connection String Format:**
```
postgresql://pgAdmin:PASSWORD@ensatepgserver.postgres.database.azure.com:5432/postgres?sslmode=require
```

**Admin Panel:**
- Azure Portal: https://portal.azure.com
- Django Admin: http://localhost:8000/admin

---

## ✨ You're All Set!

Your Django project is now connected to Azure PostgreSQL! 🎉

**Next Steps:**
1. Click "Connect" in Azure Portal to add firewall rule
2. Update `.env` with your password
3. Run migrations
4. Start building! 🚀

Need help? Let me know! 😊
