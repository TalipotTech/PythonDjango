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
from .api_views import check_participant_exists, send_session_code_email, verify_session_code_with_email, student_login_api, get_attendee_completed_sessions

# Create router for ViewSets - Student + Admin endpoints
router = DefaultRouter()
# Student endpoints
router.register(r'students', AttendeeViewSet, basename='api-student')  # Student Registration
router.register(r'sessions', QuizSessionViewSet, basename='api-session')  # Session Information
router.register(r'feedback', ReviewViewSet, basename='api-feedback')  # Feedback
router.register(r'questions', QuestionViewSet, basename='api-question')  # Questions for quiz
router.register(r'responses', ResponseViewSet, basename='api-response')  # Submit responses

# Admin endpoints
router.register(r'admins', AdminViewSet, basename='api-admin')  # Admin management

app_name = 'api'

urlpatterns = [
    # API Overview
    path('', api_overview, name='overview'),

    # Student Registration (simplified - no JWT for now)
    # Students can register directly without authentication
    
    # AJAX endpoints for session access
    path('sessions/send_code/', send_session_code_email, name='send_session_code'),
    path('sessions/verify_code/', verify_session_code_with_email, name='verify_session_code'),
    path('student/login/', student_login_api, name='student_login_api'),
    path('student/<int:attendee_id>/completed-sessions/', get_attendee_completed_sessions, name='attendee_completed_sessions'),

    # Router URLs (ViewSets) - Student + Admin endpoints
    path('', include(router.urls)),
    
    # Admin authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # Admin statistics dashboard
    path('stats/dashboard/', dashboard_statistics, name='dashboard_stats'),
]
