from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendee, Question, Response, ClassSession, Review, Admin
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password, make_password
from .forms import AttendeeForm, StudentLoginForm, AdminLoginForm
from django.contrib import messages
from django.db.models import Count, Q

def now_debug(request):
    return HttpResponse(f"server_now={timezone.now()}")



def home(request):
    return render(request, 'survey/home.html')

def submit_response(request):
    # Student signup/registration (creates an attendee with password)
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            
            # Success message with detailed info
            messages.success(
                request, 
                f"🎉 Registration Complete! Welcome {attendee.name}! "
                f"Please login and select your class to start your quiz."
            )
            
            # Redirect to student login page instead of starting quiz directly
            return redirect('student_login')
    else:
        form = AttendeeForm()

    return render(request, 'survey/submit.html', {
        'form': form,
    })


def student_login(request):
    # Students log in with name + password + class session
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            # Normalize inputs
            name = ' '.join(form.cleaned_data['name'].split())
            password = form.cleaned_data['password']
            class_session = form.cleaned_data['class_session']

            attendee = Attendee.objects.filter(name__iexact=name).first()
            if attendee and attendee.password:
                pwd = attendee.password
                # Recognize Django-hashed formats
                if pwd.startswith('pbkdf2_') or pwd.startswith('argon2$') or pwd.startswith('bcrypt') or pwd.startswith('sha1$'):
                    if check_password(password, pwd):
                        # Update attendee's class_session
                        attendee.class_session = class_session
                        attendee.save()
                        
                        request.session['attendee_id'] = attendee.id
                        request.session['class_session_id'] = class_session.id
                        request.session['class_title'] = class_session.title
                        return redirect('session_home')  # Redirect to session home instead of quiz
                else:
                    # Legacy plaintext stored; compare directly and upgrade to hashed on success
                    if pwd == password:
                        from django.contrib.auth.hashers import make_password
                        attendee.password = make_password(password)
                        attendee.class_session = class_session
                        attendee.save()
                        
                        request.session['attendee_id'] = attendee.id
                        request.session['class_session_id'] = class_session.id
                        request.session['class_title'] = class_session.title
                        return redirect('session_home')  # Redirect to session home instead of quiz

            # If attendee exists but has no password saved yet, accept the provided password as initial
            if attendee and not attendee.password and password:
                from django.contrib.auth.hashers import make_password
                attendee.password = make_password(password)
                attendee.class_session = class_session
                attendee.save()
                
                request.session['attendee_id'] = attendee.id
                request.session['class_session_id'] = class_session.id
                request.session['class_title'] = class_session.title
                return redirect('session_home')  # Redirect to session home instead of quiz

            # Invalid credentials: clarify whether attendee missing or wrong password
            if not attendee:
                error = 'No student found with that name.'
            else:
                error = 'Incorrect password. Please try again or contact your instructor.'
            return render(request, 'survey/student_login.html', {
                'form': form,
                'error': error
            })
    else:
        form = StudentLoginForm()

    return render(request, 'survey/student_login.html', {'form': form})



def quiz_view(request):
    attendee_id = request.session.get('attendee_id')
    class_session_id = request.session.get('class_session_id')

    if not attendee_id or not class_session_id:
        return redirect('submit_response')

    try:
        class_session = ClassSession.objects.get(id=class_session_id)
    except ClassSession.DoesNotExist:
        return redirect('submit_response')

    now = timezone.localtime(timezone.now())

    if not class_session.start_time or not class_session.end_time:
        return render(request, 'survey/expired.html', {
            'message': "Session time is not configured properly.",
            'start': None,
            'end': None,
            'class_session': class_session
        })

    if now < class_session.start_time:
        return render(request, 'survey/expired.html', {
            'message': "⏳ Quiz Not Yet Started",
            'start': timezone.localtime(class_session.start_time),
            'end': timezone.localtime(class_session.end_time),
            'class_session': class_session
        })

    if now > class_session.end_time:
        return render(request, 'survey/expired.html', {
            'message': "⏰ Session Expired",
            'start': timezone.localtime(class_session.start_time),
            'end': timezone.localtime(class_session.end_time),
            'class_session': class_session
        })

    try:
        attendee = Attendee.objects.get(id=attendee_id)
    except Attendee.DoesNotExist:
        return redirect('submit_response')

    # ✅ Check if already submitted - PREVENT RETAKES
    if attendee.has_submitted or Response.objects.filter(attendee=attendee).exists():
        return render(request, 'survey/already_submitted.html', {
            'attendee': attendee,
            'class_session': class_session
        })

    questions = Question.objects.filter(class_session=class_session).order_by('id')

    # ✅ POST branch - Quiz submission
    if request.method == "POST":
        print("POST data:", dict(request.POST))  # Debug

        saved_count = 0
        for q in questions:
            # Handle both multiple choice and text response questions
            if q.question_type == 'text_response':
                key = f"text_question_{q.id}"
                text_answer = request.POST.get(key, '').strip()
                
                if not text_answer:
                    continue
                
                # Prevent duplicates per question for this attendee
                if Response.objects.filter(attendee=attendee, question=q).exists():
                    continue
                
                Response.objects.create(
                    attendee=attendee,
                    question=q,
                    text_response=text_answer
                )
                saved_count += 1
            else:
                # Multiple choice question
                key = f"question_{q.id}"
                selected_option = request.POST.get(key)  # "1", "2", "3", or "4"
                
                if not selected_option:
                    continue

                # Prevent duplicates per question for this attendee
                if Response.objects.filter(attendee=attendee, question=q).exists():
                    continue

                Response.objects.create(
                    attendee=attendee,
                    question=q,
                    selected_option=int(selected_option)
                )
                saved_count += 1

        if saved_count > 0:
            # Mark as submitted to prevent retakes
            attendee.has_submitted = True
            attendee.save()
            
            return render(request, 'survey/thank_you.html', {
                'attendee': attendee,
                'class_session': class_session,
                'saved_count': saved_count
            })

        # If nothing saved, show a clear message
        return render(request, 'survey/quiz.html', {
            'questions': questions,
            'attendee': attendee,
            'class_session': class_session,
            'error': "Please select an option for at least one question before submitting."
        })

    # ✅ GET branch - Starting the quiz
    # Record quiz start time if not already recorded
    if not attendee.quiz_started_at:
        attendee.quiz_started_at = now
        attendee.save()

    # Calculate remaining time
    time_elapsed = (now - attendee.quiz_started_at).total_seconds()
    session_duration = (class_session.end_time - class_session.start_time).total_seconds()
    time_remaining = max(0, session_duration - time_elapsed)

    # If time has run out, auto-submit
    if time_remaining <= 0:
        attendee.has_submitted = True
        attendee.save()
        return render(request, 'survey/already_submitted.html', {
            'attendee': attendee,
            'class_session': class_session,
            'message': 'Time expired! Quiz auto-submitted.'
        })

    return render(request, 'survey/quiz.html', {
        'questions': questions,
        'attendee': attendee,
        'class_session': class_session,
        'time_remaining_seconds': int(time_remaining),
        'quiz_started_at': attendee.quiz_started_at,
    })

def submit_quiz(request):
    if request.method == 'POST':
        attendee_id = request.session.get('attendee_id')
        class_session_id = request.session.get('class_session_id')

        attendee = Attendee.objects.get(id=attendee_id)
        class_session = ClassSession.objects.get(id=class_session_id)
        questions = Question.objects.filter(class_session=class_session)

        for question in questions:
            selected = int(request.POST.get(f'question_{question.id}', 0))
            Response.objects.create(
                attendee=attendee,
                question=question,
                selected_option=selected
            )

        return redirect('thank_you')

    return redirect('quiz')

def thank_you_view(request):
    return render(request, 'survey/thank_you.html')

def already_submitted(request):
    return render(request, 'survey/already_submitted.html')

def expired_view(request):
    return render(request, 'survey/expired.html')
def submit_review(request):
    attendee = None
    attendee_id = request.session.get('attendee_id')
    if attendee_id:
        try:
            attendee = Attendee.objects.get(id=attendee_id)
        except Attendee.DoesNotExist:
            attendee = None

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Review.objects.create(
                attendee=attendee,  # can be None if you allow it
                content=content
            )
            return redirect('thank_you')

    return render(request, 'survey/submit_review.html', {'attendee': attendee})
def student_logout(request):
    # Clear attendee session and return home
    request.session.flush()
    return redirect('home')


def session_home(request):
    """Session home page showing countdown and session status"""
    attendee_id = request.session.get('attendee_id')
    class_session_id = request.session.get('class_session_id')

    if not attendee_id or not class_session_id:
        messages.error(request, 'Please login first')
        return redirect('student_login')

    try:
        attendee = Attendee.objects.get(id=attendee_id)
        class_session = ClassSession.objects.get(id=class_session_id)
    except (Attendee.DoesNotExist, ClassSession.DoesNotExist):
        messages.error(request, 'Session or student not found')
        return redirect('student_login')

    now = timezone.localtime(timezone.now())
    
    # Calculate time differences
    if now < class_session.start_time:
        # Session hasn't started yet - show countdown
        time_diff = class_session.start_time - now
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        status = 'waiting'
        status_message = '⏳ Quiz Not Yet Started'
        countdown = {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'total_seconds': int(time_diff.total_seconds())
        }
    elif now >= class_session.start_time and now <= class_session.end_time:
        # Session is active
        time_diff = class_session.end_time - now
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        status = 'active'
        status_message = '✅ Quiz is Active Now!'
        countdown = {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'total_seconds': int(time_diff.total_seconds())
        }
    else:
        # Session has expired
        status = 'expired'
        status_message = '⏰ Session Expired'
        countdown = None

    context = {
        'attendee': attendee,
        'class_session': class_session,
        'status': status,
        'status_message': status_message,
        'countdown': countdown,
        'now': now,
        'start_time': timezone.localtime(class_session.start_time),
        'end_time': timezone.localtime(class_session.end_time),
    }

    return render(request, 'survey/session_home.html', context)


# ============= ADMIN VIEWS =============

def admin_login(request):
    """Admin login view - separate from student login"""
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                admin = Admin.objects.get(username=username)
                if check_password(password, admin.password):
                    # Set admin session
                    request.session['admin_id'] = admin.id
                    request.session['admin_username'] = admin.username
                    request.session['is_admin'] = True
                    messages.success(request, f'Welcome back, {admin.username}!')
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Invalid username or password')
            except Admin.DoesNotExist:
                messages.error(request, 'Invalid username or password')
    else:
        form = AdminLoginForm()
    
    return render(request, 'survey/admin_login.html', {'form': form})


def admin_dashboard(request):
    """Admin dashboard view with statistics and data"""
    # Check if admin is logged in
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin to access this page')
        return redirect('admin_login')
    
    # Get search query from GET parameters
    search_query = request.GET.get('search', '').strip()
    session_filter = request.GET.get('session_filter', 'all')
    search_filter = request.GET.get('search_filter', 'all')
    
    # Get statistics
    total_attendees = Attendee.objects.count()
    total_sessions = ClassSession.objects.count()
    total_questions = Question.objects.count()
    total_responses = Response.objects.count()
    
    # Get all sessions with attendee counts and status
    sessions = ClassSession.objects.all().order_by('-start_time')
    
    # Filter sessions by status if requested
    if session_filter != 'all':
        from django.utils import timezone
        now = timezone.localtime(timezone.now())
        if session_filter == 'active':
            sessions = sessions.filter(start_time__lte=now, end_time__gte=now)
        elif session_filter == 'inactive':
            sessions = sessions.filter(start_time__gt=now)
        elif session_filter == 'finished':
            sessions = sessions.filter(end_time__lt=now)
    
    # Search sessions by title or teacher (if search filter allows)
    if search_query and search_filter in ['all', 'sessions']:
        sessions = sessions.filter(
            Q(title__icontains=search_query) | 
            Q(teacher__icontains=search_query)
        )
    elif search_filter == 'sessions' and not search_query:
        pass  # Show all sessions
    elif search_filter not in ['all', 'sessions']:
        sessions = ClassSession.objects.none()  # Hide sessions if filtering by other types
    
    # Get recent attendees (last 10) with search
    recent_attendees = Attendee.objects.all().order_by('-id')
    if search_query and search_filter in ['all', 'attendees']:
        recent_attendees = recent_attendees.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    elif search_filter == 'attendees' and not search_query:
        pass  # Show all attendees
    elif search_filter not in ['all', 'attendees']:
        recent_attendees = Attendee.objects.none()  # Hide attendees if filtering by other types
    recent_attendees = recent_attendees[:10]
    
    # Get recent reviews (last 5) with search
    recent_reviews = Review.objects.all().order_by('-submitted_at')
    if search_query and search_filter in ['all', 'reviews']:
        recent_reviews = recent_reviews.filter(
            Q(content__icontains=search_query) |
            Q(attendee__name__icontains=search_query)
        )
    elif search_filter == 'reviews' and not search_query:
        pass  # Show all reviews
    elif search_filter not in ['all', 'reviews']:
        recent_reviews = Review.objects.none()  # Hide reviews if filtering by other types
    recent_reviews = recent_reviews[:5]
    
    # Add session status to each session
    from django.utils import timezone
    now = timezone.localtime(timezone.now())
    for session in sessions:
        if now < session.start_time:
            session.status = 'inactive'
            session.status_label = '⏳ Inactive'
            session.status_class = 'badge-warning'
        elif session.start_time <= now <= session.end_time:
            session.status = 'active'
            session.status_label = '✅ Active'
            session.status_class = 'badge-success'
        else:
            session.status = 'finished'
            session.status_label = '🔴 Finished'
            session.status_class = 'badge-danger'
    
    context = {
        'admin_username': request.session.get('admin_username'),
        'total_attendees': total_attendees,
        'total_sessions': total_sessions,
        'total_questions': total_questions,
        'total_responses': total_responses,
        'sessions': sessions,
        'recent_attendees': recent_attendees,
        'recent_reviews': recent_reviews,
        'search_query': search_query,
        'session_filter': session_filter,
        'search_filter': search_filter,
        'now': now,
    }
    
    return render(request, 'survey/admin_dashboard.html', context)


def admin_logout(request):
    """Logout admin and clear session"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully')
    return redirect('admin_login')


def student_dashboard(request):
    """Student dashboard showing their info, quiz status, and responses"""
    # Check if student is logged in
    attendee_id = request.session.get('attendee_id')
    if not attendee_id:
        messages.error(request, 'Please login to access your dashboard')
        return redirect('student_login')
    
    try:
        attendee = Attendee.objects.get(id=attendee_id)
    except Attendee.DoesNotExist:
        messages.error(request, 'Student not found')
        return redirect('student_login')
    
    # Get student's responses
    responses = Response.objects.filter(attendee=attendee).select_related('question')
    
    # Calculate statistics
    total_questions = Question.objects.filter(class_session=attendee.class_session).count()
    total_responses = responses.count()
    correct_answers = sum(1 for r in responses if r.is_correct)
    score = round((correct_answers / total_questions * 100) if total_questions > 0 else 0, 2)
    
    # Check if student has submitted review
    has_reviewed = Review.objects.filter(attendee=attendee).exists()
    user_review = Review.objects.filter(attendee=attendee).first() if has_reviewed else None
    
    context = {
        'student_name': attendee.name,
        'attendee': attendee,
        'responses': responses,
        'total_questions': total_questions,
        'total_responses': total_responses,
        'correct_answers': correct_answers,
        'score': score,
        'has_reviewed': has_reviewed,
        'user_review': user_review,
    }
    
    return render(request, 'survey/student_dashboard.html', context)


# ============= ADMIN CRUD OPERATIONS =============

def admin_session_view(request, session_id):
    """View detailed information about a session"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        session = ClassSession.objects.get(id=session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('admin_dashboard')
    
    # Get session statistics
    attendees = Attendee.objects.filter(class_session=session)
    questions = Question.objects.filter(class_session=session).order_by('id')
    responses = Response.objects.filter(question__class_session=session)
    
    # Calculate session status
    from django.utils import timezone
    now = timezone.localtime(timezone.now())
    if now < session.start_time:
        status = 'inactive'
        status_label = '⏳ Inactive (Not Started)'
    elif session.start_time <= now <= session.end_time:
        status = 'active'
        status_label = '✅ Active'
    else:
        status = 'finished'
        status_label = '🔴 Finished'
    
    context = {
        'session': session,
        'attendees': attendees,
        'questions': questions,
        'total_responses': responses.count(),
        'status': status,
        'status_label': status_label,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'survey/admin_session_view.html', context)


def admin_question_add(request, session_id):
    """Add a new question to a session"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        session = ClassSession.objects.get(id=session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        text = request.POST.get('text')
        question_type = request.POST.get('question_type', 'multiple_choice')
        
        if question_type == 'text_response':
            # For text response questions, no options needed
            if text:
                Question.objects.create(
                    class_session=session,
                    text=text,
                    question_type='text_response'
                )
                messages.success(request, 'Text response question added successfully!')
                return redirect('admin_session_view', session_id=session_id)
            else:
                messages.error(request, 'Question text is required')
        else:
            # For multiple choice questions
            option1 = request.POST.get('option1')
            option2 = request.POST.get('option2')
            option3 = request.POST.get('option3')
            option4 = request.POST.get('option4')
            correct_option = request.POST.get('correct_option')
            
            if all([text, option1, option2, option3, option4, correct_option]):
                Question.objects.create(
                    class_session=session,
                    text=text,
                    question_type='multiple_choice',
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    correct_option=int(correct_option)
                )
                messages.success(request, 'Multiple choice question added successfully!')
                return redirect('admin_session_view', session_id=session_id)
            else:
                messages.error(request, 'All fields are required for multiple choice questions')
    
    context = {
        'session': session,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'survey/admin_question_add.html', context)


def admin_question_edit(request, question_id):
    """Edit an existing question"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        question.text = request.POST.get('text')
        question_type = request.POST.get('question_type', question.question_type)
        question.question_type = question_type
        
        if question_type == 'text_response':
            # Clear options for text response questions
            question.option1 = None
            question.option2 = None
            question.option3 = None
            question.option4 = None
            question.correct_option = None
        else:
            # Update options for multiple choice
            question.option1 = request.POST.get('option1')
            question.option2 = request.POST.get('option2')
            question.option3 = request.POST.get('option3')
            question.option4 = request.POST.get('option4')
            question.correct_option = int(request.POST.get('correct_option'))
        
        question.save()
        messages.success(request, 'Question updated successfully!')
        return redirect('admin_session_view', session_id=question.class_session.id)
    
    context = {
        'question': question,
        'session': question.class_session,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'survey/admin_question_edit.html', context)


def admin_question_delete(request, question_id):
    """Delete a question"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        question = Question.objects.get(id=question_id)
        session_id = question.class_session.id
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('admin_session_view', session_id=session_id)
    except Question.DoesNotExist:
        messages.error(request, 'Question not found')
        return redirect('admin_dashboard')


def admin_session_create(request):
    """Create a new session"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        teacher = request.POST.get('teacher')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        if title and teacher and start_time and end_time:
            session = ClassSession.objects.create(
                title=title,
                teacher=teacher,
                start_time=start_time,
                end_time=end_time
            )
            messages.success(request, f'Session "{session.title}" created successfully!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'All fields are required')
    
    context = {
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'survey/admin_session_edit.html', context)


def admin_session_edit(request, session_id):
    """Edit a session"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        session = ClassSession.objects.get(id=session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        session.title = request.POST.get('title')
        session.teacher = request.POST.get('teacher')
        session.start_time = request.POST.get('start_time')
        session.end_time = request.POST.get('end_time')
        session.save()
        messages.success(request, f'Session "{session.title}" updated successfully!')
        return redirect('admin_dashboard')
    
    context = {
        'session': session,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'survey/admin_session_edit.html', context)


def admin_session_delete(request, session_id):
    """Delete a session"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        session = ClassSession.objects.get(id=session_id)
        session_title = session.title
        session.delete()
        messages.success(request, f'Session "{session_title}" deleted successfully!')
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
    
    return redirect('admin_dashboard')


def admin_attendee_view(request, attendee_id):
    """View detailed information about an attendee"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        attendee = Attendee.objects.get(id=attendee_id)
    except Attendee.DoesNotExist:
        messages.error(request, 'Attendee not found')
        return redirect('admin_dashboard')
    
    # Get attendee's responses
    responses = Response.objects.filter(attendee=attendee).select_related('question')
    
    # Calculate statistics
    total_questions = Question.objects.filter(class_session=attendee.class_session).count() if attendee.class_session else 0
    total_responses = responses.count()
    correct_answers = sum(1 for r in responses if r.is_correct)
    score = round((correct_answers / total_questions * 100) if total_questions > 0 else 0, 2)
    
    context = {
        'attendee': attendee,
        'responses': responses,
        'total_questions': total_questions,
        'total_responses': total_responses,
        'correct_answers': correct_answers,
        'score': score,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'survey/admin_attendee_view.html', context)


def admin_attendee_edit(request, attendee_id):
    """Edit an attendee"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        attendee = Attendee.objects.get(id=attendee_id)
    except Attendee.DoesNotExist:
        messages.error(request, 'Attendee not found')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        attendee.name = request.POST.get('name')
        attendee.email = request.POST.get('email')
        attendee.phone = request.POST.get('phone')
        attendee.age = request.POST.get('age') or None
        attendee.place = request.POST.get('place', '')
        
        # Handle class session
        class_session_id = request.POST.get('class_session')
        if class_session_id:
            try:
                attendee.class_session = ClassSession.objects.get(id=class_session_id)
            except ClassSession.DoesNotExist:
                pass
        
        attendee.save()
        messages.success(request, f'Attendee "{attendee.name}" updated successfully!')
        return redirect('admin_dashboard')
    
    sessions = ClassSession.objects.all()
    context = {
        'attendee': attendee,
        'sessions': sessions,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'survey/admin_attendee_edit.html', context)


def admin_attendee_delete(request, attendee_id):
    """Delete an attendee"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        attendee = Attendee.objects.get(id=attendee_id)
        attendee_name = attendee.name
        attendee.delete()
        messages.success(request, f'Attendee "{attendee_name}" deleted successfully!')
    except Attendee.DoesNotExist:
        messages.error(request, 'Attendee not found')
    
    return redirect('admin_dashboard')


def admin_review_delete(request, review_id):
    """Delete a review"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    try:
        review = Review.objects.get(id=review_id)
        review.delete()
        messages.success(request, 'Review deleted successfully!')
    except Review.DoesNotExist:
        messages.error(request, 'Review not found')
    
    return redirect('admin_dashboard')


def admin_bulk_delete_reviews(request):
    """Bulk delete reviews"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    if request.method == 'POST':
        review_ids = request.POST.getlist('review_ids')
        if review_ids:
            count = Review.objects.filter(id__in=review_ids).delete()[0]
            messages.success(request, f'{count} review(s) deleted successfully!')
        else:
            messages.warning(request, 'No reviews selected')
    
    return redirect('admin_dashboard')


def admin_bulk_delete_attendees(request):
    """Bulk delete attendees"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Please login as admin')
        return redirect('admin_login')
    
    if request.method == 'POST':
        attendee_ids = request.POST.getlist('attendee_ids')
        if attendee_ids:
            count = Attendee.objects.filter(id__in=attendee_ids).delete()[0]
            messages.success(request, f'{count} attendee(s) deleted successfully!')
        else:
            messages.warning(request, 'No attendees selected')
    
    return redirect('admin_dashboard')


