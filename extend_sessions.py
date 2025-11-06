import django
import os
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from survey.models import ClassSession
from django.utils import timezone

# Get expired sessions and extend them
sessions_to_extend = ClassSession.objects.filter(id__in=[1, 5, 6])

now = timezone.now()
future_end = now + timedelta(days=3)

print("\n=== Extending Sessions ===")
for session in sessions_to_extend:
    old_end = session.end_time
    session.start_time = now - timedelta(hours=1)  # Started 1 hour ago
    session.end_time = future_end
    session.save()
    print(f"✓ {session.title}: {old_end} → {session.end_time}")

print(f"\n✅ Extended {sessions_to_extend.count()} sessions to end on {future_end}")
