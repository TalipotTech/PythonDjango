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

# Create router for ViewSets
router = DefaultRouter()
router.register(r'attendees', AttendeeViewSet, basename='api-attendee')
router.register(r'sessions', QuizSessionViewSet, basename='api-session')
router.register(r'questions', QuestionViewSet, basename='api-question')
router.register(r'responses', ResponseViewSet, basename='api-response')
router.register(r'reviews', ReviewViewSet, basename='api-review')
router.register(r'progress', QuizProgressViewSet, basename='api-progress')
router.register(r'attendance', SessionAttendanceViewSet, basename='api-attendance')
router.register(r'hits', HitCounterViewSet, basename='api-hits')
router.register(r'admins', AdminViewSet, basename='api-admin')

app_name = 'api'

urlpatterns = [
    # API Overview
    path('', api_overview, name='overview'),
    
    # Authentication endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # Statistics endpoints
    path('stats/dashboard/', dashboard_statistics, name='dashboard_stats'),
    
    # Router URLs (ViewSets)
    path('', include(router.urls)),
]
