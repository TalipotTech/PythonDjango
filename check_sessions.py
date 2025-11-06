#!/usr/bin/env python
"""
Quick script to check session times and status
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from django.utils import timezone
from survey.models import ClassSession

now = timezone.now()
print(f"Current time (UTC): {now}")
print(f"Current time (Local): {timezone.localtime(now)}")
print("\n" + "="*80)

all_sessions = ClassSession.objects.all().order_by('-start_time')

for session in all_sessions:
    print(f"\nSession: {session.title}")
    print(f"  Teacher: {session.teacher}")
    print(f"  Start: {timezone.localtime(session.start_time)}")
    print(f"  End: {timezone.localtime(session.end_time)}")
    
    if session.end_time < now:
        status = "EXPIRED ❌"
    elif session.start_time <= now <= session.end_time:
        status = "ACTIVE ✅"
    elif session.start_time > now:
        status = "UPCOMING 🔵"
    else:
        status = "UNKNOWN ❓"
    
    print(f"  Status: {status}")
    print(f"  Session Code: {session.session_code}")
    print("-" * 80)
