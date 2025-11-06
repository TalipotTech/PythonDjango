"""
Clean migration script from SQLite to Azure PostgreSQL
This handles encoding issues by processing data in Python
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from django.contrib.auth.models import User
from survey.models import Attendee, ClassSession, Question, Response, Review, Admin
import json

print("=" * 60)
print("SQLite to Azure PostgreSQL Migration Script")
print("=" * 60)

# Step 1: Export data from SQLite (currently active)
print("\n📤 Step 1: Exporting data from SQLite...")

data_export = {
    'users': [],
    'attendees': [],
    'sessions': [],
    'questions': [],
    'responses': [],
    'reviews': [],
    'admins': []
}

# Export Users
for user in User.objects.all():
    data_export['users'].append({
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })

# Export Attendees
for attendee in Attendee.objects.all():
    data_export['attendees'].append({
        'name': attendee.name,
        'email': attendee.email,
        'age': attendee.age,
        'place': attendee.place,
        'class_session_id': attendee.class_session_id,
        'password': attendee.password,
        'plain_password': attendee.plain_password,
    })

# Export Sessions
for session in ClassSession.objects.all():
    data_export['sessions'].append({
        'id': session.id,
        'title': session.title,
        'teacher': session.teacher,
        'start_time': str(session.start_time),
        'end_time': str(session.end_time),
        'session_code': session.session_code,
    })

# Export Questions
for question in Question.objects.all():
    data_export['questions'].append({
        'text': question.text[:500],  # Limit length
        'question_type': question.question_type,
        'option1': question.option1,
        'option2': question.option2,
        'option3': question.option3,
        'option4': question.option4,
        'correct_option': question.correct_option,
        'class_session_id': question.class_session_id,
    })

# Export Responses
for response in Response.objects.all():
    data_export['responses'].append({
        'question_id': response.question_id,
        'attendee_id': response.attendee_id,
        'selected_option': response.selected_option,
        'text_response': response.text_response[:500] if response.text_response else None,
    })

# Export Reviews
for review in Review.objects.all():
    data_export['reviews'].append({
        'attendee_id': review.attendee_id,
        'content': review.content[:500] if review.content else None,
        'feedback_type': review.feedback_type,
    })

# Export Admins
for admin in Admin.objects.all():
    data_export['admins'].append({
        'username': admin.username,
        'password': admin.password,
        'email': admin.email,
    })

print(f"✅ Exported:")
print(f"   - {len(data_export['users'])} users")
print(f"   - {len(data_export['attendees'])} attendees")
print(f"   - {len(data_export['sessions'])} sessions")
print(f"   - {len(data_export['questions'])} questions")
print(f"   - {len(data_export['responses'])} responses")
print(f"   - {len(data_export['reviews'])} reviews")
print(f"   - {len(data_export['admins'])} admins")

# Save to JSON file with UTF-8 encoding
with open('clean_migration_data.json', 'w', encoding='utf-8') as f:
    json.dump(data_export, f, ensure_ascii=False, indent=2)

print("\n✅ Data exported to: clean_migration_data.json")
print("\n" + "=" * 60)
print("Next Steps:")
print("1. Uncomment DATABASE_URL in .env file")
print("2. Run: python import_to_azure.py")
print("=" * 60)
