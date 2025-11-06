"""
Remove all student passwords to make them optional
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from survey.models import Attendee

print("="*70)
print("MAKING ALL PASSWORDS OPTIONAL")
print("="*70)

students = Attendee.objects.all()
updated_count = 0

for student in students:
    if student.password:
        print(f"\n✓ Removing password for: {student.email}")
        print(f"  Name: {student.name}")
        student.password = ""
        student.plain_password = ""
        student.save()
        updated_count += 1
    else:
        print(f"\n- {student.email} (already has no password)")

print("\n" + "="*70)
print(f"COMPLETED: {updated_count} passwords removed")
print("="*70)
print("\nAll students can now login with:")
print("  - Email only (no password required)")
print("  - Or set a new password during next registration")
print("="*70)
