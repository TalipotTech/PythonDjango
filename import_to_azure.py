"""
Import script: Load data from JSON into Azure PostgreSQL
"""

import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from django.contrib.auth.models import User
from survey.models import Attendee, ClassSession, Question, Response, Review, Admin
from django.contrib.auth.hashers import make_password
from datetime import datetime

print("=" * 60)
print("Importing Data to Azure PostgreSQL")
print("=" * 60)

# Load exported data
with open('clean_migration_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"\n📥 Loaded data:")
print(f"   - {len(data['users'])} users")
print(f"   - {len(data['attendees'])} attendees")
print(f"   - {len(data['sessions'])} sessions")
print(f"   - {len(data['questions'])} questions")
print(f"   - {len(data['responses'])} responses")
print(f"   - {len(data['reviews'])} reviews")
print(f"   - {len(data['admins'])} admins")

print("\n🚀 Starting import...")

# Import Users
print("\n1️⃣ Importing Admin Users...")
user_map = {}
for user_data in data['users']:
    try:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'is_staff': user_data['is_staff'],
                'is_superuser': user_data['is_superuser'],
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
            }
        )
        if created:
            # Set a default password (change this later!)
            user.set_password('changeme123')
            user.save()
            print(f"   ✅ Created: {user.username}")
        else:
            print(f"   ⏭️  Exists: {user.username}")
        user_map[user_data['username']] = user.id
    except Exception as e:
        print(f"   ❌ Error with {user_data['username']}: {e}")

# Import Sessions
print("\n2️⃣ Importing Sessions...")
session_map = {}
for i, session_data in enumerate(data['sessions']):
    try:
        session, created = ClassSession.objects.get_or_create(
            session_code=session_data['session_code'],
            defaults={
                'title': session_data['title'],
                'teacher': session_data['teacher'],
                'start_time': session_data['start_time'],
                'end_time': session_data['end_time'],
            }
        )
        if created:
            print(f"   ✅ Created: {session.title}")
        else:
            print(f"   ⏭️  Exists: {session.title}")
        session_map[session_data['id']] = session.id
    except Exception as e:
        print(f"   ❌ Error with session {i}: {e}")

# Import Attendees
print("\n3️⃣ Importing Students...")
attendee_map = {}
for i, attendee_data in enumerate(data['attendees']):
    try:
        # Map old session ID to new session ID
        session_id = session_map.get(attendee_data['class_session_id'])
        
        attendee, created = Attendee.objects.get_or_create(
            email=attendee_data['email'],
            defaults={
                'name': attendee_data['name'],
                'age': attendee_data.get('age'),
                'place': attendee_data.get('place', ''),
                'class_session_id': session_id,
                'password': attendee_data.get('password', ''),
                'plain_password': attendee_data.get('plain_password', ''),
            }
        )
        if created:
            print(f"   ✅ Created: {attendee.name}")
        else:
            print(f"   ⏭️  Exists: {attendee.name}")
        # Store mapping of old ID to new ID (using index as old ID)
        attendee_map[i] = attendee.id
    except Exception as e:
        print(f"   ❌ Error with attendee {i}: {e}")

# Import Questions
print("\n4️⃣ Importing Questions...")
question_map = {}
for i, question_data in enumerate(data['questions']):
    try:
        session_id = session_map.get(question_data['class_session_id'])
        if not session_id:
            print(f"   ⏭️  Skipping question (no session)")
            continue
            
        question = Question.objects.create(
            text=question_data['text'],
            question_type=question_data['question_type'],
            option1=question_data.get('option1'),
            option2=question_data.get('option2'),
            option3=question_data.get('option3'),
            option4=question_data.get('option4'),
            correct_option=question_data.get('correct_option'),
            class_session_id=session_id,
        )
        print(f"   ✅ Created question {i+1}")
        question_map[i] = question.id
    except Exception as e:
        print(f"   ❌ Error with question {i}: {e}")

# Import Responses
print("\n5️⃣ Importing Responses...")
for i, response_data in enumerate(data['responses']):
    try:
        question_id = question_map.get(response_data['question_id'] - 1)  # Adjust for index
        attendee_id = attendee_map.get(response_data['attendee_id'] - 1)
        
        if not question_id or not attendee_id:
            continue
            
        Response.objects.create(
            question_id=question_id,
            attendee_id=attendee_id,
            selected_option=response_data.get('selected_option'),
            text_response=response_data.get('text_response'),
        )
        if (i+1) % 10 == 0:
            print(f"   ✅ Imported {i+1} responses...")
    except Exception as e:
        if i < 5:  # Only show first few errors
            print(f"   ⏭️  Skipping response {i}: {e}")

print(f"   ✅ Total responses imported")

# Import Reviews
print("\n6️⃣ Importing Reviews...")
for i, review_data in enumerate(data['reviews']):
    try:
        attendee_id = attendee_map.get(review_data['attendee_id'] - 1)
        if not attendee_id:
            continue
            
        Review.objects.create(
            attendee_id=attendee_id,
            content=review_data.get('content'),
            feedback_type=review_data.get('feedback_type', 'general'),
        )
        print(f"   ✅ Imported review {i+1}")
    except Exception as e:
        print(f"   ⏭️  Skipping review {i}: {e}")

# Import Admins
print("\n7️⃣ Importing Admins...")
for admin_data in data['admins']:
    try:
        admin, created = Admin.objects.get_or_create(
            username=admin_data['username'],
            defaults={
                'password': admin_data['password'],
                'email': admin_data['email'],
            }
        )
        if created:
            print(f"   ✅ Created: {admin.username}")
        else:
            print(f"   ⏭️  Exists: {admin.username}")
    except Exception as e:
        print(f"   ❌ Error with admin {admin_data['username']}: {e}")

print("\n" + "=" * 60)
print("✅ Migration Complete!")
print("=" * 60)
print("\n📊 Final Counts in Azure PostgreSQL:")
print(f"   - Users: {User.objects.count()}")
print(f"   - Students: {Attendee.objects.count()}")
print(f"   - Sessions: {ClassSession.objects.count()}")
print(f"   - Questions: {Question.objects.count()}")
print(f"   - Responses: {Response.objects.count()}")
print(f"   - Reviews: {Review.objects.count()}")
print(f"   - Admins: {Admin.objects.count()}")
print("\n⚠️  IMPORTANT: Admin user passwords have been reset to 'changeme123'")
print("   Please log in and change them!")
