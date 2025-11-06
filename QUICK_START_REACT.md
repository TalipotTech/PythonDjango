# 🚀 Quick Start - React Frontend (Node.js Already Installed)

Since Node.js is already on your system, follow these simplified steps:

---

## ✅ Step 1: Verify Node.js Installation

Open PowerShell and check versions:

```powershell
node --version
npm --version
```

You should see version numbers like:
- Node: `v18.x.x` or higher
- npm: `9.x.x` or higher

✅ **If you see versions, you're ready to proceed!**

---

## 📂 Step 2: Navigate to React Folder

### Method 1: Using File Explorer (Easiest)

1. Press **Windows Key + E** (opens File Explorer)
2. Paste this in the address bar:
   ```
   G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend
   ```
3. Press **Enter**
4. Click in the address bar again
5. Type: `powershell`
6. Press **Enter**

### Method 2: Using PowerShell

```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend
```

---

## 📦 Step 3: Install React Dependencies

In the PowerShell window (in react-frontend folder), run:

```powershell
npm install
```

**What happens:**
- Downloads React, React Router, Axios, and other packages
- Takes **2-5 minutes**
- Creates a `node_modules` folder

**Wait for this message:**
```
added 1500+ packages in 3m
```

✅ **Installation complete!**

---

## 🔧 Step 4: Check Configuration (Optional)

The `.env` file should already be configured, but verify:

```powershell
cat .env
```

Should show:
```
REACT_APP_API_URL=http://127.0.0.1:8000/api
PORT=3000
```

If your Django runs on a different port, edit the `.env` file.

---

## ▶️ Step 5: Start Django Backend

**Important:** Django must be running first!

Open a **new PowerShell window**:

```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

✅ **Keep this window open!**

---

## 🚀 Step 6: Start React Frontend

Back in the **react-frontend PowerShell window**, run:

```powershell
npm start
```

**What happens:**
- Compiles React code (takes 20-30 seconds)
- Opens browser automatically
- Shows app at `http://localhost:3000`

You'll see:
```
Compiled successfully!

Local:            http://localhost:3000
On Your Network:  http://192.168.1.100:3000
```

✅ **Your React app is now running!**

---

## 🎉 Step 7: Test the Application

### Test Registration:
1. Click **"Register"** in the navbar
2. Fill in the form
3. Submit
4. Should redirect to Dashboard

### Test Sessions:
1. Click **"Sessions"**
2. You should see workshop sessions
3. Try the filter tabs (All, Active, Upcoming)

### Test Login:
1. Logout and login again
2. Use the credentials you just created

✅ **If everything works, you're all set!**

---

## 🛑 How to Stop

**Stop React:**
- Go to React PowerShell window
- Press **Ctrl + C**
- Type `Y` and press Enter

**Stop Django:**
- Go to Django PowerShell window
- Press **Ctrl + C**
- Type `Y` and press Enter

---

## 🔄 Future Use

**You only need to run `npm install` ONCE!**

Next time, just run:

**Terminal 1 - Django:**
```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango
python manage.py runserver
```

**Terminal 2 - React:**
```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend
npm start
```

---

## ⚠️ Common Issues

### "Port 3000 is already in use"

**Solution:**
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

Or edit `.env` and change to `PORT=3001`

---

### "Failed to fetch" or "Network Error"

**Solutions:**
1. Make sure Django is running on port 8000
2. Test: `http://127.0.0.1:8000/api/auth/register/`
3. Check browser console (F12) for errors

---

### Changes not showing up

**Solution:**
- Hard refresh: **Ctrl + Shift + R**
- Or restart React: Ctrl+C then `npm start`

---

### "Cannot find module" error

**Solution:**
```powershell
Remove-Item -Recurse -Force node_modules
npm install
```

---

## 📋 Quick Command Reference

| Task | Command |
|------|---------|
| Navigate to folder | `cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend` |
| Install dependencies (first time only) | `npm install` |
| Start React | `npm start` |
| Stop React | `Ctrl + C` |
| Start Django | `python manage.py runserver` |
| Check what's running on port | `netstat -ano | findstr :3000` |

---

## 🌐 Important URLs

- **React Frontend:** http://localhost:3000
- **Django Backend:** http://127.0.0.1:8000
- **Django API:** http://127.0.0.1:8000/api/
- **Swagger Docs:** http://127.0.0.1:8000/api/swagger/

---

## ✅ Success Checklist

- [ ] Node.js and npm versions checked
- [ ] Navigated to `react-frontend` folder
- [ ] Ran `npm install` successfully
- [ ] Django running on port 8000
- [ ] React running on port 3000
- [ ] Homepage loads in browser
- [ ] Can register a new user
- [ ] Can view sessions
- [ ] No red errors in console (F12)

---

## 🆘 Need More Help?

- **Full detailed guide:** See `REACT_SETUP_STEP_BY_STEP.md`
- **Beginner explanations:** See `react-frontend/README.md`
- **API documentation:** See `SWAGGER_API_DOCUMENTATION.md`

---

## 🎯 You're Ready!

With Node.js already installed, you're just **3 commands away** from running the app:

```powershell
# 1. Navigate
cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend

# 2. Install (first time only)
npm install

# 3. Start
npm start
```

**Happy coding! 🚀**
