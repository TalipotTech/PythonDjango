from django.core.management.base import BaseCommand, CommandError
from survey.smtp_email import generate_otp, send_session_code_smtp
import os


class Command(BaseCommand):
    help = 'Generate a 6-digit OTP and send it via Gmail SMTP to the specified email address'

    def add_arguments(self, parser):
        parser.add_argument('--email', '-e', required=True, help='Recipient email address')
        parser.add_argument('--sender', '-s', required=False, help='Sender email (overrides SENDER_EMAIL env var)')
        parser.add_argument('--smtp-user', required=False, help='SMTP username (overrides SMTP_USER env var)')
        parser.add_argument('--smtp-password', required=False, help='SMTP password (overrides SMTP_PASSWORD env var)')

    def handle(self, *args, **options):
        recipient = options.get('email')
        sender = options.get('sender') or os.environ.get('SENDER_EMAIL')
        smtp_user = options.get('smtp_user') or os.environ.get('SMTP_USER')
        smtp_password = options.get('smtp_password') or os.environ.get('SMTP_PASSWORD')

        if not recipient:
            raise CommandError('Please provide --email')

        otp = generate_otp(6)
        self.stdout.write(f'Generated OTP: {otp}')

        try:
            ok = send_session_code_smtp(
                recipient_email=recipient,
                otp=otp,
                subject='your session code',
                sender_email=sender,
                smtp_user=smtp_user,
                smtp_password=smtp_password,
            )
            if ok:
                self.stdout.write(self.style.SUCCESS(f'Successfully sent OTP to {recipient}'))
            else:
                self.stdout.write(self.style.ERROR('Failed to send OTP. Check SMTP settings.'))
        except Exception as exc:
            raise CommandError(f'Error sending OTP: {exc}')
