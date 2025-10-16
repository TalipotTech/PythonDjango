from django.db import models
from django.core.validators import RegexValidator

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

    def __str__(self):
        return f"{self.title} — {self.teacher}"

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits.')]
    )
    email = models.EmailField()
    age = models.PositiveIntegerField(null=True, blank=True)  # Made optional
    place = models.CharField(max_length=100, blank=True, default='')  # Made optional
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, null=True, blank=True)  # Made optional
    has_submitted = models.BooleanField(default=False)
    quiz_started_at = models.DateTimeField(null=True, blank=True)  # Track when quiz started
    # Store Django-style hashed password for student login
    password = models.CharField(max_length=128, blank=True)

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


class Review(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee.name} - {self.submitted_at.strftime('%Y-%m-%d')}"