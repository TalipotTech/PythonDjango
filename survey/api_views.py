"""
API views for AJAX requests
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import Attendee, ClassSession
import json


@require_http_methods(["POST"])
def check_participant_exists(request):
    """
    Check if participant exists by email or phone and return their details for auto-fill
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()

        attendee = None

        # Try to find by email first
        if email:
            try:
                attendee = Attendee.objects.get(email__iexact=email)
            except Attendee.DoesNotExist:
                pass

        # If not found by email, try phone
        if not attendee and phone:
            try:
                attendee = Attendee.objects.get(phone=phone)
            except Attendee.DoesNotExist:
                pass

        if attendee:
            return JsonResponse({
                'exists': True,
                'data': {
                    'name': attendee.name,
                    'email': attendee.email,
                    'phone': attendee.phone,
                    'age': attendee.age,
                    'place': attendee.place,
                }
            })
        else:
            return JsonResponse({
                'exists': False,
                'message': 'No existing participant found. Please fill in all details.'
            })

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def send_session_code_email(request):
    """
    Send session code to user's email
    Request body: { "email": "user@example.com", "session_code": "ABC12345" }
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        session_code = data.get('session_code', '').strip()

        if not email or not session_code:
            return JsonResponse({
                'success': False,
                'message': 'Email and session code are required.'
            }, status=400)

        # Verify session code exists
        try:
            session = ClassSession.objects.get(session_code=session_code)
        except ClassSession.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid session code.'
            }, status=404)

        # Send email
        subject = f'Your Session Code for {session.title}'
        message = f"""
Hello,

You requested to join the session: {session.title}
Teacher: {session.teacher}

Your session code is: {session_code}

Please use this code to complete your registration.

Best regards,
Workshop Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return JsonResponse({
            'success': True,
            'message': f'Session code sent to {email}'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error sending email: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def verify_session_code_with_email(request):
    """
    Verify session code and check if user is new or existing
    Request body: { 
        "email": "user@example.com", 
        "session_code": "ABC12345",
        "expected_session_id": 1  (optional - to validate against specific session)
    }
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        session_code = data.get('session_code', '').strip()
        expected_session_id = data.get('expected_session_id')  # Optional

        if not email or not session_code:
            return JsonResponse({
                'valid': False,
                'message': 'Email and session code are required.'
            }, status=400)

        # Verify session code exists
        try:
            session = ClassSession.objects.get(session_code=session_code)
        except ClassSession.DoesNotExist:
            return JsonResponse({
                'valid': False,
                'message': 'Invalid session code. Please check and try again.'
            }, status=404)

        # If expected_session_id is provided, validate it matches
        if expected_session_id and session.id != expected_session_id:
            return JsonResponse({
                'valid': False,
                'message': f'This code is for a different session. Please use the code for the session you selected.'
            }, status=400)

        # Check if user already exists
        user_exists = Attendee.objects.filter(email__iexact=email).exists()

        return JsonResponse({
            'valid': True,
            'is_new_user': not user_exists,
            'message': 'Session code verified successfully.',
            'session': {
                'id': session.id,
                'title': session.title,
                'teacher': session.teacher,
                'session_code': session.session_code,
                'start_time': session.start_time.isoformat(),
                'end_time': session.end_time.isoformat(),
            }
        })

    except Exception as e:
        return JsonResponse({
            'valid': False,
            'message': f'Error verifying code: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def student_login_api(request):
    """
    Student login with email and optional password
    Request body: { "email": "user@example.com", "password": "password123" }
    Password is optional - if attendee has no password set, login with email only
    """
    try:
        from django.contrib.auth.hashers import check_password
        
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email is required.'
            }, status=400)

        # Find attendee by email
        try:
            attendee = Attendee.objects.get(email__iexact=email)
        except Attendee.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No account found with this email address.'
            }, status=401)

        # Check password if attendee has one set
        if attendee.password:
            if not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Password is required for this account.'
                }, status=401)
            
            pwd = attendee.password
            # Check if password is hashed
            if pwd.startswith('pbkdf2_') or pwd.startswith('argon2$') or pwd.startswith('bcrypt') or pwd.startswith('sha1$'):
                if not check_password(password, pwd):
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid password.'
                    }, status=401)
            else:
                # Legacy plaintext password
                if pwd != password:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid password.'
                    }, status=401)
        # If no password set, allow login with email only

        # Login successful - return attendee data
        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'attendee': {
                'id': attendee.id,
                'name': attendee.name,
                'email': attendee.email,
                'phone': attendee.phone,
                'session_id': attendee.class_session.id if attendee.class_session else None,
                'session_title': attendee.class_session.title if attendee.class_session else None,
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error during login: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_attendee_completed_sessions(request, attendee_id):
    """
    Get all sessions that the attendee has responded to
    Returns session IDs that should be hidden from "Available Sessions"
    """
    try:
        from .models import Response
        
        attendee = Attendee.objects.get(id=attendee_id)
        
        # Get all unique session IDs where the student has submitted responses
        completed_session_ids = Response.objects.filter(
            attendee=attendee
        ).values_list(
            'question__class_session_id', flat=True
        ).distinct()
        
        return JsonResponse({
            'success': True,
            'completed_session_ids': list(completed_session_ids),
            'count': len(completed_session_ids)
        })
        
    except Attendee.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Attendee not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
