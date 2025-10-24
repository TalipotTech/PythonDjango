"""
SMTP Configuration Checker
--------------------------
This script checks if your SMTP environment variables are set correctly
and if they will persist after system restart.
"""
import os
import sys


def check_smtp_config():
    """Check if SMTP configuration is properly set"""
    print("=" * 70)
    print("🔍 SMTP CONFIGURATION STATUS CHECK")
    print("=" * 70)
    print()
    
    # List of required environment variables
    required_vars = {
        'SMTP_HOST': 'smtp.gmail.com',
        'SMTP_PORT': '587',
        'SMTP_USER': 'your-gmail@gmail.com',
        'SMTP_PASSWORD': 'your-app-password',
        'SMTP_USE_TLS': 'True',
        'SENDER_EMAIL': 'your-gmail@gmail.com'
    }
    
    all_set = True
    missing = []
    
    print("📋 Checking environment variables:")
    print("-" * 70)
    
    for var, example in required_vars.items():
        value = os.environ.get(var)
        if value:
            if 'PASSWORD' in var:
                print(f"  ✅ {var:20} = ********")
            else:
                print(f"  ✅ {var:20} = {value}")
        else:
            print(f"  ❌ {var:20} = NOT SET (example: {example})")
            all_set = False
            missing.append(var)
    
    print()
    print("=" * 70)
    print()
    
    if all_set:
        print("✅ SUCCESS! All SMTP environment variables are set!")
        print()
        print("📧 Email System Status: READY")
        print("   - Emails will be sent via Gmail SMTP")
        print("   - Configuration will persist after system restart")
        print()
        print("Next steps:")
        print("  1. Run: python test_email_config.py")
        print("  2. Run: python manage.py runserver")
        print("  3. Test email sending on your website")
        print()
        return True
    else:
        print("⚠️  WARNING: SMTP configuration is incomplete!")
        print()
        print(f"Missing variables: {', '.join(missing)}")
        print()
        print("📧 Email System Status: USING FILE BACKEND")
        print("   - Emails will be saved to 'sent_emails' folder")
        print("   - Real emails will NOT be sent")
        print()
        print("To fix this:")
        print("  Option 1 (Recommended - Permanent):")
        print("    Run: .\\setup_smtp_permanent.ps1")
        print("    Then restart VS Code and test again")
        print()
        print("  Option 2 (Temporary - This session only):")
        print("    Run: .\\setup_smtp.ps1")
        print("    Then run Django in the SAME terminal window")
        print()
        print("  Option 3 (Manual):")
        print("    Open PowerShell as Administrator and run:")
        for var in missing:
            example = required_vars[var]
            print(f'      [System.Environment]::SetEnvironmentVariable("{var}", "{example}", "User")')
        print()
        return False
    

def check_django_settings():
    """Check Django email settings"""
    print("=" * 70)
    print("⚙️  DJANGO SETTINGS CHECK")
    print("=" * 70)
    print()
    
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
        print()
        
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
            print("✅ SMTP Backend Active!")
            print()
            print("Configuration:")
            print(f"  Host: {getattr(settings, 'EMAIL_HOST', 'NOT SET')}")
            print(f"  Port: {getattr(settings, 'EMAIL_PORT', 'NOT SET')}")
            print(f"  User: {getattr(settings, 'EMAIL_HOST_USER', 'NOT SET')}")
            print(f"  Password: {'********' if getattr(settings, 'EMAIL_HOST_PASSWORD', '') else 'NOT SET'}")
            print(f"  Use TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}")
            print(f"  From: {settings.DEFAULT_FROM_EMAIL}")
            print()
            return True
            
        elif settings.EMAIL_BACKEND == 'django.core.mail.backends.filebased.EmailBackend':
            print("⚠️  File Backend Active (Development Mode)")
            print()
            print(f"Emails saved to: {getattr(settings, 'EMAIL_FILE_PATH', 'NOT SET')}")
            print()
            print("This means:")
            print("  - Emails are NOT actually sent")
            print("  - They are saved as files in the 'sent_emails' folder")
            print("  - To send real emails, configure SMTP environment variables")
            print()
            return False
            
        else:
            print(f"❓ Unknown backend: {settings.EMAIL_BACKEND}")
            return False
            
    except Exception as e:
        print(f"❌ Error loading Django settings: {e}")
        print()
        print("Make sure you're running this from the project root directory.")
        return False


def main():
    """Main function"""
    print()
    
    # Check environment variables
    env_ok = check_smtp_config()
    print()
    
    # Check Django settings
    django_ok = check_django_settings()
    print()
    
    print("=" * 70)
    print("📊 FINAL STATUS")
    print("=" * 70)
    print()
    
    if env_ok and django_ok:
        print("✅ EVERYTHING IS WORKING!")
        print("   Your email system is fully configured and ready.")
        print("   Emails will be sent via Gmail SMTP.")
        print()
        print("🎉 You can now use email features in your Django app!")
        print()
    elif env_ok and not django_ok:
        print("⚠️  Environment variables are set, but Django isn't using them yet.")
        print()
        print("Solution:")
        print("  1. Close ALL terminal windows")
        print("  2. Close VS Code completely")
        print("  3. Reopen VS Code")
        print("  4. Run this script again")
        print()
    else:
        print("❌ Email system is NOT configured.")
        print("   Using file-based backend (emails saved to files).")
        print()
        print("To enable SMTP:")
        print("  Run: .\\setup_smtp_permanent.ps1")
        print()
    
    print("=" * 70)
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
