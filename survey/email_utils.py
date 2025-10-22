"""
Email utility functions for sending session codes and notifications
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_session_code_email(email, name, session_code, session_title, teacher):
    """
    Send session code to participant via email
    """
    subject = f'Your Session Code for {session_title}'
    attendee_email = email
    attendee_name = name
    session_teacher = teacher
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">Welcome to Quiz Portal!</h1>
            </div>
            
            <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #667eea;">Hello {attendee_name}! 👋</h2>
                
                <p>Thank you for registering for the quiz session:</p>
                
                <div style="background: #f0f4ff; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0;">
                    <h3 style="margin: 0 0 10px 0; color: #667eea;">📚 {session_title}</h3>
                    <p style="margin: 5px 0;"><strong>Teacher:</strong> {session_teacher}</p>
                </div>
                
                <p>Your unique session code is:</p>
                
                <div style="background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%); padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0;">
                    <h1 style="color: white; margin: 0; font-size: 36px; letter-spacing: 5px; font-family: 'Courier New', monospace;">
                        🔑 {session_code}
                    </h1>
                </div>
                
                <div style="background: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>⚠️ Important:</strong> Keep this code safe! You'll need it to join the quiz session.</p>
                </div>
                
                <h3 style="color: #667eea;">How to Join:</h3>
                <ol style="line-height: 1.8;">
                    <li>Go to the Quiz Portal homepage</li>
                    <li>Click on "Join with Session Code"</li>
                    <li>Enter your session code: <strong>{session_code}</strong></li>
                    <li>Login with your credentials</li>
                    <li>Start your quiz!</li>
                </ol>
                
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">
                
                <p style="color: #666; font-size: 14px;">
                    If you didn't register for this quiz, please ignore this email or contact the administrator.
                </p>
                
                <p style="color: #666; font-size: 14px;">
                    Best regards,<br>
                    <strong>Quiz Portal Team</strong>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
Hello {attendee_name}!

Thank you for registering for the quiz session:
📚 {session_title}
Teacher: {session_teacher}

Your unique session code is: {session_code}

How to Join:
1. Go to the Quiz Portal homepage
2. Click on "Join with Session Code"
3. Enter your session code: {session_code}
4. Login with your credentials
5. Start your quiz!

⚠️ Important: Keep this code safe! You'll need it to join the quiz session.

If you didn't register for this quiz, please ignore this email.

Best regards,
Quiz Portal Team
    """
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [attendee_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_welcome_email(email, name):
    """
    Send welcome email to new participant
    """
    subject = 'Welcome to Quiz Portal!'
    attendee_email = email
    attendee_name = name
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px;">
                <h1 style="color: white; margin: 0;">Welcome to Quiz Portal! 🎉</h1>
            </div>
            
            <div style="padding: 30px; background: white;">
                <h2 style="color: #667eea;">Hello {attendee_name}!</h2>
                
                <p>Thank you for registering with Quiz Portal. Your account has been created successfully!</p>
                
                <p>You can now:</p>
                <ul>
                    <li>Join quiz sessions using session codes</li>
                    <li>Take quizzes and track your progress</li>
                    <li>View your dashboard and results</li>
                </ul>
                
                <p>We're excited to have you on board!</p>
                
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>Quiz Portal Team</strong>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
Hello {attendee_name}!

Thank you for registering with Quiz Portal. Your account has been created successfully!

You can now:
- Join quiz sessions using session codes
- Take quizzes and track your progress
- View your dashboard and results

We're excited to have you on board!

Best regards,
Quiz Portal Team
    """
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [attendee_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
