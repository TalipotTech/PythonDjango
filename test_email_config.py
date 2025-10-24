"""
Quick Email Test Script
-----------------------
This script tests your email configuration to ensure SMTP is working.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings


def test_email_configuration():
    """Test the current email configuration"""
    print("=" * 60)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 60)
    print()
    
    # Check current email backend
    print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
    print()
    
    # Check SMTP settings
    if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
        print("✅ SMTP Backend Configured!")
        print(f"   Host: {getattr(settings, 'EMAIL_HOST', 'NOT SET')}")
        print(f"   Port: {getattr(settings, 'EMAIL_PORT', 'NOT SET')}")
        print(f"   User: {getattr(settings, 'EMAIL_HOST_USER', 'NOT SET')}")
        print(f"   Password: {'*' * 8 if getattr(settings, 'EMAIL_HOST_PASSWORD', '') else 'NOT SET'}")
        print(f"   Use TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}")
        print(f"   Use SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
        print()
        
        # Try sending a test email
        test_email = input("Enter a test email address to send to (or press Enter to skip): ").strip()
        
        if test_email:
            print()
            print(f"📤 Sending test email to {test_email}...")
            try:
                send_mail(
                    subject='Test Email from Quiz Portal',
                    message='This is a test email. If you receive this, your SMTP configuration is working correctly!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[test_email],
                    fail_silently=False,
                )
                print("✅ Email sent successfully!")
                print("   Check your inbox (and spam folder)")
            except Exception as e:
                print(f"❌ Failed to send email:")
                print(f"   Error: {e}")
                print()
                print("Possible issues:")
                print("  1. Check your Gmail App Password is correct")
                print("  2. Ensure 2-Factor Authentication is enabled on your Gmail")
                print("  3. Make sure you're using an App Password, not your regular password")
                print("  4. Check your internet connection")
        
    elif settings.EMAIL_BACKEND == 'django.core.mail.backends.filebased.EmailBackend':
        print("⚠️  File-based Backend (Development Mode)")
        print(f"   Emails are saved to: {getattr(settings, 'EMAIL_FILE_PATH', 'NOT SET')}")
        print()
        print("To enable actual email sending via SMTP:")
        print("  1. Run: setup_smtp.ps1")
        print("  2. Edit the file with your Gmail credentials")
        print("  3. Run it in PowerShell")
        print("  4. Restart your Django server in the same PowerShell window")
    
    else:
        print(f"❓ Unknown backend: {settings.EMAIL_BACKEND}")
    
    print()
    print("=" * 60)
    
    # Check environment variables
    print()
    print("ENVIRONMENT VARIABLES CHECK:")
    print("-" * 60)
    env_vars = ['SMTP_HOST', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASSWORD', 'SENDER_EMAIL']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            if 'PASSWORD' in var:
                print(f"  ✅ {var}: {'*' * 8}")
            else:
                print(f"  ✅ {var}: {value}")
        else:
            print(f"  ❌ {var}: NOT SET")
    print()
    
    if not any(os.environ.get(var) for var in env_vars):
        print("⚠️  No SMTP environment variables found!")
        print("   Run 'setup_smtp.ps1' to configure them.")
    
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_email_configuration()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
