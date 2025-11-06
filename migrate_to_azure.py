"""
Script to migrate data from SQLite to Azure PostgreSQL
Run this if you want to transfer existing data
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

print("=" * 50)
print("Data Migration: SQLite → Azure PostgreSQL")
print("=" * 50)

# Step 1: Check current database
from django.conf import settings
current_db = settings.DATABASES['default']['ENGINE']
print(f"\nCurrently using: {current_db}")

if 'postgresql' in current_db:
    print("\n✅ Connected to Azure PostgreSQL")
    print("\nTo migrate data from SQLite:")
    print("1. Temporarily comment out DATABASE_URL in .env")
    print("2. Run: python manage.py dumpdata > sqlite_backup.json")
    print("3. Uncomment DATABASE_URL in .env")
    print("4. Run: python manage.py loaddata sqlite_backup.json")
else:
    print("\n✅ Connected to SQLite")
    print("Exporting data...")
    os.system('python manage.py dumpdata > sqlite_backup.json')
    print("\n✅ Data exported to sqlite_backup.json")
    print("\nNext steps:")
    print("1. Add DATABASE_URL to .env")
    print("2. Run: python manage.py loaddata sqlite_backup.json")
