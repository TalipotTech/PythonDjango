from django.db import models
from django.core.validators import RegexValidator
import random
import string

class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class ClassSession(models.Model):
    title = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    session_code = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-generate session code if not provided
        if not self.session_code:
            self.session_code = self.generate_session_code()
        super().save(*args, **kwargs)

    def generate_session_code(self):
        """Generate a unique 8-character session code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not ClassSession.objects.filter(session_code=code).exists():
                return code

    def __str__(self):
        return f"{self.title} — {self.teacher}"

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits.')]
        # Note: unique=True removed to allow migration, will be enforced in forms
    )
    email = models.EmailField()  # unique=True removed to allow migration, will be enforced in forms
    age = models.PositiveIntegerField(null=True, blank=True)  # Made optional
    place = models.CharField(max_length=100, blank=True, default='')  # Made optional
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, null=True, blank=True)  # Made optional
    has_submitted = models.BooleanField(default=False)
    quiz_started_at = models.DateTimeField(null=True, blank=True)  # Track when quiz started
    # Store Django-style hashed password for student login
    password = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Allow null for existing rows
    updated_at = models.DateTimeField(auto_now=True, null=True)  # Allow null for existing rows

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.name} - {self.class_session.title if self.class_session else 'No Session'}"

class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('text_response', 'Text Response'),
    ]
    
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    
    # These fields are only used for multiple choice questions
    option1 = models.CharField(max_length=255, blank=True, null=True)
    option2 = models.CharField(max_length=255, blank=True, null=True)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)
    correct_option = models.IntegerField(blank=True, null=True)  # stores 1, 2, 3, or 4
    
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} [{self.class_session.title}] - {self.get_question_type_display()}"


class Response(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # For multiple choice questions
    selected_option = models.IntegerField(blank=True, null=True)
    
    # For text response questions
    text_response = models.TextField(blank=True, null=True)

    @property
    def is_correct(self):
        # Only applicable for multiple choice questions
        if self.question.question_type == 'multiple_choice':
            return self.selected_option == self.question.correct_option
        return None  # Text responses don't have right/wrong answers


class QuizProgress(models.Model):
    """Track which questions a student has answered for each session"""
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    last_answered_at = models.DateTimeField(auto_now=True)
    is_fully_completed = models.BooleanField(default=False)  # True when all current questions are answered
    
    class Meta:
        unique_together = ('attendee', 'class_session')
        verbose_name_plural = 'Quiz Progress Records'
    
    def __str__(self):
        return f"{self.attendee.name} - {self.class_session.title} ({'Complete' if self.is_fully_completed else 'In Progress'})"
    
    def get_answered_question_ids(self):
        """Get list of question IDs this student has answered for this session"""
        return list(Response.objects.filter(
            attendee=self.attendee,
            question__class_session=self.class_session
        ).values_list('question_id', flat=True))
    
    def get_unanswered_questions(self):
        """Get questions in this session that student hasn't answered yet"""
        answered_ids = self.get_answered_question_ids()
        return Question.objects.filter(
            class_session=self.class_session
        ).exclude(id__in=answered_ids).order_by('id')
    
    def get_progress_stats(self):
        """Get progress statistics"""
        total_questions = Question.objects.filter(class_session=self.class_session).count()
        answered_questions = len(self.get_answered_question_ids())
        pending_questions = total_questions - answered_questions
        
        return {
            'total': total_questions,
            'answered': answered_questions,
            'pending': pending_questions,
            'percentage': round((answered_questions / total_questions * 100) if total_questions > 0 else 0, 1)
        }
    
    def update_completion_status(self):
        """Check if all questions are answered and update completion status"""
        stats = self.get_progress_stats()
        self.is_fully_completed = (stats['pending'] == 0 and stats['total'] > 0)
        self.save()
        return self.is_fully_completed


class SessionAttendance(models.Model):
    """Track all sessions attended by each user"""
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='attendance_history')
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='attendances')
    joined_at = models.DateTimeField(auto_now_add=True)
    has_submitted = models.BooleanField(default=False)  # Did they submit responses for this session?
    
    class Meta:
        unique_together = ('attendee', 'class_session')
        ordering = ['-joined_at']
        verbose_name_plural = 'Session Attendances'
    
    def __str__(self):
        return f"{self.attendee.name} → {self.class_session.title}"


class Review(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee.name} - {self.submitted_at.strftime('%Y-%m-%d')}"