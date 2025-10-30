"""
API URL Configuration with JWT Authentication
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .rest_api_views import (
    UserRegistrationView, UserProfileView,
    AttendeeViewSet, QuizSessionViewSet, QuestionViewSet,
    ResponseViewSet, ReviewViewSet,
    QuizProgressViewSet, SessionAttendanceViewSet,
    HitCounterViewSet, AdminViewSet,
    api_overview, dashboard_statistics
)

# Import from api_views
from .api_views import check_participant_exists, send_session_code_email, verify_session_code_with_email

# Create router for ViewSets - Only 3 endpoints for now
router = DefaultRouter()
router.register(r'students', AttendeeViewSet, basename='api-student')  # Student Registration
router.register(r'sessions', QuizSessionViewSet, basename='api-session')  # Session Information
router.register(r'feedback', ReviewViewSet, basename='api-feedback')  # Feedback

# Commented out - Not needed for now
# router.register(r'questions', QuestionViewSet, basename='api-question')
# router.register(r'responses', ResponseViewSet, basename='api-response')
# router.register(r'progress', QuizProgressViewSet, basename='api-progress')
# router.register(r'attendance', SessionAttendanceViewSet, basename='api-attendance')
# router.register(r'hits', HitCounterViewSet, basename='api-hits')
# router.register(r'admins', AdminViewSet, basename='api-admin')

app_name = 'api'

urlpatterns = [
    # API Overview
    path('', api_overview, name='overview'),

    # Student Registration (simplified - no JWT for now)
    # Students can register directly without authentication
    
    # AJAX endpoints for session access
    path('sessions/send_code/', send_session_code_email, name='send_session_code'),
    path('sessions/verify_code/', verify_session_code_with_email, name='verify_session_code'),

    # Router URLs (ViewSets) - Only 3 main endpoints
    path('', include(router.urls)),
    
    # Commented out - Authentication endpoints (not needed for now)
    # path('auth/register/', UserRegistrationView.as_view(), name='register'),
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/profile/', UserProfileView.as_view(), name='profile'),
    # path('stats/dashboard/', dashboard_statistics, name='dashboard_stats'),
    # path('check-participant/', check_participant_exists, name='check_participant'),
]
