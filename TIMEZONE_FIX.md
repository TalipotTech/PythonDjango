# Timezone and Countdown Timer Fix

## Problem
The countdown timers on the homepage and session pages were showing incorrect times. Events that should be active were showing as upcoming, and the countdown times were off.

## Root Cause
The issue was mixing timezone-aware and timezone-naive datetime comparisons:
- Database stores times in **UTC** (as it should)
- Settings are configured for **Asia/Kolkata (IST)** timezone (+5:30)
- The code was converting to local time BEFORE comparing, which caused incorrect filtering

## Solution
Changed all view functions to:
1. **Use UTC time for database comparisons** (Django's recommended approach)
2. **Convert to local time ONLY for display** in templates

### Files Modified
- `survey/views.py`:
  - `home()` function - Main homepage
  - `session_confirm()` function - Session confirmation page  
  - `session_home()` function - Student session page

### What Changed

**BEFORE (Incorrect):**
```python
now = timezone.localtime(timezone.now())  # ❌ Local time for comparison
current_sessions = ClassSession.objects.filter(
    start_time__lte=now,  # ❌ Comparing local to UTC
    end_time__gte=now
)
```

**AFTER (Correct):**
```python
now = timezone.now()  # ✅ UTC for comparison
current_sessions = ClassSession.objects.filter(
    start_time__lte=now,  # ✅ Comparing UTC to UTC
    end_time__gte=now
)
# Send local time to template for display only
context = {'now': timezone.localtime(now)}
```

## How It Works Now

1. **Server Side (Python/Django)**:
   - All datetime comparisons use UTC
   - Sessions are correctly identified as current/upcoming/past
   - Countdown seconds are calculated correctly

2. **Client Side (JavaScript)**:
   - JavaScript receives the countdown in seconds
   - Updates every second client-side
   - No timezone issues in browser

3. **Display (Templates)**:
   - Times are converted to IST for display
   - Users see their local time
   - Countdown matches actual time remaining

## Testing

To verify the fix:

1. **Check current time:**
```bash
python manage.py shell -c "from django.utils import timezone; print('UTC:', timezone.now()); print('IST:', timezone.localtime(timezone.now()))"
```

2. **Check session classification:**
- Active sessions: Start time < current time < End time
- Upcoming sessions: Start time > current time
- Past sessions: End time < current time

3. **Verify countdown:**
- Create a session starting in 5 minutes
- Homepage should show it as "Upcoming" with ~5 minute countdown
- At start time, it should automatically move to "Current Events"

## Best Practices Applied

✅ **Always use UTC for storage and comparison**  
✅ **Convert to local timezone only for display**  
✅ **Use Django's timezone utilities consistently**  
✅ **Let JavaScript handle client-side countdown**  

## Related Settings

In `settings.py`:
```python
TIME_ZONE = 'Asia/Kolkata'  # Your local timezone
USE_TZ = True  # Enable timezone support
```

This ensures:
- Database stores UTC
- Django converts for display
- Comparisons work correctly

---

**Date Fixed:** October 24, 2025  
**Status:** ✅ Resolved
