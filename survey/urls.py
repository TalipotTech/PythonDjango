from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_response, name='submit_response'),    path('quiz/', views.quiz_view, name='quiz'),
     path('thank-you/', views.thank_you_view, name='thank_you'),    path('already-submitted/', views.already_submitted, name='already_submitted'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('submit-review/', views.submit_review, name='submit_review'),
     path('now_debug/', views.now_debug, name='now_debug'),
    path('post-login/', views.post_login, name='post_login'),


]