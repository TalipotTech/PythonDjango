# Quick Testing Guide: Multi-Session Dynamic Quiz System

## 🧪 How to Test the New Features

### Test 1: Multiple Sessions (Different Subjects)

**Steps:**
1. **As Admin:**
   - Login to admin dashboard
   - Create Session 1: "Python Basics" (start now, end +2 hours)
   - Add 5 questions to Python Basics
   - Create Session 2: "Django Framework" (start now, end +2 hours)
   - Add 5 questions to Django Framework

2. **As Student (Sandra):**
   - Register/Login
   - Select "Python Basics" session
   - Start quiz, answer all 5 questions
   - Submit
   - ✅ **Check:** See "Quiz Completed!" message
   - Return to session home
   - ✅ **Check:** Button should show "Quiz Completed!"
   - ✅ **Check:** Progress shows 5/5 (100%)

3. **Switch to Another Session:**
   - Logout and login again
   - Select "Django Framework" session
   - ✅ **Check:** Shows "Start Quiz Now" (not blocked by Python completion)
   - Start quiz, answer all 5 questions
   - Submit
   - ✅ **Check:** Both sessions can be completed independently

**Expected Result:** ✅ Student can complete multiple sessions without interference

---

### Test 2: Dynamic Questions (Admin Adds Questions)

**Steps:**
1. **Setup (As Admin):**
   - Create Session: "Science Quiz" (start now, end +2 hours)
   - Add 8 questions

2. **Student Starts Quiz:**
   - Login as student (John)
   - Select "Science Quiz"
   - ✅ **Check:** Session home shows 0/8 (0%)
   - Start quiz
   - Answer only 5 out of 8 questions
   - Submit
   - ✅ **Check:** Progress shows 5/8 (62.5%) - 3 pending

3. **Admin Adds More Questions:**
   - As admin, go to "Science Quiz"
   - Add 4 more questions
   - ✅ **Check:** Session now has 12 total questions

4. **Student Returns:**
   - As John, go back to "Science Quiz" session home
   - ✅ **Check:** Progress now shows 5/12 (41.7%) - 7 pending
   - ✅ **Check:** Button shows "Continue Quiz (7 questions remaining)"
   - Click Continue Quiz
   - ✅ **Check:** Only sees 7 unanswered questions (not the 5 already answered)
   - Answer all 7 questions
   - Submit
   - ✅ **Check:** Progress shows 12/12 (100%) - Completed

**Expected Result:** ✅ Student can answer newly added questions without re-answering previous ones

---

### Test 3: Resume Partial Quiz

**Steps:**
1. **As Admin:**
   - Create Session: "Math Test" with 10 questions

2. **As Student (Mary):**
   - Start "Math Test"
   - Answer 6 questions
   - **Close browser / logout** (simulate interruption)

3. **Return Later:**
   - Login again as Mary
   - Go to "Math Test" session home
   - ✅ **Check:** Progress shows 6/10 (60%) - 4 pending
   - ✅ **Check:** Button shows "Continue Quiz (4 questions remaining)"
   - Click Continue
   - ✅ **Check:** Sees only 4 unanswered questions
   - Complete remaining 4 questions
   - ✅ **Check:** Progress shows 10/10 (100%) - Completed

**Expected Result:** ✅ Student can resume quiz from where they left off

---

### Test 4: Cannot Retake Completed Quiz

**Steps:**
1. **As Student:**
   - Complete a quiz (answer all questions)
   - ✅ **Check:** See "Quiz Completed!" message
   - Try to access quiz again
   - ✅ **Check:** See "Quiz Completed!" message (not quiz page)
   - ✅ **Check:** No way to retake or re-answer questions

**Expected Result:** ✅ Completed quizzes are locked

---

### Test 5: Mixed Question Types with Dynamic Addition

**Steps:**
1. **As Admin:**
   - Create Session: "Comprehensive Test"
   - Add 3 multiple choice questions
   - Add 2 text response questions

2. **As Student:**
   - Start quiz
   - Answer all 3 MC questions
   - Answer 1 text question, skip 1 text question
   - Submit
   - ✅ **Check:** Progress shows 4/5 (80%) - 1 pending

3. **Admin Adds More:**
   - Add 2 more MC questions
   - Add 1 more text question
   - ✅ **Check:** Total now 8 questions

4. **Student Returns:**
   - ✅ **Check:** Progress shows 4/8 (50%) - 4 pending
   - Click Continue Quiz
   - ✅ **Check:** Sees 4 unanswered questions:
     - 1 text (the one skipped before)
     - 2 MC (newly added)
     - 1 text (newly added)
   - Answer all 4
   - ✅ **Check:** Progress shows 8/8 (100%) - Completed
   - ✅ **Check:** Score calculated from MC only (not text responses)

**Expected Result:** ✅ Mixed question types work with dynamic additions

---

### Test 6: Progress Bar Accuracy

**Steps:**
1. Create session with 10 questions
2. Student answers 3 questions
3. ✅ **Check Progress Bar:**
   - Shows "3 of 10 questions answered (7 pending)"
   - Visual bar shows 30%
   - Stats show: Total: 10, Answered: 3, Pending: 7

4. Admin adds 5 more questions (now 15 total)
5. Student refreshes/returns
6. ✅ **Check Updated Progress:**
   - Shows "3 of 15 questions answered (12 pending)"
   - Visual bar shows 20%
   - Stats show: Total: 15, Answered: 3, Pending: 12

7. Student answers 7 more (now 10 total answered)
8. ✅ **Check Progress:**
   - Shows "10 of 15 questions answered (5 pending)"
   - Visual bar shows 66.7%
   - Stats show: Total: 15, Answered: 10, Pending: 5

**Expected Result:** ✅ Progress bar accurately reflects current status

---

## 🎯 Quick Verification Checklist

### Multiple Sessions:
- [ ] Student can complete Session A
- [ ] Student can then start Session B
- [ ] Completing Session A doesn't block Session B
- [ ] Each session shows independent progress

### Dynamic Questions:
- [ ] Admin can add questions to existing session
- [ ] Student sees updated total question count
- [ ] Student sees only unanswered questions
- [ ] Previous answers are preserved
- [ ] Progress updates correctly

### Resume Capability:
- [ ] Student can answer partial quiz
- [ ] Student can logout/close browser
- [ ] Student can return and continue
- [ ] Only unanswered questions shown
- [ ] Progress maintained across sessions

### Completion Lock:
- [ ] Completed quiz shows "Quiz Completed!"
- [ ] Cannot access quiz page when completed
- [ ] Progress shows 100%
- [ ] Button shows "View Your Results"

### UI Elements:
- [ ] Progress bar displays correctly
- [ ] "Start Quiz Now" for fresh sessions
- [ ] "Continue Quiz (X remaining)" for partial
- [ ] "Quiz Completed!" for finished
- [ ] Pending count updates dynamically

---

## 💡 Testing Tips

### Tip 1: Use Multiple Browser Profiles
- Admin in regular window
- Student in incognito/private window
- Easy to switch between roles

### Tip 2: Check Database
```bash
python manage.py shell
```
```python
from survey.models import QuizProgress, Response
# Check progress records
QuizProgress.objects.all()
# Check responses
Response.objects.all()
```

### Tip 3: Monitor Progress
- Watch the progress bar update
- Check pending count decreases
- Verify percentages calculate correctly

### Tip 4: Test Edge Cases
- Add question while student is taking quiz
- Add question after student submitted
- Student answers some, admin adds more
- Multiple students, different progress

---

## 🐛 Common Issues & Solutions

### Issue: Progress not updating
**Solution:** Refresh the session home page

### Issue: Seeing already answered questions
**Solution:** Check Response model for duplicates

### Issue: Progress shows wrong percentage
**Solution:** Verify total question count in session

### Issue: Can still access completed quiz
**Solution:** Check `is_fully_completed` flag in QuizProgress

---

## ✅ Success Criteria

All these should work:
1. ✅ Multiple sessions tracked independently
2. ✅ Dynamic questions show up for students
3. ✅ Only unanswered questions displayed
4. ✅ Progress tracks accurately
5. ✅ Cannot retake completed quizzes
6. ✅ Can resume partial quizzes
7. ✅ UI shows correct button labels
8. ✅ Progress bar reflects current status

---

## 🎉 You're Ready!

The system now supports:
- **Multiple subject quizzes** - Take Math, Science, English separately
- **Dynamic questions** - Admin can add anytime, students see them
- **Resume capability** - Never lose progress
- **Fair system** - No retakes, no duplicates
- **Clear visibility** - Always know your progress

**Test it out and enjoy the new features!** 🚀
