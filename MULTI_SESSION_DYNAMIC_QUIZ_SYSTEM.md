# Multi-Session Quiz System with Dynamic Questions

## 🎯 What Was Implemented

Your quiz system now supports:

### ✅ **Requirement 1: Multiple Subject Quizzes**
- Students can attend quizzes for **multiple subjects** (different sessions)
- Once a student completes a subject quiz, they **cannot retake that specific session**
- Students can attend different sessions without interference

### ✅ **Requirement 2: Dynamic Question Updates**
- Admins can **add new questions** even after students have started/submitted
- Students can **see and answer only the newly added questions**
- **Previous answers are preserved** - no duplication
- Students see pending questions count and progress

---

## 🚀 How It Works Now

### For Students:

#### 1. **Start a Quiz**
- Login and select a session
- See session status and countdown timer
- Click "Start Quiz Now" when active

#### 2. **Answer Questions**
- See progress bar showing answered vs. pending questions
- Answer multiple choice (required) and text (optional) questions
- Submit partial answers

#### 3. **Admin Adds New Questions**
- While student is working or after submission
- Admin adds questions to the session

#### 4. **Student Returns**
- Sees "Continue Quiz" button instead of "Start Quiz"
- Progress shows: "X of Y questions answered (Z pending)"
- Only sees the NEW unanswered questions
- Previous answers are saved and won't be asked again

#### 5. **Complete All Questions**
- Once all questions answered, sees "Quiz Completed!"
- Cannot retake that specific session
- Can still take other sessions (different subjects)

---

## 📊 Real-World Example

### Scenario: Python Programming Course

**Session 1: Python Basics**
- Admin creates session with 10 questions
- Student Sandra logs in, answers all 10 questions
- Sandra's progress: 10/10 (100%) ✅ Completed

**Admin adds 3 more questions to Python Basics**
- New total: 13 questions in session

**Sandra returns to session:**
- Sees message: "You have 3 pending questions"
- Progress: 10/13 (77%) - 3 pending
- Button shows: "Continue Quiz (3 questions remaining)"
- Only sees the 3 NEW questions
- Answers them and completes

**Sandra's final status:**
- Python Basics: 13/13 (100%) ✅ Completed
- Cannot retake Python Basics

**Session 2: Django Framework**
- Admin creates new session with 15 questions
- Sandra can start this fresh (different subject)
- Her Python Basics answers don't interfere

---

## 🔧 Technical Implementation

### New Model: `QuizProgress`

```python
class QuizProgress(models.Model):
    attendee = models.ForeignKey(Attendee)
    class_session = models.ForeignKey(ClassSession)
    last_answered_at = models.DateTimeField(auto_now=True)
    is_fully_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('attendee', 'class_session')
```

**Key Features:**
- **Per-session tracking** - each student+session combination tracked separately
- **Automatic question detection** - dynamically finds unanswered questions
- **Completion status** - marks when all current questions answered

### Methods:

#### `get_answered_question_ids()`
Returns list of question IDs the student has already answered for this session.

#### `get_unanswered_questions()`
Returns QuerySet of questions in this session that student hasn't answered yet.
- Compares ALL questions in session with answered questions
- Returns only the NEW/unanswered ones

#### `get_progress_stats()`
Returns dictionary with:
```python
{
    'total': 13,           # Total questions in session
    'answered': 10,        # Questions student answered
    'pending': 3,          # Questions yet to answer
    'percentage': 76.9     # Completion percentage
}
```

#### `update_completion_status()`
Checks if all questions answered and updates `is_fully_completed` flag.

---

## 📝 Updated Views

### `quiz_view()`

**Old Behavior:**
```python
# Blocked if has_submitted = True (global)
if attendee.has_submitted:
    return already_submitted_page()
```

**New Behavior:**
```python
# Get or create progress for THIS session
quiz_progress, created = QuizProgress.objects.get_or_create(
    attendee=attendee,
    class_session=class_session
)

# Get only unanswered questions
unanswered_questions = quiz_progress.get_unanswered_questions()

# If no unanswered questions, mark complete
if not unanswered_questions.exists():
    quiz_progress.update_completion_status()
    return already_submitted_page()

# Show only unanswered questions
return render('quiz.html', {'questions': unanswered_questions})
```

**Benefits:**
- ✅ Per-session tracking
- ✅ Only shows unanswered questions
- ✅ Handles newly added questions automatically
- ✅ Prevents duplicate answers

### `session_home()`

**New Features:**
- Shows quiz progress stats
- Different buttons based on status:
  - "Start Quiz Now" - if not started (0 answered)
  - "Continue Quiz (X remaining)" - if in progress
  - "Quiz Completed!" - if all answered

**Progress Display:**
```
📊 Your Progress
┌─────────────────────────────────┐
│ Total: 13  Answered: 10  Pending: 3 │
│ [███████████░░░] 76.9%          │
└─────────────────────────────────┘
```

---

## 🎨 UI Updates

### Quiz Page (`quiz.html`)

**Progress Banner:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Progress: 10 of 13 questions answered (3 pending)
[████████████░░░░] 76.9%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Title Changes:**
- If first time: "Answer all questions and submit when ready"
- If continuing: "Continue answering the remaining questions"

### Session Home (`session_home.html`)

**Progress Card:**
Shows three statistics:
1. **Total Questions** - Total in session
2. **Answered** - Questions student completed (green)
3. **Pending** - Questions remaining (orange)

**Dynamic Button:**
- 🚀 "Start Quiz Now" - Fresh start
- ▶️ "Continue Quiz (3 questions remaining)" - In progress
- ✅ "Quiz Completed" + "View Your Results" - Done

---

## 🧪 Testing Scenarios

### Test 1: Basic Flow
1. Admin creates session "Math Quiz" with 5 questions
2. Student John starts quiz, answers all 5
3. ✅ John's progress: 5/5 (100%) - Completed
4. John tries to access quiz again
5. ✅ Sees "Quiz Completed!" message
6. ✅ Cannot answer questions again

### Test 2: Dynamic Questions
1. Admin creates "Science Quiz" with 8 questions
2. Student Mary starts quiz, answers 5 questions
3. Mary's progress: 5/8 (62.5%) - 3 pending
4. **Admin adds 4 more questions** (now 12 total)
5. Mary returns to quiz
6. ✅ Mary's progress: 5/12 (41.7%) - 7 pending
7. ✅ Mary sees only the 7 unanswered questions
8. Mary answers the 7 questions
9. ✅ Mary's progress: 12/12 (100%) - Completed

### Test 3: Multiple Sessions
1. Admin creates two sessions:
   - "Biology" with 10 questions
   - "Chemistry" with 8 questions
2. Student Tom completes Biology (10/10)
3. ✅ Tom cannot retake Biology
4. ✅ Tom can start Chemistry (fresh 0/8)
5. Tom answers 5 Chemistry questions (5/8)
6. ✅ Biology still shows completed (10/10)
7. ✅ Chemistry shows in progress (5/8 - 3 pending)
8. Tom completes remaining Chemistry questions
9. ✅ Both sessions completed, both locked

### Test 4: Mixed Question Types
1. Admin creates "Comprehensive Test":
   - 5 multiple choice questions
   - 3 text response questions
2. Student Sarah answers all 5 MC, skips 2 text questions
3. Sarah's progress: 6/8 (75%) - 2 pending
4. ✅ Score calculated from MC only (e.g., 4/5 = 80%)
5. ✅ Text responses don't affect score
6. Admin adds 2 more MC questions (now 10 total)
7. Sarah returns
8. ✅ Sarah's progress: 6/10 (60%) - 4 pending
9. ✅ Sarah sees: 2 unanswered text + 2 new MC questions
10. Sarah answers all 4, completes quiz

---

## 🎯 Key Benefits

### For Admins:
1. **Flexible question management** - add questions anytime
2. **No disruption to students** - ongoing quizzes not affected
3. **Track progress** - see who completed what
4. **Multiple subjects** - organize by sessions

### For Students:
1. **Resume capability** - can leave and return
2. **See progress** - know how many questions left
3. **Multiple subjects** - take different quizzes
4. **Fair system** - can't retake completed quizzes
5. **New questions** - automatically see additions

### Technical:
1. **Per-session tracking** - isolated by session
2. **Per-question tracking** - no duplicates
3. **Dynamic updates** - handles new questions
4. **Efficient queries** - only fetches unanswered
5. **Clean data model** - easy to understand

---

## 📋 Database Schema

### Before (Old System):
```
Attendee:
  - has_submitted (Boolean) ❌ GLOBAL BLOCK

Problem: Once submitted ANY quiz, blocked from ALL quizzes
```

### After (New System):
```
Attendee:
  - has_submitted (still exists, not actively used)

QuizProgress:
  - attendee_id
  - class_session_id
  - is_fully_completed
  - last_answered_at
  
Response:
  - attendee_id
  - question_id
  - selected_option / text_response
  
✅ Per-session tracking
✅ Per-question responses
✅ Dynamic question detection
```

---

## 🔄 Flow Diagrams

### Student Takes Quiz:
```
Login → Select Session → Session Home
  ↓
Check QuizProgress for this session
  ↓
Not Started (0%) → "Start Quiz Now"
In Progress (X%) → "Continue Quiz (Y pending)"
Completed (100%) → "Quiz Completed!"
  ↓
Click Button → Load Quiz
  ↓
Get Unanswered Questions Only
  ↓
Show Progress Bar + Questions
  ↓
Submit Answers
  ↓
Save Responses (no duplicates)
  ↓
Update QuizProgress
  ↓
Check if More Questions Pending
  ↓
YES → Show "Continue Quiz" button
NO → Mark Completed, Show "Quiz Completed!"
```

### Admin Adds Questions:
```
Admin Dashboard → Select Session
  ↓
View Questions → Add New Question
  ↓
Question Saved to Session
  ↓
Students with Progress < 100%:
  ↓
Automatically see new questions
  ↓
Progress updated (e.g., 10/13 becomes 10/15)
  ↓
"Continue Quiz" button shows new count
  ↓
Student clicks → Sees ONLY new questions
```

---

## 🚨 Important Notes

### What's Changed:
1. ✅ **Per-session tracking** - students can take multiple sessions
2. ✅ **Dynamic questions** - admins can add questions anytime
3. ✅ **Resume capability** - students can continue partial quizzes
4. ✅ **Progress visibility** - students see exactly where they stand
5. ✅ **Prevents duplicates** - can't answer same question twice

### What's Preserved:
1. ✅ **Timer system** - still enforces session time limits
2. ✅ **Flexible questions** - still supports MC and text types
3. ✅ **Scoring logic** - still only counts MC questions
4. ✅ **Admin features** - all CRUD operations still work
5. ✅ **Student dashboard** - still shows results

### Migration:
- New `QuizProgress` model added
- Existing data not affected
- Old `has_submitted` field still exists (for backwards compatibility)
- New logic uses `QuizProgress` instead

---

## ✅ Summary

Your quiz system now fully supports:

### ✅ Requirement 1: Multiple Subjects
- Students can take quizzes for Math, Science, English, etc.
- Completing Math quiz doesn't block Science quiz
- Each session tracked independently

### ✅ Requirement 2: Dynamic Questions
- Admin adds 5 questions, student answers them
- Admin adds 3 more questions
- Student returns, sees ONLY the 3 new questions
- Previous 5 answers preserved
- Progress shows: 5/8 answered, 3 pending

**Result:** Flexible, dynamic, multi-session quiz system that handles everything you requested! 🎉
