# 📖 Complete Step-by-Step Instructions for React Frontend

## 🎯 Overview

This guide will walk you through setting up and running the React frontend for your Django Quiz Workshop System. Follow each step carefully.

---

## ⚠️ Before You Start

**What you'll need:**
- Your Django backend (already working)
- Internet connection (to download Node.js and packages)
- About 15-20 minutes of time

---

## 📥 STEP 1: Install Node.js

### 1.1 Download Node.js

1. Open your web browser
2. Go to: **https://nodejs.org/**
3. You'll see two download buttons:
   - **LTS (Long Term Support)** - Recommended, more stable
   - **Current** - Latest features
4. Click the **LTS version** button (recommended)
5. The download will start automatically (file size: ~30-50 MB)

### 1.2 Install Node.js

1. Find the downloaded file (usually in your Downloads folder)
   - File name: something like `node-v20.9.0-x64.msi`
2. **Double-click** the installer file
3. The Node.js Setup Wizard will open:
   - Click **"Next"**
   - Accept the license agreement → Click **"Next"**
   - Choose installation location (default is fine) → Click **"Next"**
   - Keep all features checked → Click **"Next"**
   - Click **"Install"**
   - Wait for installation (takes 2-3 minutes)
   - Click **"Finish"**

### 1.3 Verify Node.js Installation

1. Press **Windows Key + R**
2. Type: `powershell`
3. Press **Enter** (PowerShell window opens)
4. Type this command and press Enter:
   ```powershell
   node --version
   ```
5. You should see something like: `v20.9.0` or similar
6. Now check npm (comes with Node.js):
   ```powershell
   npm --version
   ```
7. You should see something like: `10.1.0` or similar

✅ **If you see version numbers, Node.js is installed correctly!**

❌ **If you see an error:**
- Close PowerShell
- Restart your computer
- Try the verification steps again

---

## 📂 STEP 2: Navigate to React Project Folder

### 2.1 Using File Explorer (Easier Method)

1. Open **File Explorer** (Windows Key + E)
2. In the address bar at the top, type or paste:
   ```
   G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend
   ```
3. Press **Enter**
4. You should see folders like: `public`, `src`, and files like `package.json`
5. Click in the **address bar** at the top
6. Type: `powershell`
7. Press **Enter**
8. A PowerShell window opens in this folder

### 2.2 Using PowerShell Commands (Alternative Method)

1. Press **Windows Key + R**
2. Type: `powershell`
3. Press **Enter**
4. In PowerShell, type:
   ```powershell
   cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend
   ```
5. Press **Enter**

### 2.3 Verify You're in the Right Folder

Type this command:
```powershell
dir
```

You should see these files and folders:
- `public` (folder)
- `src` (folder)
- `package.json` (file)
- `.env` (file)
- `README.md` (file)

✅ **If you see these, you're in the right place!**

---

## 📦 STEP 3: Install React Dependencies

### 3.1 Run the Installation Command

In PowerShell (in the `react-frontend` folder), type:
```powershell
npm install
```

Press **Enter**

### 3.2 What Happens Now?

- npm reads `package.json` to see what packages are needed
- It downloads React, React Router, Axios, and other tools
- Creates a `node_modules` folder (will be ~200-300 MB)
- This takes **2-5 minutes** depending on your internet speed

### 3.3 What You'll See

You'll see lots of text scrolling:
```
npm WARN deprecated package1@1.0.0: some message
npm WARN deprecated package2@2.0.0: another message
...
added 1523 packages, and audited 1524 packages in 3m
```

**Don't worry about:**
- "WARN" messages - these are just warnings, not errors
- Lots of packages being downloaded - React needs many tools

**Do worry if you see:**
- "ERROR" messages in red
- "npm ERR!" messages

### 3.4 Installation Complete

When you see:
```
added XXXX packages in XXm
```

✅ **Installation is complete!**

---

## 🔧 STEP 4: Configure Environment Variables

### 4.1 Check the .env File

1. In the `react-frontend` folder, find the file named `.env`
   - If you don't see it, enable "Show hidden files" in File Explorer:
     - Click "View" menu
     - Check "Hidden items"
2. Right-click `.env`
3. Select **"Open with"** → **"Notepad"**

### 4.2 Verify the Contents

The file should contain:
```
REACT_APP_API_URL=http://127.0.0.1:8000/api
PORT=3000
```

### 4.3 Adjust if Needed

**If your Django runs on a different port:**
- Change `8000` to your Django port number
- Example: If Django is on port 8080, change to:
  ```
  REACT_APP_API_URL=http://127.0.0.1:8080/api
  ```

**If you want React on a different port:**
- Change `PORT=3000` to another number like `PORT=3001`

Save and close the file.

---

## ▶️ STEP 5: Start Django Backend

**IMPORTANT:** Django must be running BEFORE you start React!

### 5.1 Open a New PowerShell Window

1. Press **Windows Key + R**
2. Type: `powershell`
3. Press **Enter**
4. Navigate to Django folder:
   ```powershell
   cd G:\Sandra\PYTHONDJANGO\PythonDjango
   ```

### 5.2 Start Django Server

Type this command:
```powershell
python manage.py runserver
```

Press **Enter**

### 5.3 Verify Django is Running

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

✅ **Django is now running!**

**Test it:**
- Open browser
- Go to: `http://127.0.0.1:8000/api/auth/register/`
- You should see a Django REST API page

**Keep this PowerShell window open!** Don't close it or Django will stop.

---

## 🚀 STEP 6: Start React Frontend

### 6.1 Open Another PowerShell Window

1. Go back to File Explorer
2. Navigate to: `G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend`
3. Click in the address bar
4. Type: `powershell`
5. Press **Enter**

### 6.2 Start React Development Server

In the new PowerShell window, type:
```powershell
npm start
```

Press **Enter**

### 6.3 What Happens

1. React compiles your code (takes 20-30 seconds)
2. You'll see:
   ```
   Compiled successfully!
   
   You can now view react-frontend in the browser.
   
     Local:            http://localhost:3000
     On Your Network:  http://192.168.1.100:3000
   ```
3. Your web browser will **automatically open**
4. The React app loads at `http://localhost:3000`

### 6.4 If Browser Doesn't Open Automatically

1. Open your browser manually
2. Go to: `http://localhost:3000`

✅ **You should see the Quiz Workshop homepage!**

---

## 🎉 STEP 7: Test the Application

### 7.1 Test Homepage

You should see:
- A blue navigation bar at the top
- "Quiz Workshop System" title
- Hero section with "Welcome" message
- "Login" and "Register" buttons

### 7.2 Test Registration

1. Click **"Register"** in the navbar
2. Fill in the form:
   - **Username:** `testuser123`
   - **Email:** `test@example.com`
   - **Password:** `mypassword123`
   - **Confirm Password:** `mypassword123`
   - **First Name:** `Test`
   - **Last Name:** `User`
3. Click **"Register"** button
4. You should be redirected to the Dashboard

✅ **If you see the Dashboard, registration works!**

### 7.3 Test Login

1. Click **"Logout"** in the navbar
2. Click **"Login"**
3. Enter:
   - **Username:** `testuser123`
   - **Password:** `mypassword123`
4. Click **"Login"** button
5. You should be redirected to the Dashboard

✅ **If you see the Dashboard, login works!**

### 7.4 Test Sessions List

1. Click **"Sessions"** in the navbar
2. You should see a list of workshop sessions
3. Try the filter tabs:
   - Click **"All"** - shows all sessions
   - Click **"Active"** - shows only active sessions
   - Click **"Upcoming"** - shows future sessions

✅ **If you see sessions, the API connection works!**

---

## 🔍 STEP 8: Verify Everything is Working

### 8.1 Check Both Terminals

You should have **TWO PowerShell windows open:**

**Window 1 - Django:**
```
System check identified no issues (0 silenced).
October 31, 2025 - 10:30:00
Django version 4.2.x
Starting development server at http://127.0.0.1:8000/
```

**Window 2 - React:**
```
Compiled successfully!

webpack compiled with 0 warnings
Files successfully emitted, waiting for typecheck results...
No issues found.
```

### 8.2 Check Browser Console (Optional but Good to Learn)

1. In your browser, press **F12**
2. Click the **"Console"** tab
3. You should NOT see any red error messages

✅ **If no red errors, everything is working perfectly!**

---

## 🛑 STEP 9: How to Stop the Servers

### 9.1 Stop React Server

1. Go to the PowerShell window running React
2. Press **Ctrl + C**
3. Type: `Y`
4. Press **Enter**

### 9.2 Stop Django Server

1. Go to the PowerShell window running Django
2. Press **Ctrl + C**
3. Type: `Y`
4. Press **Enter**

✅ **Both servers are now stopped**

---

## 🔄 STEP 10: How to Start Again Later

### Every Time You Want to Use the App:

**Terminal 1 - Start Django:**
```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango
python manage.py runserver
```

**Terminal 2 - Start React:**
```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend
npm start
```

**Note:** You only need to run `npm install` ONCE (the first time). After that, just use `npm start`.

---

## ⚠️ Common Problems & Solutions

### Problem 1: "npm is not recognized"

**Cause:** Node.js not installed or not in PATH

**Solution:**
1. Install Node.js from https://nodejs.org/
2. Restart your computer
3. Try again

---

### Problem 2: "Port 3000 is already in use"

**Cause:** React is already running, or another program is using port 3000

**Solution Option A - Kill the process:**
```powershell
netstat -ano | findstr :3000
```
Look for the PID number (last column), then:
```powershell
taskkill /PID <PID_NUMBER> /F
```

**Solution Option B - Use a different port:**
1. Edit `.env` file
2. Change `PORT=3000` to `PORT=3001`
3. Save and try again

---

### Problem 3: "Failed to fetch" or "Network Error"

**Cause:** Django is not running, or CORS not configured

**Solution:**
1. Make sure Django is running: `http://127.0.0.1:8000`
2. Check CORS in Django `settings.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://127.0.0.1:3000",
   ]
   ```
3. Restart both servers

---

### Problem 4: Blank page or white screen

**Cause:** JavaScript error

**Solution:**
1. Press **F12** in browser
2. Click **"Console"** tab
3. Look for red error messages
4. Copy the error message
5. Google it or ask for help

---

### Problem 5: Changes not appearing

**Cause:** Browser cache

**Solution:**
1. Hard refresh: **Ctrl + Shift + R**
2. Or clear browser cache
3. Or restart React server:
   - Press **Ctrl + C**
   - Run `npm start` again

---

### Problem 6: "Cannot find module" errors

**Cause:** Dependencies not installed properly

**Solution:**
```powershell
# Delete node_modules folder and package-lock.json
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json

# Reinstall everything
npm install
```

---

## 📋 Quick Reference

### Essential Commands

| Task | Command |
|------|---------|
| Check Node.js version | `node --version` |
| Check npm version | `npm --version` |
| Navigate to folder | `cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend` |
| Install dependencies | `npm install` |
| Start React server | `npm start` |
| Stop server | `Ctrl + C` then `Y` |
| List files in folder | `dir` |
| Clear terminal | `cls` |

### Important URLs

| Service | URL |
|---------|-----|
| React Frontend | http://localhost:3000 |
| Django Backend | http://127.0.0.1:8000 |
| Django API | http://127.0.0.1:8000/api/ |
| Swagger Docs | http://127.0.0.1:8000/api/swagger/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

---

## 📚 Next Steps

### 1. Explore the Application

- Create a user account
- Browse sessions
- Register for a session (you'll need a session code from Django admin)
- Take a quiz
- Submit feedback

### 2. Learn React Basics

- Open `README.md` for beginner-friendly explanations
- Read the comments in component files (they explain everything!)
- Check out: https://react.dev/learn

### 3. Understand the Code

Start with these files (in order):
1. `src/index.js` - Entry point
2. `src/App.js` - Main app and routing
3. `src/components/auth/Login.js` - See how login works
4. `src/services/api.js` - See how API calls work

Each file has **BEGINNER EXPLANATION** sections!

---

## 🎯 Success Checklist

Use this to verify everything:

- [ ] Node.js installed (check with `node --version`)
- [ ] npm installed (check with `npm --version`)
- [ ] Navigated to `react-frontend` folder
- [ ] Ran `npm install` successfully
- [ ] `.env` file configured correctly
- [ ] Django server running on port 8000
- [ ] React server running on port 3000
- [ ] Homepage loads in browser
- [ ] Can click around the navigation
- [ ] Can register a new user
- [ ] Can login successfully
- [ ] Can view sessions list
- [ ] No red errors in browser console

---

## 🆘 Still Having Issues?

### Debugging Checklist:

1. **Read error messages carefully** - they usually tell you what's wrong
2. **Check browser console** (F12 → Console tab)
3. **Check PowerShell terminals** for error messages
4. **Restart both servers**
5. **Restart your computer** (sometimes helps!)
6. **Google the error message** - copy/paste it
7. **Check the README.md** for more detailed explanations

### When Asking for Help, Provide:

1. What step you were on
2. What command you ran
3. The full error message (copy/paste from PowerShell)
4. Screenshot of the error (if in browser)
5. Your Node.js version (`node --version`)
6. Your npm version (`npm --version`)

---

## 🎉 Congratulations!

You now have a fully working React frontend connected to your Django backend!

**What you've accomplished:**
✅ Installed Node.js and npm
✅ Set up a professional React project
✅ Connected React to Django API
✅ Built a complete quiz workshop system
✅ Learned basic React concepts

**Keep learning and building! 🚀**

---

## 📞 Project Information

**Project Name:** React Quiz Workshop Frontend
**Version:** 1.0.0
**React Version:** 18.2.0
**Node.js Required:** 18.x or higher

**Project Location:**
```
G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend\
```

**Documentation:**
- `README.md` - Complete beginner guide
- `SETUP_INSTRUCTIONS.md` - Quick start guide
- This file - Step-by-step instructions

**Happy Coding! 🎓**
