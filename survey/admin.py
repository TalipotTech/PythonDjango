from django.contrib import admin
from .models import ClassSession, Attendee, Question, Response, Review, Admin
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
    list_display = ['name', 'email', 'phone', 'class_session', 'age', 'place', 'has_submitted', 'total_questions', 'total_correct', 'score_percent']
    readonly_fields = ['total_questions', 'total_correct', 'score_percent']
    inlines = [ResponseInline]
    search_fields = ['name', 'email', 'phone', 'place']
    list_filter = ['class_session', 'has_submitted', 'age', 'place']
    list_per_page = 20
    ordering = ['-id']
    date_hierarchy = None
    actions = ['delete_selected']
    list_display_links = ['name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'age', 'place')
        }),
        ('Session Information', {
            'fields': ('class_session', 'has_submitted', 'quiz_started_at')
        }),
        ('Performance', {
            'fields': ('total_questions', 'total_correct', 'score_percent')
        }),
    )

    def total_questions(self, obj):
        return Response.objects.filter(attendee=obj).count()
    total_questions.short_description = 'Total Questions'

    def total_correct(self, obj):
        return Response.objects.filter(
            attendee=obj,
            selected_option=models.F('question__correct_option')
        ).count()
    total_correct.short_description = 'Total Correct'

    def score_percent(self, obj):
        attempted = self.total_questions(obj)
        correct = self.total_correct(obj)
        return round((correct / attempted) * 100, 2) if attempted else 0
    score_percent.short_description = 'Score %'

# 🔹 Question admin: editable per class
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'class_session', 'correct_option', 'option1', 'option2', 'option3', 'option4']
    fields = ['class_session', 'text', 'option1', 'option2', 'option3', 'option4', 'correct_option']
    search_fields = ['text', 'option1', 'option2', 'option3', 'option4']
    list_filter = ['class_session', 'correct_option']
    list_per_page = 20
    actions = ['delete_selected']


# 🔹 Response admin: view-only
@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['attendee', 'class_session', 'question', 'selected_option', 'is_correct']
    readonly_fields = ['attendee', 'question', 'selected_option']
    search_fields = ['attendee__name', 'attendee__email', 'question__text']
    list_filter = ['question__class_session', 'selected_option']
    list_per_page = 30
    actions = ['delete_selected']

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
    list_display = ['title', 'teacher', 'start_time', 'end_time', 'session_status', 'attendee_count', 'question_count']
    fields = ['title', 'teacher', 'start_time', 'end_time']
    search_fields = ['title', 'teacher']
    list_filter = ['teacher', 'start_time', 'end_time']
    date_hierarchy = 'start_time'
    list_per_page = 20
    actions = ['delete_selected']
    
    def session_status(self, obj):
        from django.utils import timezone
        now = timezone.localtime(timezone.now())
        
        if now < obj.start_time:
            return "⏳ Inactive (Not Started)"
        elif obj.start_time <= now <= obj.end_time:
            return "✅ Active"
        else:
            return "🔴 Finished"
    session_status.short_description = 'Status'
    
    def attendee_count(self, obj):
        return obj.attendee_set.count()
    attendee_count.short_description = 'Attendees'
    
    def question_count(self, obj):
        return obj.question_set.count()
    question_count.short_description = 'Questions'

# 🔹 Review admin: corrected to match your new model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('attendee', 'content', 'submitted_at', 'feedback_type')
    list_display = ('attendee', 'attendee_email', 'content_preview', 'feedback_type', 'submitted_at', 'class_session_info')
    search_fields = ['attendee__name', 'attendee__email', 'content']
    list_filter = ['submitted_at', 'attendee__class_session', 'feedback_type']
    date_hierarchy = 'submitted_at'
    list_per_page = 20
    actions = ['delete_selected']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Feedback/Question Content'
    
    def class_session_info(self, obj):
        return obj.attendee.class_session.title if obj.attendee and obj.attendee.class_session else 'N/A'
    class_session_info.short_description = 'Class Session'
    
    def attendee_email(self, obj):
        return obj.attendee.email if obj.attendee else 'N/A'
    attendee_email.short_description = 'Email'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True

# 🔹 Admin model registration
@admin.register(Admin)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'created_at']
    readonly_fields = ['created_at']
    fields = ['username', 'email', 'password', 'created_at']
    search_fields = ['username', 'email']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    actions = ['delete_selected']

# 🔹 Clean up default admin
admin.site.unregister(Group)
admin.site.unregister(User)

# 🔹 Customize admin site
admin.site.site_header = 'Quiz Portal Administration'
admin.site.site_title = 'Quiz Portal Admin'
admin.site.index_title = 'Welcome to Quiz Portal Admin'
