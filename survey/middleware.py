"""
Middleware for tracking page hits and visitor statistics
"""
from .models import HitCounter


def get_client_ip(request):
    """Get the client's IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class HitCountMiddleware:
    """
    Middleware to track all page visits
    Records IP address, user agent, path, and timestamp
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request before view
        response = self.get_response(request)
        
        # Track the hit after response (async-safe)
        try:
            # Skip static files and media
            if not request.path.startswith(('/static/', '/media/', '/admin/jsi18n/')):
                # Skip API endpoints if desired (optional)
                # if not request.path.startswith('/api/'):
                
                HitCounter.objects.create(
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    path=request.path,
                    method=request.method,
                    session_key=request.session.session_key if hasattr(request.session, 'session_key') else None,
                    user=request.user if request.user.is_authenticated else None
                )
        except Exception as e:
            # Don't break the request if tracking fails
            print(f"Hit counter error: {e}")
        
        return response
