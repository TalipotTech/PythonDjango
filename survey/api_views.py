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
    Request body: { "email": "user@example.com", "session_code": "ABC12345" }
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        session_code = data.get('session_code', '').strip()

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
                'message': 'Invalid session code.'
            }, status=404)

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
