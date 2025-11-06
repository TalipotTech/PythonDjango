"""
Check student passwords
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from survey.models import Attendee
from django.contrib.auth.hashers import check_password

print("=== All Students ===")
students = Attendee.objects.all()

for student in students:
    print(f"\nEmail: {student.email}")
    print(f"  Name: {student.name}")
    print(f"  Phone: {student.phone}")
    print(f"  Session: {student.class_session.title if student.class_session else 'None'}")
    
    if student.password:
        # Check if password is hashed or plaintext
        if student.password.startswith('pbkdf2_') or student.password.startswith('argon2$'):
            print(f"  Password: (hashed - likely set during registration)")
        else:
            print(f"  Password: {student.password} (plaintext)")
    else:
        print(f"  Password: (not set - can login with email only)")

print("\n" + "="*50)
print("To login, use:")
print("  - Email + Password (if password is shown)")
print("  - Email only (if password is not set)")
print("="*50)
