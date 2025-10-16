# Quiz Timer & Anti-Cheating Implementation

## ✅ Changes Completed (October 14, 2025)

### Overview
Implemented countdown timer for quizzes and one-time quiz attempt restriction to prevent answer copying and ensure exam integrity.

---

## 🎯 Problems Solved

### 1. **Django Admin Heading Correction** ✅
- **Problem**: Admin page showed "Total attempted" which was misleading
- **Solution**: Changed to "Total Questions" for clarity
- **File**: `survey/admin.py`

**Before:**
```python
list_display = ['name', 'email', 'class_session', 'total_attempted', ...]
def total_attempted(self, obj):
    return Response.objects.filter(attendee=obj).count()
```

**After:**
```python
list_display = ['name', 'email', 'class_session', 'total_questions', ...]
def total_questions(self, obj):
    return Response.objects.filter(attendee=obj).count()
total_questions.short_description = 'Total Questions'
```

---

### 2. **One-Time Quiz Attempt** ✅
- **Problem**: Students could take the same quiz multiple times, allowing them to copy answers
- **Solution**: Implemented strict one-attempt-per-quiz policy
- **Files**: `survey/views.py`, `survey/models.py`

#### Implementation Details:

**Database Field Added:**
```python
# In Attendee model
quiz_started_at = models.DateTimeField(null=True, blank=True)
```

**Quiz View Logic:**
```python
# Check if already submitted - PREVENT RETAKES
if attendee.has_submitted or Response.objects.filter(attendee=attendee).exists():
    return render(request, 'survey/already_submitted.html', {
        'attendee': attendee,
        'class_session': class_session
    })
```

**After Submission:**
```python
if saved_count > 0:
    # Mark as submitted to prevent retakes
    attendee.has_submitted = True
    attendee.save()
```

---

### 3. **Countdown Timer Implementation** ✅
- **Problem**: No time pressure, students could spend unlimited time or look up answers
- **Solution**: Real-time countdown timer that auto-submits when time expires
- **Files**: `survey/views.py`, `survey/templates/survey/quiz.html`

#### Features Implemented:

1. **Visual Timer Display**
   - Shows MM:SS format
   - Updates every second
   - Sticky position (always visible)
   - Color-coded warnings:
     - 🔵 Normal: Purple/Blue gradient
     - 🟠 Warning: Orange (< 5 minutes)
     - 🔴 Critical: Red (< 1 minute)

2. **Automatic Time Tracking**
   ```python
   # Record quiz start time
   if not attendee.quiz_started_at:
       attendee.quiz_started_at = now
       attendee.save()
   
   # Calculate remaining time
   time_elapsed = (now - attendee.quiz_started_at).total_seconds()
   session_duration = (class_session.end_time - class_session.start_time).total_seconds()
   time_remaining = max(0, session_duration - time_elapsed)
   ```

3. **Auto-Submit on Timeout**
   ```javascript
   function updateTimer() {
       if (timeRemaining <= 0) {
           alert('⏰ Time is up! Your quiz will be submitted automatically.');
           quizForm.submit();
           return;
       }
       // Update display...
   }
   ```

4. **Browser Protection**
   - Prevents page refresh during quiz
   - Disables back button
   - Warning on tab close attempt

---

## 🔒 Anti-Cheating Measures

### 1. One-Time Attempt
```
✅ Student can only take quiz ONCE
✅ No retakes allowed
✅ has_submitted flag prevents re-entry
✅ Response records checked for duplicates
```

### 2. Time Pressure
```
✅ Countdown timer creates time pressure
✅ Auto-submit prevents extending time
✅ Timer starts on first page load
✅ Cannot pause or stop timer
```

### 3. Browser Controls
```
✅ Back button disabled during quiz
✅ Page refresh shows warning
✅ Tab close requires confirmation
✅ Cannot navigate away easily
```

### 4. Session Validation
```
✅ Must be within session time window
✅ Start time recorded in database
✅ Cannot restart quiz once started
✅ Time calculated server-side (secure)
```

---

## 📊 User Experience Flow

### Starting Quiz:
```
1. Student logs in and goes to Session Home
2. When session is ACTIVE, clicks "Start Quiz Now"
3. Quiz page loads and timer STARTS immediately
4. quiz_started_at timestamp saved to database
5. Timer displays remaining time
6. Student answers questions under time pressure
```

### During Quiz:
```
- Timer counts down in real-time
- Color changes as time runs low:
  • Normal (Purple) → All good
  • Warning (Orange) → < 5 minutes
  • Critical (Red) → < 1 minute
- Warning messages appear
- Cannot go back or refresh
```

### Quiz Completion:
```
Option A: Student submits manually
  → Answers saved
  → has_submitted = True
  → Redirect to Thank You page

Option B: Time runs out
  → Auto-submit triggered
  → All answered questions saved
  → has_submitted = True
  → Redirect to Already Submitted page
```

### Attempting Again:
```
Student tries to access quiz again
  ↓
System checks:
  - has_submitted flag = True? → BLOCKED
  - Response records exist? → BLOCKED
  ↓
Redirect to Already Submitted page
Shows: "You've already taken this quiz"
```

---

## 🎨 Visual Timer States

### Normal State (Purple)
```css
Background: Purple/Blue gradient
Icon: ⏱️ (animated ticking)
Text: "Time Remaining: MM:SS"
Behavior: Calm, professional
```

### Warning State (Orange)
```css
Background: Orange gradient
Animation: Pulsing
Icon: ⏱️ (faster animation)
Text: "⚠️ Time is running out!"
Trigger: < 5 minutes remaining
```

### Critical State (Red)
```css
Background: Red gradient
Animation: Fast pulsing
Icon: ⏱️ (rapid animation)
Text: "⚠️ Less than 1 minute remaining!"
Trigger: < 1 minute remaining
```

---

## 💾 Database Changes

### New Migration: `0007_attendee_quiz_started_at.py`

```python
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='attendee',
            name='quiz_started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
```

### Updated Fields:
```
Attendee Model:
├── quiz_started_at (DateTime, nullable) ← NEW
├── has_submitted (Boolean) ← Enforced
└── ... (other fields)
```

---

## 🔧 Technical Implementation

### Timer Calculation (Server-side):
```python
# Get times
now = timezone.localtime(timezone.now())
start = attendee.quiz_started_at
session_duration = (session.end_time - session.start_time).total_seconds()

# Calculate remaining
time_elapsed = (now - start).total_seconds()
time_remaining = max(0, session_duration - time_elapsed)

# Check if expired
if time_remaining <= 0:
    attendee.has_submitted = True
    attendee.save()
    # Redirect to already submitted
```

### Timer Update (Client-side):
```javascript
let timeRemaining = {{ time_remaining_seconds }};

function updateTimer() {
    if (timeRemaining <= 0) {
        quizForm.submit();  // Auto-submit
        return;
    }
    
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    
    // Update display
    minutesDisplay.textContent = minutes.toString().padStart(2, '0');
    secondsDisplay.textContent = seconds.toString().padStart(2, '0');
    
    timeRemaining--;
}

setInterval(updateTimer, 1000);  // Update every second
```

---

## 📋 Testing Checklist

### Admin Interface:
- [ ] Login to Django admin
- [ ] Go to Survey → Attendees
- [ ] Verify column header shows "Total Questions" (not "Total attempted")
- [ ] Check that Total Questions, Total Correct, and Score % display correctly

### Quiz Timer:
- [ ] Login as student
- [ ] Start quiz when session is active
- [ ] Verify timer starts immediately
- [ ] Check timer counts down every second
- [ ] Verify color changes at 5 minutes (orange)
- [ ] Verify color changes at 1 minute (red)
- [ ] Try to refresh page - should show warning
- [ ] Try to go back - should be prevented
- [ ] Let timer expire - should auto-submit

### One-Time Attempt:
- [ ] Take quiz and submit
- [ ] Try to access quiz page again
- [ ] Should see "Already Submitted" message
- [ ] Verify can't retake quiz
- [ ] Check database - has_submitted should be True
- [ ] Check Response records exist

### Edge Cases:
- [ ] Try accessing quiz before start time
- [ ] Try accessing quiz after end time
- [ ] Try accessing quiz without login
- [ ] Close browser mid-quiz, reopen - timer should continue
- [ ] Multiple tabs - both should show same countdown

---

## ⚠️ Important Notes

### For Administrators:
1. **Session Duration = Quiz Time**: The quiz duration equals the session duration (end_time - start_time)
2. **No Pause**: Once started, timer cannot be paused
3. **Server Time**: All calculations use server time (secure, can't be manipulated)
4. **Automatic Enforcement**: System automatically prevents retakes

### For Students:
1. **One Attempt Only**: You get ONE chance to take each quiz
2. **Time Starts Immediately**: Timer begins when quiz page loads
3. **Auto-Submit**: Quiz submits automatically when time expires
4. **No Going Back**: Cannot navigate away or refresh during quiz
5. **Answer All**: Make sure to answer all questions before time runs out

### For Instructors:
1. **Set Appropriate Duration**: Make sure session duration allows enough time
2. **Test First**: Create a test session and take the quiz yourself
3. **Monitor**: Check Django admin to see who has submitted
4. **No Resets**: Once submitted, students cannot retake (contact admin if needed)

---

## 📈 Benefits

### Academic Integrity:
✅ Prevents answer copying from multiple attempts  
✅ Creates time pressure similar to real exams  
✅ Discourages looking up answers  
✅ Ensures fair testing conditions  

### User Experience:
✅ Clear visual feedback with countdown  
✅ Color-coded warnings  
✅ Professional exam-like interface  
✅ Automatic submission (no lost submissions)  

### Administrative:
✅ No manual monitoring needed  
✅ Automatic enforcement  
✅ Clear records in database  
✅ Better admin interface labels  

---

## 🚀 Future Enhancements (Optional)

1. **Question Randomization**: Show questions in random order
2. **Option Shuffling**: Shuffle answer options per student
3. **Question Pool**: Random selection from larger question bank
4. **Proctoring**: Webcam monitoring (advanced)
5. **Tab Switching Detection**: Track when student switches tabs
6. **Copy-Paste Prevention**: Disable copy-paste in quiz
7. **Custom Time Limits**: Per-question time limits
8. **Grace Period**: Allow 30 seconds after time expires
9. **Pause Button**: For emergencies (admin approval required)
10. **Attempt History**: Show past attempts with timestamps

---

## 📁 Files Modified

1. ✅ `survey/admin.py` - Changed column heading
2. ✅ `survey/models.py` - Added quiz_started_at field
3. ✅ `survey/views.py` - Implemented timer and one-attempt logic
4. ✅ `survey/templates/survey/quiz.html` - Added timer UI
5. ✅ `survey/templates/survey/already_submitted.html` - Improved message
6. ✅ `survey/migrations/0007_attendee_quiz_started_at.py` - NEW migration

---

## ✅ Status

**Implementation**: ✅ Complete  
**Migrations**: ✅ Applied  
**Testing**: ⏳ Ready for testing  
**Server**: ✅ Running  

---

**Implemented By**: AI Assistant  
**Date**: October 14, 2025  
**Version**: 3.0  
**Status**: Ready for Production Testing
