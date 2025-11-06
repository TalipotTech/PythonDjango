"""
Quick script to view data from Azure PostgreSQL database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from survey.models import Student, Session, Question, Response, Attendance
from django.contrib.auth.models import User

print("=" * 60)
print("DATABASE OVERVIEW - Azure PostgreSQL")
print("=" * 60)

# Count records
print(f"\n📊 Record Counts:")
print(f"   Users: {User.objects.count()}")
print(f"   Students: {Student.objects.count()}")
print(f"   Sessions: {Session.objects.count()}")
print(f"   Questions: {Question.objects.count()}")
print(f"   Responses: {Response.objects.count()}")
print(f"   Attendance: {Attendance.objects.count()}")

# Show recent students
print(f"\n👥 Recent Students:")
for student in Student.objects.all()[:5]:
    print(f"   - {student.first_name} {student.last_name} ({student.email})")

# Show active sessions
print(f"\n📅 Active Sessions:")
for session in Session.objects.filter(is_active=True)[:5]:
    print(f"   - {session.name} (Code: {session.session_code})")
    print(f"     Start: {session.start_time}, End: {session.end_time}")

# Show recent responses
print(f"\n💬 Recent Responses:")
for response in Response.objects.all().order_by('-submitted_at')[:5]:
    print(f"   - Student: {response.student.email}")
    print(f"     Question: {response.question.text[:50]}...")
    print(f"     Answer: {response.answer_text[:50] if response.answer_text else 'N/A'}")
    print()

print("=" * 60)
print("✅ Database connected successfully!")
print("=" * 60)
