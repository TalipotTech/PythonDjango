# Script to create a sample admin user
from django.contrib.auth.hashers import make_password
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from survey.models import Admin

# Create admin user if not exists
username = "admin"
password = "admin123"
email = "admin@example.com"

if not Admin.objects.filter(username=username).exists():
    admin = Admin.objects.create(
        username=username,
        password=make_password(password),
        email=email
    )
    print(f"✅ Admin user created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")
else:
    print(f"⚠️ Admin user '{username}' already exists")
