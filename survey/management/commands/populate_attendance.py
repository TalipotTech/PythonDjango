"""
Management command to populate SessionAttendance records for existing attendees
"""
from django.core.management.base import BaseCommand
from survey.models import Attendee, SessionAttendance


class Command(BaseCommand):
    help = 'Create SessionAttendance records for all existing attendees based on their current class_session'

    def handle(self, *args, **options):
        attendees = Attendee.objects.filter(class_session__isnull=False)
        created_count = 0
        skipped_count = 0
        
        self.stdout.write(self.style.SUCCESS(f'Found {attendees.count()} attendees with sessions'))
        
        for attendee in attendees:
            # Check if attendance record already exists
            attendance, created = SessionAttendance.objects.get_or_create(
                attendee=attendee,
                class_session=attendee.class_session,
                defaults={'has_submitted': attendee.has_submitted}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created attendance: {attendee.name} → {attendee.class_session.title}'
                    )
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'⊗ Already exists: {attendee.name} → {attendee.class_session.title}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Done!'))
        self.stdout.write(self.style.SUCCESS(f'   Created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'   Skipped: {skipped_count}'))
