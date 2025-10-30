"""
REST API Views with JWT Authentication
"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import (
    Attendee, ClassSession, Question, Response as QuizResponse, Review,
    QuizProgress, SessionAttendance, HitCounter, Admin
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    AttendeeSerializer, AttendeeRegistrationSerializer,
    QuizSessionSerializer, QuizSessionDetailSerializer,
    QuestionSerializer, ResponseSerializer, ReviewSerializer,
    QuizProgressSerializer, SessionAttendanceSerializer,
    HitCounterSerializer, AdminSerializer, AdminRegistrationSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully. Please login to get your access token.'
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for user profile
    GET/PUT /api/auth/profile/
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class AttendeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Attendees
    GET /api/attendees/ - List all attendees (Admin only)
    POST /api/attendees/ - Register new attendee
    GET /api/attendees/{id}/ - Get attendee details
    PUT/PATCH /api/attendees/{id}/ - Update attendee
    DELETE /api/attendees/{id}/ - Delete attendee (Admin only)
    """
    queryset = Attendee.objects.all().select_related('class_session')
    serializer_class = AttendeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['class_session', 'has_submitted']
    search_fields = ['name', 'email', 'place']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Allow anyone to register (POST)
        Require authentication for list/retrieve
        Require admin for delete
        """
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['destroy', 'list']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AttendeeRegistrationSerializer
        return AttendeeSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_registrations(self, request):
        """Get registrations for current user's email"""
        email = request.query_params.get('email', request.user.email)
        attendees = self.queryset.filter(email=email)
        serializer = self.get_serializer(attendees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit_quiz(self, request, pk=None):
        """Mark attendee as having submitted their quiz"""
        attendee = self.get_object()
        attendee.has_submitted = True
        attendee.save()
        return Response({'message': 'Quiz marked as submitted'}, status=status.HTTP_200_OK)


class QuizSessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Quiz Sessions
    GET /api/sessions/ - List all sessions
    POST /api/sessions/ - Create new session (Admin only)
    GET /api/sessions/{id}/ - Get session details
    PUT/PATCH /api/sessions/{id}/ - Update session (Admin only)
    DELETE /api/sessions/{id}/ - Delete session (Admin only)
    """
    queryset = ClassSession.objects.all().prefetch_related('attendee_set', 'question_set')
    serializer_class = QuizSessionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['teacher']
    search_fields = ['title', 'teacher', 'session_code']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['-start_time']
    
    def get_permissions(self):
        """
        Allow anyone to view sessions (GET)
        Require admin for create/update/delete
        """
        if self.action in ['list', 'retrieve', 'active_sessions', 'upcoming_sessions']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizSessionDetailSerializer
        return QuizSessionSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def active_sessions(self, request):
        """Get currently active sessions"""
        now = timezone.now()
        sessions = self.queryset.filter(
            start_time__lte=now,
            end_time__gte=now
        )
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def upcoming_sessions(self, request):
        """Get upcoming sessions"""
        now = timezone.now()
        sessions = self.queryset.filter(start_time__gt=now)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def attendees(self, request, pk=None):
        """Get all attendees for a session"""
        session = self.get_object()
        attendees = session.attendee_set.all()
        serializer = AttendeeSerializer(attendees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def questions(self, request, pk=None):
        """Get all questions for a session"""
        session = self.get_object()
        questions = session.question_set.all()
        serializer = QuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_code(self, request):
        """Verify if session code is valid"""
        session_code = request.data.get('session_code')
        if not session_code:
            return Response(
                {'error': 'Session code is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            session = ClassSession.objects.get(session_code=session_code)
            now = timezone.now()
            
            if now < session.start_time:
                return Response({
                    'valid': False,
                    'message': 'Session has not started yet',
                    'session': QuizSessionSerializer(session).data
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if now > session.end_time:
                return Response({
                    'valid': False,
                    'message': 'Session has ended',
                    'session': QuizSessionSerializer(session).data
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'valid': True,
                'message': 'Session code is valid',
                'session': QuizSessionSerializer(session).data
            }, status=status.HTTP_200_OK)
            
        except ClassSession.DoesNotExist:
            return Response(
                {'valid': False, 'message': 'Invalid session code'},
                status=status.HTTP_404_NOT_FOUND
            )


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Questions
    """
    queryset = Question.objects.all().select_related('class_session')
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['class_session', 'question_type']
    search_fields = ['text']
    
    def get_permissions(self):
        """
        Allow authenticated users to view questions
        Require admin for create/update/delete
        """
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class ResponseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Quiz Responses
    """
    queryset = QuizResponse.objects.all().select_related('attendee', 'question')
    serializer_class = ResponseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['attendee', 'question']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Non-staff users can only see their own responses
        """
        queryset = super().get_queryset()
        # Skip filtering during Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        if not self.request.user.is_staff:
            # Filter by email if attendee
            email = self.request.query_params.get('email', self.request.user.email if self.request.user.is_authenticated else None)
            if email:
                queryset = queryset.filter(attendee__email=email)
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_responses(self, request):
        """Get responses for current user"""
        email = request.query_params.get('email', request.user.email)
        responses = self.queryset.filter(attendee__email=email)
        serializer = self.get_serializer(responses, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Reviews/Feedback - No authentication required for creating feedback
    """
    queryset = Review.objects.all().select_related('attendee')
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['attendee']
    search_fields = ['content']
    ordering_fields = ['submitted_at']
    ordering = ['-submitted_at']
    authentication_classes = []  # No authentication required
    
    def get_permissions(self):
        """
        Allow anyone to create feedback/reviews
        Admin can see all reviews
        """
        if self.action == 'create':
            return [AllowAny()]  # Anyone can submit feedback
        elif self.action in ['list', 'retrieve']:
            return [IsAdminUser()]  # Only admin can view feedback
        return [IsAdminUser()]
    
    def get_queryset(self):
        """
        Non-staff users can only see their own reviews
        """
        queryset = super().get_queryset()
        # Skip filtering during Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        if not self.request.user.is_staff:
            email = self.request.query_params.get('email', self.request.user.email if self.request.user.is_authenticated else None)
            if email:
                queryset = queryset.filter(attendee__email=email)
        return queryset


class QuizProgressViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Quiz Progress tracking
    """
    queryset = QuizProgress.objects.all().select_related('attendee', 'class_session')
    serializer_class = QuizProgressSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['attendee', 'class_session', 'is_fully_completed']
    ordering_fields = ['last_answered_at']
    ordering = ['-last_answered_at']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Non-staff users can only see their own progress
        """
        queryset = super().get_queryset()
        # Skip filtering during Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        if not self.request.user.is_staff:
            email = self.request.query_params.get('email', self.request.user.email if self.request.user.is_authenticated else None)
            if email:
                queryset = queryset.filter(attendee__email=email)
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def update_completion(self, request, pk=None):
        """Update completion status for a quiz progress"""
        progress = self.get_object()
        is_completed = progress.update_completion_status()
        return Response({
            'is_fully_completed': is_completed,
            'progress_stats': progress.get_progress_stats()
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_progress(self, request):
        """Get progress for current user"""
        email = request.query_params.get('email', request.user.email)
        progress_list = self.queryset.filter(attendee__email=email)
        serializer = self.get_serializer(progress_list, many=True)
        return Response(serializer.data)


class SessionAttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Session Attendance tracking
    """
    queryset = SessionAttendance.objects.all().select_related('attendee', 'class_session')
    serializer_class = SessionAttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['attendee', 'class_session', 'has_submitted']
    ordering_fields = ['joined_at']
    ordering = ['-joined_at']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Non-staff users can only see their own attendance
        """
        queryset = super().get_queryset()
        # Skip filtering during Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        if not self.request.user.is_staff:
            email = self.request.query_params.get('email', self.request.user.email if self.request.user.is_authenticated else None)
            if email:
                queryset = queryset.filter(attendee__email=email)
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_attendance(self, request):
        """Get attendance history for current user"""
        email = request.query_params.get('email', request.user.email)
        attendance = self.queryset.filter(attendee__email=email)
        serializer = self.get_serializer(attendance, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def session_attendees(self, request):
        """Get all attendees for a specific session"""
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response(
                {'error': 'session_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        attendance = self.queryset.filter(class_session_id=session_id)
        serializer = self.get_serializer(attendance, many=True)
        return Response(serializer.data)


class HitCounterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Hit Counter (Read-only)
    """
    queryset = HitCounter.objects.all()
    serializer_class = HitCounterSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ip_address', 'path', 'method']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """Get hit counter statistics"""
        total_hits = HitCounter.get_total_hits()
        unique_visitors = HitCounter.get_unique_visitors()
        hits_today = HitCounter.get_hits_today()
        popular_pages = list(HitCounter.get_popular_pages(limit=10))
        
        return Response({
            'total_hits': total_hits,
            'unique_visitors': unique_visitors,
            'hits_today': hits_today,
            'popular_pages': popular_pages
        })


class AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin management
    """
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['created_at', 'username']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AdminRegistrationSerializer
        return AdminSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register new admin (can be restricted in production)"""
        serializer = AdminRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin = serializer.save()
        return Response({
            'admin': AdminSerializer(admin).data,
            'message': 'Admin registered successfully'
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    """
    API Overview - List all available endpoints
    """
    endpoints = {
        'authentication': {
            'register': '/api/auth/register/ [POST]',
            'login': '/api/auth/token/ [POST]',
            'refresh': '/api/auth/token/refresh/ [POST]',
            'profile': '/api/auth/profile/ [GET, PUT]',
        },
        'sessions': {
            'list': '/api/sessions/ [GET]',
            'create': '/api/sessions/ [POST] - Admin only',
            'detail': '/api/sessions/{id}/ [GET, PUT, PATCH, DELETE]',
            'active': '/api/sessions/active_sessions/ [GET]',
            'upcoming': '/api/sessions/upcoming_sessions/ [GET]',
            'verify_code': '/api/sessions/verify_code/ [POST]',
            'attendees': '/api/sessions/{id}/attendees/ [GET]',
            'questions': '/api/sessions/{id}/questions/ [GET]',
        },
        'attendees': {
            'list': '/api/attendees/ [GET] - Admin only',
            'register': '/api/attendees/ [POST]',
            'detail': '/api/attendees/{id}/ [GET, PUT, PATCH, DELETE]',
            'my_registrations': '/api/attendees/my_registrations/ [GET]',
            'submit_quiz': '/api/attendees/{id}/submit_quiz/ [POST]',
        },
        'questions': {
            'list': '/api/questions/ [GET]',
            'create': '/api/questions/ [POST] - Admin only',
            'detail': '/api/questions/{id}/ [GET, PUT, PATCH, DELETE]',
        },
        'responses': {
            'list': '/api/responses/ [GET]',
            'create': '/api/responses/ [POST]',
            'detail': '/api/responses/{id}/ [GET, PUT, PATCH, DELETE]',
            'my_responses': '/api/responses/my_responses/ [GET]',
        },
        'reviews': {
            'list': '/api/reviews/ [GET] - Admin only',
            'create': '/api/reviews/ [POST]',
            'detail': '/api/reviews/{id}/ [GET, PUT, PATCH, DELETE]',
        },
        'progress': {
            'list': '/api/progress/ [GET]',
            'detail': '/api/progress/{id}/ [GET, PUT, PATCH, DELETE]',
            'my_progress': '/api/progress/my_progress/ [GET]',
            'update_completion': '/api/progress/{id}/update_completion/ [POST]',
        },
        'attendance': {
            'list': '/api/attendance/ [GET]',
            'detail': '/api/attendance/{id}/ [GET, PUT, PATCH, DELETE]',
            'my_attendance': '/api/attendance/my_attendance/ [GET]',
            'session_attendees': '/api/attendance/session_attendees/?session_id={id} [GET]',
        },
        'hit_counter': {
            'list': '/api/hits/ [GET] - Admin only',
            'statistics': '/api/hits/statistics/ [GET] - Admin only',
        },
        'admins': {
            'list': '/api/admins/ [GET] - Admin only',
            'register': '/api/admins/register/ [POST]',
            'detail': '/api/admins/{id}/ [GET, PUT, PATCH, DELETE] - Admin only',
        },
        'statistics': {
            'dashboard': '/api/stats/dashboard/ [GET] - Admin only',
        }
    }
    
    return Response({
        'message': 'Welcome to Ensate Workshops REST API',
        'version': '2.0',
        'endpoints': endpoints,
        'authentication': 'JWT Bearer Token required for most endpoints',
        'docs': 'Visit /api/ for browsable API documentation',
        'note': 'Use Authorization header: Bearer <your_token>'
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_statistics(request):
    """
    Get dashboard statistics
    Admin only
    """
    from django.db.models import Count, Q
    from .models import HitCounter
    
    now = timezone.now()
    
    total_sessions = ClassSession.objects.count()
    active_sessions = ClassSession.objects.filter(
        start_time__lte=now,
        end_time__gte=now
    ).count()
    upcoming_sessions = ClassSession.objects.filter(start_time__gt=now).count()
    past_sessions = ClassSession.objects.filter(end_time__lt=now).count()
    
    total_attendees = Attendee.objects.count()
    total_questions = Question.objects.count()
    total_responses = QuizResponse.objects.count()
    total_reviews = Review.objects.count()
    
    # Hit counter stats
    total_hits = HitCounter.objects.aggregate(
        total=Count('id')
    )['total'] or 0
    
    unique_ips = HitCounter.objects.values('ip_address').distinct().count()
    
    # Recent activity
    recent_attendees = AttendeeSerializer(
        Attendee.objects.order_by('-created_at')[:5],
        many=True
    ).data
    
    recent_reviews = ReviewSerializer(
        Review.objects.order_by('-created_at')[:5],
        many=True
    ).data
    
    return Response({
        'sessions': {
            'total': total_sessions,
            'active': active_sessions,
            'upcoming': upcoming_sessions,
            'past': past_sessions,
        },
        'attendees': {
            'total': total_attendees,
        },
        'content': {
            'questions': total_questions,
            'responses': total_responses,
            'reviews': total_reviews,
        },
        'traffic': {
            'total_hits': total_hits,
            'unique_visitors': unique_ips,
        },
        'recent_activity': {
            'attendees': recent_attendees,
            'reviews': recent_reviews,
        }
    })
