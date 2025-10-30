"""
API Serializers for JWT Authentication and RESTful API endpoints
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Attendee, ClassSession, Question, Response, Review,
    QuizProgress, SessionAttendance, HitCounter, Admin
)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class AttendeeSerializer(serializers.ModelSerializer):
    """Serializer for Attendee model"""
    session_title = serializers.CharField(source='class_session.title', read_only=True, allow_null=True)
    session_code = serializers.CharField(source='class_session.session_code', read_only=True, allow_null=True)
    
    class Meta:
        model = Attendee
        fields = [
            'id', 'name', 'phone', 'email', 'age', 'place',
            'class_session', 'session_title', 'session_code',
            'has_submitted', 'quiz_started_at', 'plain_password',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'quiz_started_at']
        extra_kwargs = {
            'plain_password': {'write_only': True},
            'password': {'write_only': True}
        }


class AttendeeRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for attendee registration via API"""
    session_code = serializers.CharField(write_only=True, max_length=20)
    
    class Meta:
        model = Attendee
        fields = ['name', 'phone', 'email', 'session_code']
        extra_kwargs = {
            'phone': {'required': False},  # Make phone optional
        }
    
    def validate_session_code(self, value):
        """Validate that session code exists and is active"""
        from django.utils import timezone
        try:
            session = ClassSession.objects.get(session_code=value)
            now = timezone.now()
            if now < session.start_time:
                raise serializers.ValidationError("This session has not started yet.")
            if now > session.end_time:
                raise serializers.ValidationError("This session has already ended.")
            return value
        except ClassSession.DoesNotExist:
            raise serializers.ValidationError("Invalid session code.")
    
    def validate_email(self, value):
        """Check if email already registered for this session"""
        session_code = self.initial_data.get('session_code')
        if session_code:
            try:
                session = ClassSession.objects.get(session_code=session_code)
                if Attendee.objects.filter(email=value, class_session=session).exists():
                    raise serializers.ValidationError("This email is already registered for this session.")
            except ClassSession.DoesNotExist:
                pass
        return value
    
    def create(self, validated_data):
        session_code = validated_data.pop('session_code')
        session = ClassSession.objects.get(session_code=session_code)
        attendee = Attendee.objects.create(
            class_session=session,
            **validated_data
        )
        return attendee


class QuizSessionSerializer(serializers.ModelSerializer):
    """Serializer for Quiz Session model"""
    attendee_count = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    time_until_start = serializers.SerializerMethodField()
    time_until_end = serializers.SerializerMethodField()
    
    class Meta:
        model = ClassSession
        fields = [
            'id', 'title', 'teacher', 'start_time', 'end_time',
            'session_code', 'attendee_count', 'is_active',
            'time_until_start', 'time_until_end'
        ]
        read_only_fields = ['id', 'session_code']
    
    def get_attendee_count(self, obj):
        return obj.attendee_set.count()
    
    def get_is_active(self, obj):
        from django.utils import timezone
        now = timezone.now()
        return obj.start_time <= now <= obj.end_time
    
    def get_time_until_start(self, obj):
        from django.utils import timezone
        now = timezone.now()
        if now < obj.start_time:
            delta = obj.start_time - now
            return int(delta.total_seconds())
        return 0
    
    def get_time_until_end(self, obj):
        from django.utils import timezone
        now = timezone.now()
        if now < obj.end_time:
            delta = obj.end_time - now
            return int(delta.total_seconds())
        return 0


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model"""
    session_title = serializers.CharField(source='class_session.title', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'class_session', 'session_title', 'text',
            'question_type', 'option1', 'option2', 'option3', 'option4', 
            'correct_option'
        ]
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        """Hide correct answer for non-staff users"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and not request.user.is_staff:
            representation.pop('correct_option', None)
        return representation


class ResponseSerializer(serializers.ModelSerializer):
    """Serializer for Response model"""
    attendee_name = serializers.CharField(source='attendee.name', read_only=True)
    question_text = serializers.CharField(source='question.text', read_only=True)
    is_correct = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Response
        fields = [
            'id', 'attendee', 'attendee_name', 'question',
            'question_text', 'selected_option', 'text_response', 'is_correct'
        ]
        read_only_fields = ['id', 'is_correct']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review/Feedback model"""
    attendee_name = serializers.CharField(source='attendee.name', read_only=True)
    attendee_email = serializers.CharField(source='attendee.email', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'attendee', 'attendee_name', 'attendee_email',
            'content', 'submitted_at'
        ]
        read_only_fields = ['id', 'submitted_at']


class QuizSessionDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Quiz Session with related data"""
    questions = QuestionSerializer(many=True, read_only=True, source='question_set')
    attendees = AttendeeSerializer(many=True, read_only=True, source='attendee_set')
    attendee_count = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = ClassSession
        fields = [
            'id', 'title', 'teacher', 'start_time', 'end_time',
            'session_code', 'attendee_count', 'is_active',
            'questions', 'attendees'
        ]
        read_only_fields = ['id', 'session_code']
    
    def get_attendee_count(self, obj):
        return obj.attendee_set.count()
    
    def get_is_active(self, obj):
        from django.utils import timezone
        now = timezone.now()
        return obj.start_time <= now <= obj.end_time


class QuizProgressSerializer(serializers.ModelSerializer):
    """Serializer for QuizProgress model"""
    attendee_name = serializers.CharField(source='attendee.name', read_only=True)
    session_title = serializers.CharField(source='class_session.title', read_only=True)
    progress_stats = serializers.SerializerMethodField()
    answered_question_ids = serializers.SerializerMethodField()
    
    class Meta:
        model = QuizProgress
        fields = [
            'id', 'attendee', 'attendee_name', 'class_session', 'session_title',
            'last_answered_at', 'is_fully_completed', 'progress_stats',
            'answered_question_ids'
        ]
        read_only_fields = ['id', 'last_answered_at']
    
    def get_progress_stats(self, obj):
        return obj.get_progress_stats()
    
    def get_answered_question_ids(self, obj):
        return obj.get_answered_question_ids()


class SessionAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for SessionAttendance model"""
    attendee_name = serializers.CharField(source='attendee.name', read_only=True)
    attendee_email = serializers.CharField(source='attendee.email', read_only=True)
    session_title = serializers.CharField(source='class_session.title', read_only=True)
    session_code = serializers.CharField(source='class_session.session_code', read_only=True)
    
    class Meta:
        model = SessionAttendance
        fields = [
            'id', 'attendee', 'attendee_name', 'attendee_email',
            'class_session', 'session_title', 'session_code',
            'joined_at', 'has_submitted'
        ]
        read_only_fields = ['id', 'joined_at']


class HitCounterSerializer(serializers.ModelSerializer):
    """Serializer for HitCounter model"""
    ip_address = serializers.CharField(max_length=45)  # Override to avoid DRF compatibility issue
    
    class Meta:
        model = HitCounter
        fields = [
            'id', 'ip_address', 'user_agent', 'path', 'method',
            'timestamp', 'session_key', 'user'
        ]
        read_only_fields = ['id', 'timestamp']


class AdminSerializer(serializers.ModelSerializer):
    """Serializer for Admin model"""
    
    class Meta:
        model = Admin
        fields = ['id', 'username', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AdminRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for admin registration via API"""
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    
    class Meta:
        model = Admin
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def validate_username(self, value):
        if Admin.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def validate_email(self, value):
        if Admin.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value
    
    def create(self, validated_data):
        from django.contrib.auth.hashers import make_password
        validated_data.pop('password2')
        validated_data['password'] = make_password(validated_data['password'])
        admin = Admin.objects.create(**validated_data)
        return admin
