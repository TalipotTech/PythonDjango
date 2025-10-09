from django.db import models
from django.core.validators import RegexValidator

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
    age = models.PositiveIntegerField()
    place = models.CharField(max_length=100)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    has_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.class_session.title}"

class Question(models.Model):
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField()  # stores 1, 2, 3, or 4
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} [{self.class_session.title}]"


class Response(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.IntegerField()

    @property
    def is_correct(self):
        return self.selected_option == self.question.correct_option


class Review(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee.name} - {self.submitted_at.strftime('%Y-%m-%d')}"