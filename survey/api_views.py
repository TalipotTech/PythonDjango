"""
API views for AJAX requests
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Attendee
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
