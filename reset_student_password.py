"""
Reset student password or make password optional
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from survey.models import Attendee
from django.contrib.auth.hashers import make_password

def reset_password(email, new_password=None):
    """
    Reset a student's password
    If new_password is None, removes password requirement
    """
    try:
        student = Attendee.objects.get(email__iexact=email)
        
        if new_password:
            student.password = make_password(new_password)
            print(f"✓ Password updated for {email}")
            print(f"  New password: {new_password}")
        else:
            student.password = ""
            print(f"✓ Password removed for {email}")
            print(f"  User can now login with email only")
        
        student.save()
        return True
        
    except Attendee.DoesNotExist:
        print(f"✗ Student not found: {email}")
        return False

def list_students():
    """List all students"""
    print("\n" + "="*70)
    print("ALL STUDENTS")
    print("="*70)
    
    students = Attendee.objects.all()
    for student in students:
        has_pwd = "Yes (required)" if student.password else "No (optional)"
        print(f"\n{student.name}")
        print(f"  Email: {student.email}")
        print(f"  Password: {has_pwd}")
        print(f"  Session: {student.class_session.title if student.class_session else 'None'}")

if __name__ == "__main__":
    print("="*70)
    print("STUDENT PASSWORD MANAGER")
    print("="*70)
    
    if len(sys.argv) > 1:
        email = sys.argv[1]
        new_password = sys.argv[2] if len(sys.argv) > 2 else None
        
        if new_password:
            print(f"\nSetting password for {email}...")
            reset_password(email, new_password)
        else:
            print(f"\nRemoving password for {email}...")
            reset_password(email, None)
    else:
        list_students()
        
        print("\n" + "="*70)
        print("USAGE:")
        print("="*70)
        print("# Remove password (make login email-only):")
        print("  python reset_student_password.py student@email.com")
        print()
        print("# Set new password:")
        print("  python reset_student_password.py student@email.com newpassword123")
        print()
        print("Examples:")
        print("  python reset_student_password.py sandrasanthosh1426@gmail.com")
        print("  python reset_student_password.py sandrasanthosh1426@gmail.com sandra123")
        print("="*70)
