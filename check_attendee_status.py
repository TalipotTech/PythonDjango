import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from survey.models import Attendee, Response

# Get the attendee
att = Attendee.objects.get(email='sandrasanthosh1426@gmail.com')

print(f"\n=== Attendee Status ===")
print(f"Email: {att.email}")
print(f"Current Session ID: {att.class_session_id}")
print(f"Session Title: {att.class_session.title if att.class_session else 'None'}")
print(f"Quiz Submitted: {att.has_submitted}")

# Check all responses
responses = Response.objects.filter(attendee=att).select_related('question__class_session')
print(f"\n=== All Responses ===")
sessions_responded = set()
for resp in responses:
    session_title = resp.question.class_session.title
    sessions_responded.add(session_title)
    
print(f"Sessions with responses: {sessions_responded}")
print(f"Total responses: {responses.count()}")
