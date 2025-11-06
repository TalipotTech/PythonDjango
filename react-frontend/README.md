# React Quiz Workshop Frontend

A beginner-friendly React application that connects to the Django Quiz Workshop System. This frontend allows students to register for sessions, take quizzes, and provide feedback.

---

## 🎯 What is This Project?

This is a **React web application** that works together with your Django backend. Think of it as the "face" of your quiz system - what users see and interact with in their web browser.

**Key Features:**
- 📝 Student registration and login
- 📚 Browse active workshop sessions
- ✅ Register for sessions with session codes
- 📋 Take interactive quizzes
- 💬 Submit feedback after quizzes
- 📊 View personal dashboard with progress

---

## 📋 Prerequisites (What You Need First)

Before you can run this React app, you need to install these programs:

### 1. **Node.js** (JavaScript Runtime)
   - **What it is:** Node.js lets you run JavaScript on your computer (not just in browsers)
   - **Download from:** https://nodejs.org/
   - **Which version:** Download the **LTS version** (Long Term Support) - it's the most stable
   - **How to check if installed:** Open PowerShell and type:
     ```powershell
     node --version
     ```
     You should see something like `v18.17.0` or higher

### 2. **npm** (Node Package Manager)
   - **What it is:** npm installs React and other tools your project needs
   - **Good news:** npm comes automatically with Node.js!
   - **How to check if installed:**
     ```powershell
     npm --version
     ```
     You should see something like `9.6.7` or higher

### 3. **Django Backend** (Already Running)
   - Your Django server must be running on `http://127.0.0.1:8000`
   - The React app talks to Django to get data and save information

---

## 🚀 Installation Steps

Follow these steps **exactly** in order:

### Step 1: Open PowerShell in the React Project Folder

1. Open **File Explorer**
2. Navigate to: `G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend`
3. Click in the address bar at the top
4. Type `powershell` and press Enter
5. A PowerShell window will open in this folder

### Step 2: Install Dependencies

In PowerShell, type this command and press Enter:

```powershell
npm install
```

**What this does:** Downloads React, React Router, Axios, and all other tools needed

**How long it takes:** 2-5 minutes (depending on your internet speed)

**What you'll see:** Lots of text scrolling by - this is normal! Wait until you see:
```
added 1500 packages in 3m
```

### Step 3: Check Your Environment File

1. Open the file: `react-frontend/.env`
2. Make sure it says:
   ```
   REACT_APP_API_URL=http://127.0.0.1:8000/api
   PORT=3000
   ```
3. **If Django runs on a different port**, change `8000` to match

---

## ▶️ Running the React App

### Start the Development Server

In PowerShell (in the `react-frontend` folder), type:

```powershell
npm start
```

**What this does:** Starts the React development server

**What you'll see:**
```
Compiled successfully!

You can now view react-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.100:3000
```

**What happens next:**
- Your web browser will automatically open
- You'll see the React app at `http://localhost:3000`
- If the browser doesn't open, manually go to that URL

### Stop the Server

When you want to stop the React app:
1. Go to the PowerShell window
2. Press `Ctrl + C`
3. Type `Y` and press Enter

---

## 🌐 Using the Application

### First Time Setup

1. **Start Django Backend** (in a separate PowerShell window):
   ```powershell
   cd G:\Sandra\PYTHONDJANGO\PythonDjango
   python manage.py runserver
   ```

2. **Start React Frontend** (in another PowerShell window):
   ```powershell
   cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend
   npm start
   ```

3. **Open browser** to `http://localhost:3000`

### For Students (Regular Users)

1. **Register an Account:**
   - Click "Register" in the navigation bar
   - Fill in: username, email, password, first name, last name
   - Click "Register"
   - You'll be logged in automatically

2. **Browse Sessions:**
   - Click "Sessions" to see available workshops
   - Filter by "All", "Active", or "Upcoming"

3. **Register for a Session:**
   - You need a **session code** from your teacher
   - Click "Register" on any session card
   - Enter the session code
   - Fill in your phone number and other details
   - Submit the form

4. **Take a Quiz:**
   - During an active session, click "Take Quiz"
   - Answer questions one by one
   - Click "Next" to move forward
   - Click "Submit" on the last question

5. **Submit Feedback:**
   - After completing the quiz, you'll see a feedback form
   - Choose feedback type and write your comments
   - Click "Submit Feedback"

6. **View Dashboard:**
   - Click "Dashboard" to see:
     - Sessions you've registered for
     - Quiz completion status
     - Your progress

---

## 📁 Project Structure (What Each Folder Does)

```
react-frontend/
│
├── public/                  # Static files (don't edit these much)
│   └── index.html          # Main HTML file (entry point)
│
├── src/                     # Your React code (THIS is where you work!)
│   │
│   ├── components/          # Reusable UI pieces
│   │   ├── auth/           # Login & Register components
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   └── ProtectedRoute.js
│   │   │
│   │   ├── sessions/       # Session browsing components
│   │   │   ├── SessionList.js
│   │   │   └── SessionDetail.js
│   │   │
│   │   ├── attendee/       # Registration flow
│   │   │   └── AttendeeRegistration.js
│   │   │
│   │   ├── quiz/           # Quiz taking interface
│   │   │   └── Quiz.js
│   │   │
│   │   ├── feedback/       # Feedback form
│   │   │   └── Feedback.js
│   │   │
│   │   ├── common/         # Shared components
│   │   │   └── Navbar.js
│   │   │
│   │   └── pages/          # Full page components
│   │       ├── Home.js
│   │       └── Dashboard.js
│   │
│   ├── services/            # Backend communication
│   │   └── api.js          # All API calls to Django
│   │
│   ├── styles/              # CSS styling files
│   │   ├── index.css       # Global styles
│   │   ├── Auth.css        # Login/Register styles
│   │   ├── Sessions.css    # Session list styles
│   │   ├── Quiz.css        # Quiz interface styles
│   │   └── ...             # More style files
│   │
│   ├── App.js               # Main app component (routing)
│   └── index.js             # Entry point (renders App)
│
├── .env                     # Environment variables (API URL)
├── package.json             # Project dependencies list
└── README.md                # This file!
```

---

## 🔧 Common Issues & Solutions

### Issue 1: "npm is not recognized"

**Problem:** PowerShell doesn't know what `npm` is

**Solution:**
1. Install Node.js from https://nodejs.org/
2. Restart PowerShell
3. Try `npm --version` again

---

### Issue 2: Port 3000 Already in Use

**Problem:** Error message says `Port 3000 is already in use`

**Solution:**
```powershell
# Find what's using port 3000
netstat -ano | findstr :3000

# Kill that process (replace PID with the number you see)
taskkill /PID <PID> /F

# Or use a different port in .env file
PORT=3001
```

---

### Issue 3: Cannot Connect to Django API

**Problem:** React app loads but shows "Network Error" or "Failed to fetch"

**Solution:**
1. Make sure Django is running: `python manage.py runserver`
2. Check Django is at `http://127.0.0.1:8000`
3. Test in browser: `http://127.0.0.1:8000/api/auth/register/`
4. Check CORS settings in Django `settings.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://127.0.0.1:3000",
   ]
   ```

---

### Issue 4: "Module not found" Errors

**Problem:** React can't find a package like 'react-router-dom'

**Solution:**
```powershell
# Delete node_modules and reinstall everything
Remove-Item -Recurse -Force node_modules
npm install
```

---

### Issue 5: Changes Not Showing Up

**Problem:** You edited code but the browser doesn't show changes

**Solution:**
1. Save the file (Ctrl + S)
2. Wait 2-3 seconds (React auto-reloads)
3. Hard refresh browser: `Ctrl + Shift + R`
4. If still not working, restart React server:
   - Press `Ctrl + C` in PowerShell
   - Run `npm start` again

---

## 🎓 Learning React Basics

### What is a Component?

A **component** is a piece of UI that you can reuse. Like LEGO blocks!

Example: `Login.js` is a component that shows a login form

```javascript
function Login() {
  return (
    <div>
      <h2>Login</h2>
      <input type="text" placeholder="Username" />
      <button>Login</button>
    </div>
  );
}
```

### What is State?

**State** is data that changes over time. Like a variable that triggers UI updates.

Example: Storing what the user types in a form

```javascript
const [username, setUsername] = useState('');
// username = current value
// setUsername = function to update it
```

### What is useEffect?

**useEffect** runs code when the component loads or when data changes.

Example: Fetch sessions from Django when page loads

```javascript
useEffect(() => {
  // This runs once when component loads
  fetchSessions();
}, []); // Empty array = run once
```

### What is Routing?

**Routing** changes what page you see without reloading the browser.

Example: Going from `/login` to `/dashboard`

```javascript
<Route path="/login" element={<Login />} />
<Route path="/dashboard" element={<Dashboard />} />
```

---

## 📚 Resources for Learning More

### Official Documentation
- **React:** https://react.dev/learn
- **React Router:** https://reactrouter.com/en/main/start/tutorial
- **Axios:** https://axios-http.com/docs/intro

### Beginner Tutorials
- **React in 100 Seconds:** https://www.youtube.com/watch?v=Tn6-PIqc4UM
- **React Tutorial for Beginners:** https://www.youtube.com/watch?v=SqcY0GlETPk
- **FreeCodeCamp React Course:** https://www.freecodecamp.org/learn/front-end-development-libraries/

---

## 🛠️ Making Changes

### Adding a New Page

1. **Create component file:**
   ```
   src/components/pages/About.js
   ```

2. **Write the component:**
   ```javascript
   function About() {
     return (
       <div className="container">
         <h1>About Us</h1>
         <p>Welcome to our quiz system!</p>
       </div>
     );
   }
   export default About;
   ```

3. **Add route in App.js:**
   ```javascript
   import About from './components/pages/About';
   
   <Route path="/about" element={<About />} />
   ```

4. **Add link in Navbar.js:**
   ```javascript
   <Link to="/about" className="navbar-link">About</Link>
   ```

### Changing Styles

1. **Find the CSS file:** Check `src/styles/` folder
2. **Edit the class:** Change colors, sizes, spacing
3. **Save:** React will auto-reload

Example - Change primary color:
```css
/* In src/styles/index.css */
:root {
  --primary: #3b82f6;  /* Change this blue color */
}
```

---

## 🤝 Getting Help

### If You're Stuck:

1. **Read error messages** - They usually tell you what's wrong
2. **Check the browser console:**
   - Press `F12` in browser
   - Click "Console" tab
   - Look for red error messages
3. **Check PowerShell terminal** - Look for error messages there too
4. **Google the error** - Copy/paste error message into Google
5. **Ask for help** - Provide:
   - What you were trying to do
   - What error you got
   - Screenshot of error message

---

## ✅ Checklist: Is Everything Working?

Use this to verify your setup:

- [ ] Node.js installed (`node --version` works)
- [ ] npm installed (`npm --version` works)
- [ ] Dependencies installed (`node_modules` folder exists)
- [ ] Django backend running on port 8000
- [ ] React frontend running on port 3000
- [ ] Can see homepage in browser
- [ ] Can click "Register" and see registration form
- [ ] Can click "Sessions" and see session list

---

## 📞 Project Information

**Django Backend:** `http://127.0.0.1:8000`
**React Frontend:** `http://localhost:3000`
**API Endpoints:** `http://127.0.0.1:8000/api/`
**Swagger Docs:** `http://127.0.0.1:8000/api/swagger/`

---

## 🎉 You're Ready!

Congratulations! You now have a working React frontend connected to your Django backend. 

**Next steps:**
1. Try registering a new user
2. Browse sessions
3. Register for a session (get session code from Django admin)
4. Take a quiz
5. Submit feedback

**Happy coding! 🚀**
