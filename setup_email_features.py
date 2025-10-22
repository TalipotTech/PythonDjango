"""
Quick setup script for email integration and auto-fill features
Run this after updating models.py
"""

import os
import sys

print("=" * 60)
print("🚀 Email Integration & Auto-Fill Setup")
print("=" * 60)
print()

# Check if we're in the right directory
if not os.path.exists('manage.py'):
    print("❌ Error: Please run this script from the project root directory")
    print("   (where manage.py is located)")
    sys.exit(1)

print("✅ Found manage.py")
print()

print("📋 Setup Steps:")
print()
print("Step 1: Create Migrations")
print("-" * 40)
print("Running: python manage.py makemigrations")
os.system('python manage.py makemigrations')
print()

response = input("⚠️  Did migrations complete successfully? (y/n): ")
if response.lower() != 'y':
    print()
    print("🔧 Troubleshooting:")
    print("   - If you see 'duplicate key' errors, you have duplicate emails/phones")
    print("   - Solution 1 (Fresh start): Delete db.sqlite3 and run again")
    print("   - Solution 2: Clean duplicates (see EMAIL_AUTOFILL_IMPLEMENTATION.md)")
    sys.exit(1)

print()
print("Step 2: Apply Migrations")
print("-" * 40)
print("Running: python manage.py migrate")
os.system('python manage.py migrate')
print()

response = input("✅ Did migration complete successfully? (y/n): ")
if response.lower() != 'y':
    print()
    print("🔧 Please check the error messages above")
    sys.exit(1)

print()
print("=" * 60)
print("✅ Setup Complete!")
print("=" * 60)
print()
print("📧 Next Steps:")
print()
print("1. Configure Email Backend:")
print("   Edit questionnaire_project/settings.py")
print("   Uncomment Gmail settings and add your credentials")
print()
print("2. Test Auto-Fill:")
print("   - Run: python manage.py runserver")
print("   - Register a user")
print("   - Try registering again with same email/phone")
print("   - Watch fields auto-fill!")
print()
print("3. Test Email Sending:")
print("   - For now, emails print to console")
print("   - Check terminal output when registering")
print()
print("📖 Full Documentation:")
print("   See EMAIL_AUTOFILL_IMPLEMENTATION.md")
print()
print("🎉 Happy Coding!")
