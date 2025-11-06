"""
Display all sessions with their codes for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from survey.models import ClassSession

print("="*60)
print("ALL SESSIONS WITH CODES")
print("="*60)

sessions = ClassSession.objects.all().order_by('title')

for session in sessions:
    print(f"\nSession: {session.title}")
    print(f"  Teacher: {session.teacher}")
    print(f"  Code: {session.session_code}")
    print(f"  ID: {session.id}")
    print(f"  Start: {session.start_time}")
    print(f"  End: {session.end_time}")

print("\n" + "="*60)
print("TESTING INSTRUCTIONS:")
print("="*60)
print("1. Go to React app (http://localhost:3000)")
print("2. Click on a session (e.g., 'Django Intro')")
print("3. Enter email and request code")
print("4. Enter the CORRECT code for that session")
print("5. Try entering a WRONG code (from different session)")
print("6. You should see: 'This code is for a different session'")
print("="*60)
