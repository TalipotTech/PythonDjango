"""
Create a test student for testing login
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from survey.models import Attendee, ClassSession
from django.contrib.auth.hashers import make_password

# Check existing students
print("=== Existing Students ===")
students = Attendee.objects.all()[:10]
if students:
    for student in students:
        print(f"  Email: {student.email}")
        print(f"    Name: {student.name}")
        print(f"    Has Password: {'Yes' if student.password else 'No'}")
        print(f"    Session: {student.class_session.title if student.class_session else 'None'}")
        print()
else:
    print("  No students found")
    print()

# Get first session
session = ClassSession.objects.first()
if not session:
    print("No session found. Creating one...")
    session = ClassSession.objects.create(
        title="Test Session",
        teacher="Test Teacher",
        session_code="TEST123"
    )
    print(f"Created session: {session.title} with code {session.session_code}")
    print()
else:
    print(f"Using existing session: {session.title} ({session.session_code})")
    print()

# Create test student
email = "test@student.com"
try:
    student = Attendee.objects.get(email=email)
    print(f"Student {email} already exists")
except Attendee.DoesNotExist:
    student = Attendee.objects.create(
        name="Test Student",
        email=email,
        phone="1234567890",
        age=25,
        place="Test City",
        password=make_password("password123"),  # Hashed password
        class_session=session
    )
    print(f"Created test student: {email}")
    print(f"  Password: password123")
    print(f"  Session: {session.title} ({session.session_code})")

# Also create one without password
email2 = "nopass@student.com"
try:
    student2 = Attendee.objects.get(email=email2)
    print(f"Student {email2} already exists")
except Attendee.DoesNotExist:
    student2 = Attendee.objects.create(
        name="No Password Student",
        email=email2,
        phone="9876543210",
        age=30,
        place="Test City",
        password="",  # No password
        class_session=session
    )
    print(f"\nCreated test student without password: {email2}")
    print(f"  Password: (none)")
    print(f"  Session: {session.title} ({session.session_code})")

print("\n=== Test Students Summary ===")
print(f"1. Email: test@student.com")
print(f"   Password: password123")
print(f"   Can login with email and password")
print()
print(f"2. Email: nopass@student.com")
print(f"   Password: (none)")
print(f"   Can login with email only")
