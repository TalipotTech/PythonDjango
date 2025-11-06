# 🚀 Quick Start Guide - React Frontend Setup

## Step-by-Step Instructions

### 1. Open PowerShell in React Folder

```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend
```

### 2. Install Dependencies

```powershell
npm install
```

**Wait for:** "added 1500 packages" message (takes 2-5 minutes)

### 3. Start React Development Server

```powershell
npm start
```

**What happens:**
- Compiles React app
- Opens browser automatically at `http://localhost:3000`
- Shows homepage of Quiz Workshop System

### 4. Verify Django Backend is Running

**In another PowerShell window:**

```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango
python manage.py runserver
```

**Check:** `http://127.0.0.1:8000` should show Django page

---

## 🧪 Test the Application

### Test 1: Registration
1. Go to `http://localhost:3000`
2. Click "Register" in navbar
3. Fill in form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - First Name: `Test`
   - Last Name: `User`
4. Click "Register"
5. Should redirect to Dashboard

### Test 2: Browse Sessions
1. Click "Sessions" in navbar
2. Should see list of active workshop sessions
3. Try filter tabs: "All", "Active", "Upcoming"
4. Click "View Details" on any session

### Test 3: Take Quiz (Need Session Code)
1. Get session code from Django admin
2. Click "Register" on a session
3. Enter session code
4. Fill attendee form
5. Click "Take Quiz"
6. Answer questions
7. Submit feedback

---

## ✅ Success Checklist

- [ ] `npm install` completed without errors
- [ ] `npm start` opens browser automatically
- [ ] Homepage loads at `http://localhost:3000`
- [ ] Can see navbar with Login/Register links
- [ ] Can click "Sessions" and see session list
- [ ] Can click "Register" and see registration form
- [ ] Django backend running on port 8000
- [ ] No red errors in browser console (F12)

---

## 🔧 Common Issues

### "npm is not recognized"
**Solution:** Install Node.js from https://nodejs.org/

### "Port 3000 already in use"
**Solution:** 
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

### "Failed to fetch" or "Network Error"
**Solutions:**
1. Check Django is running: `http://127.0.0.1:8000/api/auth/register/`
2. Check CORS settings in Django `settings.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://127.0.0.1:3000",
   ]
   ```

### Changes not showing up
**Solution:**
- Hard refresh: `Ctrl + Shift + R`
- Or restart: `Ctrl + C` then `npm start`

---

## 📂 Project Structure

```
react-frontend/
├── public/
│   └── index.html          # HTML entry point
├── src/
│   ├── components/         # React components
│   │   ├── auth/          # Login, Register
│   │   ├── sessions/      # Session list, detail
│   │   ├── attendee/      # Registration flow
│   │   ├── quiz/          # Quiz interface
│   │   ├── feedback/      # Feedback form
│   │   ├── common/        # Navbar
│   │   └── pages/         # Home, Dashboard
│   ├── services/
│   │   └── api.js         # API calls to Django
│   ├── styles/            # CSS files
│   ├── App.js             # Main app + routing
│   └── index.js           # Entry point
├── .env                   # API configuration
├── package.json           # Dependencies
└── README.md              # Full documentation
```

---

## 🎯 Next Steps

1. **Read README.md** - Full beginner guide with explanations
2. **Try creating an account** - Test registration flow
3. **Browse sessions** - See active workshops
4. **Take a quiz** - Get session code from Django admin
5. **Explore code** - Check out components with BEGINNER EXPLANATION comments

---

## 📚 Learning Resources

- **React Docs:** https://react.dev/learn
- **React Router:** https://reactrouter.com/en/main
- **Axios:** https://axios-http.com/docs/intro

---

## 🆘 Need Help?

1. Check browser console (F12) for errors
2. Check PowerShell terminal for errors
3. Read error messages carefully
4. Google the error message
5. Check README.md for detailed troubleshooting

---

## 🎉 You're All Set!

Your React frontend is ready to use! Start by registering a new account and exploring the application.

**Happy coding! 🚀**
