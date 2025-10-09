from django.contrib import admin
from .models import ClassSession, Attendee, Question, Response, Review
from django.db import models
from django.contrib.auth.models import Group, User

# 🔹 Inline view of attendee responses
class ResponseInline(admin.TabularInline):
    model = Response
    fields = ['question_text', 'selected_option_display', 'is_correct']
    readonly_fields = ['question_text', 'selected_option_display', 'is_correct']
    extra = 0

    def question_text(self, obj):
        return obj.question.text
    question_text.short_description = 'Question'

    def selected_option_display(self, obj):
        options = {
            1: obj.question.option1,
            2: obj.question.option2,
            3: obj.question.option3,
            4: obj.question.option4,
        }
        return options.get(obj.selected_option, "Invalid")
    selected_option_display.short_description = 'Selected Answer'

    def is_correct(self, obj):
        return obj.selected_option == obj.question.correct_option
    is_correct.boolean = True
    is_correct.short_description = 'Correct?'

# 🔹 Attendee admin: view-only with score summary and inline responses
@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'class_session', 'total_attempted', 'total_correct', 'score_percent']
    readonly_fields = ['total_attempted', 'total_correct', 'score_percent']
    inlines = [ResponseInline]

    def total_attempted(self, obj):
        return Response.objects.filter(attendee=obj).count()

    def total_correct(self, obj):
        return Response.objects.filter(
            attendee=obj,
            selected_option=models.F('question__correct_option')
        ).count()

    def score_percent(self, obj):
        attempted = self.total_attempted(obj)
        correct = self.total_correct(obj)
        return round((correct / attempted) * 100, 2) if attempted else 0

# 🔹 Question admin: editable per class
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'class_session', 'correct_option']
    fields = ['class_session', 'text', 'option1', 'option2', 'option3', 'option4', 'correct_option']


# 🔹 Response admin: view-only
@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['attendee', 'class_session', 'question', 'selected_option', 'is_correct']
    readonly_fields = ['attendee', 'question', 'selected_option']

    def class_session(self, obj):
        return obj.question.class_session
    class_session.short_description = 'Class'

    def is_correct(self, obj):
        return obj.selected_option == obj.question.correct_option
    is_correct.boolean = True
    is_correct.short_description = 'Correct?'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

# 🔹 ClassSession admin
@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'start_time', 'end_time']
    fields = ['title', 'teacher', 'start_time', 'end_time']

# 🔹 Review admin: corrected to match your new model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('attendee', 'content', 'submitted_at')
    list_display = ('attendee', 'content', 'submitted_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# 🔹 Clean up default admin
admin.site.unregister(Group)
admin.site.unregister(User)
