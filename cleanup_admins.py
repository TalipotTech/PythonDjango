"""
Clean up extra admin users - keep only one
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from django.contrib.auth.models import User

print("=" * 60)
print("Admin User Cleanup")
print("=" * 60)

# Show current admin users
print("\n📋 Current Admin Users:")
for user in User.objects.filter(is_superuser=True):
    print(f"   - {user.username} ({user.email})")

print("\n" + "=" * 60)
print("Which admin user do you want to KEEP?")
print("=" * 60)
print("1. admin")
print("2. admin1")
print("3. sandra")
print("4. Admin")
print("5. testadmin")
print("\nEnter the number (1-5): ", end='')

choice = input().strip()

keep_user = {
    '1': 'admin',
    '2': 'admin1',
    '3': 'sandra',
    '4': 'Admin',
    '5': 'testadmin',
}.get(choice)

if not keep_user:
    print("❌ Invalid choice!")
    exit()

print(f"\n✅ Keeping: {keep_user}")
print(f"🗑️  Deleting all other admin users...")

# Delete all other admin users
deleted_count = 0
for user in User.objects.filter(is_superuser=True).exclude(username=keep_user):
    print(f"   ❌ Deleting: {user.username}")
    user.delete()
    deleted_count += 1

print(f"\n✅ Cleanup complete!")
print(f"   - Deleted: {deleted_count} admin users")
print(f"   - Remaining: 1 admin user ({keep_user})")

# Set a new password for the remaining admin
print(f"\n🔐 Setting new password for {keep_user}...")
user = User.objects.get(username=keep_user)
user.set_password('admin123')  # You should change this after login
user.email = user.email if user.email else f"{keep_user}@example.com"
user.save()

print(f"✅ Password set to: admin123")
print(f"\n⚠️  Remember to change the password after logging in!")
print(f"\nLogin at: http://127.0.0.1:8000/admin")
print(f"Username: {keep_user}")
print(f"Password: admin123")
