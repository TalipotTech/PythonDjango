from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.home, name='home'),
    
    # New workflow URLs
    path('session/<int:session_id>/request-code/', views.request_session_code, name='request_session_code'),
    path('session/<int:session_id>/verify-code/', views.verify_session_code, name='verify_session_code'),
    path('new/register/', views.new_participant_register, name='new_participant_register'),
    path('new/login/', views.new_participant_login, name='new_participant_login'),
    
    # API endpoints
    path('api/check-participant/', api_views.check_participant_exists, name='api_check_participant'),
    path('session/<int:session_id>/confirm/', views.session_confirm, name='session_confirm'),
    path('join/', views.session_code_entry, name='session_code_entry'),
    path('identify/', views.participant_identify, name='participant_identify'),
    path('participant/register/', views.participant_register, name='participant_register'),
    path('participant/login/', views.participant_login, name='participant_login'),
    path('submit/', views.submit_response, name='submit_response'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
    path('already-submitted/', views.already_submitted, name='already_submitted'),
    
    # Student routes
    path('student-login/', views.student_login, name='student_login'),
    path('student-logout/', views.student_logout, name='student_logout'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('session-home/', views.session_home, name='session_home'),
    
    # Admin routes
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    
    # Admin CRUD operations - Sessions
    path('manage/session/create/', views.admin_session_create, name='admin_session_create'),
    path('manage/session/<int:session_id>/view/', views.admin_session_view, name='admin_session_view'),
    path('manage/session/<int:session_id>/edit/', views.admin_session_edit, name='admin_session_edit'),
    path('manage/session/<int:session_id>/delete/', views.admin_session_delete, name='admin_session_delete'),
    
    # Admin CRUD operations - Questions
    path('manage/session/<int:session_id>/question/add/', views.admin_question_add, name='admin_question_add'),
    path('manage/question/<int:question_id>/edit/', views.admin_question_edit, name='admin_question_edit'),
    path('manage/question/<int:question_id>/delete/', views.admin_question_delete, name='admin_question_delete'),
    
    # Admin CRUD operations - Attendees
    path('manage/attendee/<int:attendee_id>/view/', views.admin_attendee_view, name='admin_attendee_view'),
    path('manage/attendee/<int:attendee_id>/edit/', views.admin_attendee_edit, name='admin_attendee_edit'),
    path('manage/attendee/<int:attendee_id>/delete/', views.admin_attendee_delete, name='admin_attendee_delete'),
    
    # Admin CRUD operations - Reviews
    path('manage/review/<int:review_id>/delete/', views.admin_review_delete, name='admin_review_delete'),
    path('manage/reviews/bulk-delete/', views.admin_bulk_delete_reviews, name='admin_bulk_delete_reviews'),
    path('manage/attendees/bulk-delete/', views.admin_bulk_delete_attendees, name='admin_bulk_delete_attendees'),
    
    path('submit-review/', views.submit_review, name='submit_review'),
    path('now_debug/', views.now_debug, name='now_debug'),
]