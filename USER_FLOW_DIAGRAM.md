# User Flow Diagram - Quiz System

## 📊 Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                         HOME PAGE                                │
│                    http://127.0.0.1:8000/                       │
└───────────────┬─────────────────────────┬───────────────────────┘
                │                         │
                │                         │
        ┌───────▼────────┐        ┌──────▼──────┐
        │   REGISTER     │        │    LOGIN    │
        │  New Student   │        │  Returning  │
        └───────┬────────┘        └──────┬──────┘
                │                        │
                │                        │
┌───────────────▼─────────────────────────────────────────────────┐
│              REGISTRATION PAGE                                   │
│           /submit/ (submit.html)                                │
│                                                                  │
│  Fields:                                                         │
│  ✅ Name (required)                                              │
│  ✅ Phone (required)                                             │
│  ✅ Email (required)                                             │
│  ✅ Password (required, min 6 chars)                            │
│                                                                  │
│  ❌ Age (REMOVED)                                                │
│  ❌ Place/City (REMOVED)                                         │
│  ❌ Confirm Email (REMOVED)                                      │
│  ❌ Class Selection (REMOVED - moved to login)                  │
└───────────────┬─────────────────────────────────────────────────┘
                │
                │ Submit Registration
                │
        ┌───────▼────────┐
        │  Registration  │
        │   Complete!    │
        │ Redirect to... │
        └───────┬────────┘
                │
                │
┌───────────────▼─────────────────────────────────────────────────┐
│              STUDENT LOGIN PAGE                                  │
│        /student-login/ (student_login.html)                     │
│                                                                  │
│  Fields:                                                         │
│  ✅ Name (required)                                              │
│  ✅ Password (required)                                          │
│  ✅ Select Class/Session (required) ← NEW LOCATION              │
│                                                                  │
│  System Action:                                                  │
│  - Validates credentials                                         │
│  - Saves selected class to student record                        │
│  - Creates session                                               │
└───────────────┬─────────────────────────────────────────────────┘
                │
                │ Login Success
                │
        ┌───────▼────────┐
        │   Session      │
        │   Created      │
        │ Redirect to... │
        └───────┬────────┘
                │
                │
┌───────────────▼─────────────────────────────────────────────────┐
│              SESSION HOME PAGE (NEW!)                            │
│        /session-home/ (session_home.html)                       │
│                                                                  │
│  Displays:                                                       │
│  - Welcome message with student name                             │
│  - Class title and teacher name                                  │
│  - Session status (one of three)                                 │
└──────────────────────────────────────────────────────────────────┘
                │
                │
        ┌───────▼────────────┐
        │ Check Session Time │
        │  (Server-side)     │
        └───┬────────┬───┬───┘
            │        │   │
    ┌───────┘        │   └─────────┐
    │                │             │
┌───▼────────┐  ┌───▼─────┐  ┌───▼────────┐
│  WAITING   │  │ ACTIVE  │  │  EXPIRED   │
│  Status    │  │ Status  │  │   Status   │
└───┬────────┘  └───┬─────┘  └───┬────────┘
    │               │             │
    │               │             │


┌───▼─────────────────────────────────────────────────────────────┐
│  ⏳ WAITING STATUS                                               │
│                                                                  │
│  "Quiz Not Yet Started"                                          │
│                                                                  │
│  Countdown Display:                                              │
│  ┌──────────────────────────────────────────────────┐          │
│  │  Quiz starts in:                                 │          │
│  │                                                   │          │
│  │    2 Days  │  15 Hours  │  30 Minutes  │  45 Sec │          │
│  │    ─────   │   ─────    │    ─────     │   ───   │          │
│  │      2     │     15     │      30      │    45   │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                  │
│  Session Info:                                                   │
│  📅 Start: October 16, 2025 - 10:00 AM                         │
│  📅 End:   October 16, 2025 - 11:30 AM                         │
│                                                                  │
│  ℹ️ The quiz will be available once session starts             │
│                                                                  │
│  [ View Dashboard ]  [ Logout ]                                 │
└──────────────────────────────────────────────────────────────────┘


┌───▼─────────────────────────────────────────────────────────────┐
│  ✅ ACTIVE STATUS                                                │
│                                                                  │
│  "Quiz is Active Now!"                                           │
│                                                                  │
│  Time Remaining:                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │  Time remaining:                                 │          │
│  │                                                   │          │
│  │    0 Days  │  1 Hour  │  15 Minutes  │  30 Sec   │          │
│  │    ───     │  ─────   │    ─────     │   ───     │          │
│  │     0      │    1     │      15      │    30     │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                  │
│  Session Info:                                                   │
│  📅 Started: October 14, 2025 - 10:00 AM                       │
│  📅 Ends:    October 14, 2025 - 11:30 AM                       │
│                                                                  │
│  ┌────────────────────────────────────┐                        │
│  │     🚀 START QUIZ NOW              │  ← CLICK HERE          │
│  └────────────────────────────────────┘                        │
│                                                                  │
│  ⚠️ Complete the quiz before time runs out!                    │
│                                                                  │
│  [ View Dashboard ]  [ Logout ]                                 │
└─────────────────────┬────────────────────────────────────────────┘
                      │
                      │ Click "Start Quiz Now"
                      │
          ┌───────────▼──────────┐
          │   QUIZ PAGE          │
          │   /quiz/             │
          │  (quiz.html)         │
          │                      │
          │  - Show questions    │
          │  - Answer choices    │
          │  - Submit button     │
          └───────────┬──────────┘
                      │
                      │ Submit Quiz
                      │
          ┌───────────▼──────────┐
          │   THANK YOU PAGE     │
          │   /thank-you/        │
          │  (thank_you.html)    │
          │                      │
          │  - Confirmation      │
          │  - Score (optional)  │
          └──────────────────────┘


┌───▼─────────────────────────────────────────────────────────────┐
│  ⏰ EXPIRED STATUS                                               │
│                                                                  │
│  "Session Expired"                                               │
│                                                                  │
│  No countdown shown                                              │
│                                                                  │
│  Session Info:                                                   │
│  📅 Started: October 14, 2025 - 10:00 AM                       │
│  📅 Ended:   October 14, 2025 - 11:30 AM                       │
│                                                                  │
│  ❌ This session has ended. You can no longer take              │
│     the quiz for this session.                                   │
│                                                                  │
│  Please contact your instructor if you have questions.           │
│                                                                  │
│  [ View Dashboard ]  [ Logout ]                                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Automatic Updates

### Real-time Countdown:
- Updates every **1 second** (JavaScript)
- No page refresh needed for countdown

### Server Sync:
- Page auto-refreshes every **60 seconds**
- Ensures accurate server time sync
- Prevents clock drift issues

### Status Transitions:
```
WAITING → (start_time reached) → ACTIVE
ACTIVE  → (end_time reached)   → EXPIRED
```

---

## 📱 Responsive Design

### Desktop View:
```
┌────────────────────────────────────────┐
│  Large countdown boxes                 │
│  Side-by-side layout                   │
│  Full-width buttons                    │
└────────────────────────────────────────┘
```

### Mobile View:
```
┌──────────────────┐
│  Stacked layout  │
│  Compact boxes   │
│  Touch-friendly  │
│  buttons         │
└──────────────────┘
```

---

## 🎨 Visual States

### Color Coding:
- **🟠 WAITING**: Orange theme (#f57c00)
- **🟢 ACTIVE**: Green theme (#388e3c)
- **🔴 EXPIRED**: Red theme (#d32f2f)

### Icons:
- ⏳ Waiting/Hourglass
- ✅ Active/Check mark
- ⏰ Expired/Clock

---

## 🔐 Security Flow

```
┌────────────────────────────────────┐
│  All Pages Check:                  │
│  - Is attendee_id in session?      │
│  - Is class_session_id in session? │
│  - Are records valid in DB?        │
│                                    │
│  If NO → Redirect to Login         │
│  If YES → Continue                 │
└────────────────────────────────────┘
```

---

## 📊 Database Changes

### Before:
```
Attendee Model:
├── name (required)
├── phone (required)
├── email (required)
├── age (optional)
├── place (optional)
├── class_session (required) ← Changed
└── password (required)
```

### After:
```
Attendee Model:
├── name (required)
├── phone (required)
├── email (required)
├── age (optional, unused)
├── place (optional, unused)
├── class_session (nullable) ← Can be NULL initially
└── password (required)
```

---

## ⚙️ Server-side Logic

### Time Calculation:
```python
now = current server time (timezone aware)
start_time = session.start_time
end_time = session.end_time

if now < start_time:
    status = "waiting"
    countdown = start_time - now

elif start_time <= now <= end_time:
    status = "active"
    countdown = end_time - now

else:
    status = "expired"
    countdown = None
```

---

**Created**: October 14, 2025  
**Version**: 2.0  
**Status**: ✅ Implemented and Running
