from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendee, Question, Response, ClassSession, Review, Admin, QuizProgress
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password, make_password
from .forms import AttendeeForm, StudentLoginForm, AdminLoginForm
from django.contrib import messages
from django.db.models import Count, Q

# Maximum minutes allowed per quiz attempt (cap per student attempt)
QUIZ_MAX_MINUTES = 15

def now_debug(request):
    return HttpResponse(f"server_now={timezone.now()}")



def home(request):
    """Homepage showing current and future events with countdowns"""
    from django.utils import timezone
    
    # Get current time in UTC (Django stores in UTC by default)
    now = timezone.now()
    
    # Get current sessions (started but not expired)
    current_sessions = ClassSession.objects.filter(
        start_time__lte=now,
        end_time__gte=now
    ).order_by('end_time')
    
    # Get future sessions (not started yet)
    future_sessions = ClassSession.objects.filter(
        start_time__gt=now
    ).order_by('start_time')
    
    # Calculate countdown for each session
    for session in current_sessions:
        time_diff = session.end_time - now
        session.countdown_days = time_diff.days
        session.countdown_hours, remainder = divmod(time_diff.seconds, 3600)
        session.countdown_minutes, session.countdown_seconds = divmod(remainder, 60)
        session.countdown_total_seconds = int(time_diff.total_seconds())
        session.status = 'current'
        # expose current attendee count via SessionAttendance related_name 'attendances'
        try:
            session.attendee_count = session.attendances.count()
        except Exception:
            session.attendee_count = 0
    
    for session in future_sessions:
        time_diff = session.start_time - now
        session.countdown_days = time_diff.days
        session.countdown_hours, remainder = divmod(time_diff.seconds, 3600)
        session.countdown_minutes, session.countdown_seconds = divmod(remainder, 60)
        session.countdown_total_seconds = int(time_diff.total_seconds())
        session.status = 'future'
        try:
            session.attendee_count = session.attendances.count()
        except Exception:
            session.attendee_count = 0
    
    context = {
        'current_sessions': current_sessions,
        'future_sessions': future_sessions,
        'now': timezone.localtime(now),  # Send local time to template for display
    }
    
    return render(request, 'survey/home.html', context)


def request_session_code(request, session_id):
    """Page where user enters email to receive session code"""
    try:
        session = ClassSession.objects.get(id=session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('home')
    
    code_sent = False
    email = ''
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address')
        else:
            # Store email in session for later use
            request.session['user_email'] = email
            request.session['pending_session_id'] = session.id
            
            # Send session code via SMTP if configured, otherwise fallback to email_utils
            code_sent = False
            try:
                from .smtp_email import generate_otp, send_session_code_smtp
                # Generate an OTP only for display; the app previously uses session.session_code
                otp = session.session_code or generate_otp(6)
                sender = None
                smtp_user = None
                smtp_password = None
                # Try to send via SMTP (Gmail) using environment variables if set
                sent_ok = send_session_code_smtp(
                    recipient_email=email,
                    otp=otp,
                    subject='your session code',
                    sender_email=sender,
                    smtp_user=smtp_user,
                    smtp_password=smtp_password,
                )
                if sent_ok:
                    code_sent = True
                    messages.success(request, f'Session code sent to {email}!')
                else:
                    raise Exception('SMTP send failed')
            except Exception:
                # Fall back to existing email_utils (file backend or configured django backend)
                try:
                    from .email_utils import send_session_code_email
                    send_session_code_email(
                        email=email,
                        name="Participant",
                        session_code=session.session_code,
                        session_title=session.title,
                        teacher=session.teacher
                    )
                    code_sent = True
                    messages.success(request, f'Session code saved/sent to {email}!')
                except Exception as e:
                    print(f"Email error fallback: {e}")
                    messages.error(request, 'Failed to send email. Please try again.')
    
    context = {
        'session': session,
        'code_sent': code_sent,
        'email': email,
    }
    
    return render(request, 'survey/request_session_code.html', context)


def verify_session_code(request, session_id):
    """Verify session code entered by user and proceed to registration"""
    try:
        session = ClassSession.objects.get(id=session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('home')
    
    if request.method == 'POST':
        entered_code = request.POST.get('session_code', '').strip().upper()
        email = request.POST.get('email', '').strip()
        
        if entered_code == session.session_code:
            # Code is correct! Check if user already exists
            existing_user = Attendee.objects.filter(email=email).first()
            
            if existing_user:
                # Returning user - go directly to login page
                request.session['verified_email'] = email
                request.session['verified_session_id'] = session.id
                request.session['verified_session_code'] = session.session_code
                request.session['registered_name'] = existing_user.name
                request.session['registered_email'] = existing_user.email
                request.session['registered_session_id'] = session.id  # Pass correct session
                
                messages.success(request, 'Welcome back! Please login with your password.')
                return redirect('new_participant_login')
            else:
                # New user - go to registration page
                request.session['verified_email'] = email
                request.session['verified_session_id'] = session.id
                request.session['verified_session_code'] = session.session_code
                
                messages.success(request, 'Session code verified! Please complete registration.')
                return redirect('new_participant_register')
        else:
            messages.error(request, 'Invalid session code. Please check your email and try again.')
            return redirect('request_session_code', session_id=session.id)
    
    return redirect('request_session_code', session_id=session.id)


def new_participant_register(request):
    """New registration page with auto-filled email and session code"""
    verified_email = request.session.get('verified_email')
    verified_session_id = request.session.get('verified_session_id')
    verified_session_code = request.session.get('verified_session_code')
    
    if not verified_email or not verified_session_id:
        messages.error(request, 'Please start from the beginning')
        return redirect('home')
    
    try:
        session = ClassSession.objects.get(id=verified_session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('home')
    
    # Check if user exists in database
    existing_user = Attendee.objects.filter(email=verified_email).first()
    
    # Pre-fill data
    prefill_name = existing_user.name if existing_user else ''
    prefill_phone = existing_user.phone if existing_user else ''
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not all([name, phone, password]):
            messages.error(request, 'Name, phone, and password are required')
            return render(request, 'survey/new_participant_register.html', {
                'session': session,
                'email': verified_email,
                'session_code': verified_session_code,
                'prefill_name': name or prefill_name,
                'prefill_phone': phone or prefill_phone,
            })
        
        # Create or update attendee
        if existing_user:
            # Update existing user
            existing_user.name = name
            existing_user.phone = phone
            existing_user.age = None  # No longer collecting age
            existing_user.place = ''  # No longer collecting place
            existing_user.password = make_password(password)
            existing_user.plain_password = password  # Store plain password for admin viewing
            existing_user.class_session = session
            existing_user.save()
            attendee = existing_user
        else:
            # Create new attendee (first time user)
            attendee = Attendee.objects.create(
                name=name,
                phone=phone,
                email=verified_email,
                age=None,  # No longer collecting age
                place='',  # No longer collecting place
                password=make_password(password),
                plain_password=password,  # Store plain password for admin viewing
                class_session=session
            )
        
        # Log them in directly (first time registration - skip login page)
        request.session['attendee_id'] = attendee.id
        request.session['class_session_id'] = session.id
        request.session['class_title'] = session.title
        
        # Create attendance record for this session
        from .models import SessionAttendance
        SessionAttendance.objects.get_or_create(
            attendee=attendee,
            class_session=session
        )
        
        # Clear verification data
        for key in ['verified_email', 'verified_session_id', 'verified_session_code']:
            if key in request.session:
                del request.session[key]
        
        messages.success(request, f'Welcome {name}! Registration successful.')
        return redirect('session_home')
    
    context = {
        'session': session,
        'email': verified_email,
        'session_code': verified_session_code,
        'prefill_name': prefill_name,
        'prefill_phone': prefill_phone,
    }
    
    return render(request, 'survey/new_participant_register.html', context)


def new_participant_login(request):
    """New login page with auto-filled name, email, session"""
    registered_name = request.session.get('registered_name')
    registered_email = request.session.get('registered_email')
    registered_session_id = request.session.get('registered_session_id')
    
    if not all([registered_name, registered_email, registered_session_id]):
        messages.error(request, 'Please register first')
        return redirect('home')
    
    try:
        session = ClassSession.objects.get(id=registered_session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('home')
    
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        
        if not password:
            messages.error(request, 'Please enter your password')
            return render(request, 'survey/new_participant_login.html', {
                'name': registered_name,
                'email': registered_email,
                'session': session,
            })
        
        # Find attendee and verify password
        try:
            attendee = Attendee.objects.get(
                name__iexact=registered_name,
                email=registered_email
            )
            
            if check_password(password, attendee.password):
                # Correct password - update session and log in
                attendee.class_session = session  # Update to new session
                attendee.save()
                
                # Create attendance record for this session
                from .models import SessionAttendance
                SessionAttendance.objects.get_or_create(
                    attendee=attendee,
                    class_session=session
                )
                
                request.session['attendee_id'] = attendee.id
                request.session['class_session_id'] = session.id
                request.session['class_title'] = session.title
                
                # Clear registration data
                for key in ['registered_name', 'registered_email', 'registered_session_id']:
                    if key in request.session:
                        del request.session[key]
                
                messages.success(request, f'Welcome, {attendee.name}!')
                return redirect('session_home')
            else:
                messages.error(request, 'Incorrect password')
        except Attendee.DoesNotExist:
            messages.error(request, 'User not found. Please register again.')
            return redirect('home')
    
    context = {
        'name': registered_name,
        'email': registered_email,
        'session': session,
    }
    
    return render(request, 'survey/new_participant_login.html', context)


def session_confirm(request, session_id):
    """Session confirmation page asking if user wants to attend"""
    try:
        session = ClassSession.objects.get(id=session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('home')
    
    from django.utils import timezone
    now = timezone.now()  # Use UTC for comparison
    
    # Calculate countdown
    if now < session.start_time:
        time_diff = session.start_time - now
        status = 'future'
    elif now <= session.end_time:
        time_diff = session.end_time - now
        status = 'current'
    else:
        messages.error(request, 'This session has already ended')
        return redirect('home')
    
    session.countdown_days = time_diff.days
    session.countdown_hours, remainder = divmod(time_diff.seconds, 3600)
    session.countdown_minutes, session.countdown_seconds = divmod(remainder, 60)
    session.countdown_total_seconds = int(time_diff.total_seconds())
    session.status = status
    
    # Handle form submission
    if request.method == 'POST':
        # Store session info and redirect to code entry
        request.session['pending_session_id'] = session.id
        return redirect('session_code_entry')
    
    context = {
        'session': session,
        'now': timezone.localtime(now),  # Send local time for display
        'start_time': timezone.localtime(session.start_time),
        'end_time': timezone.localtime(session.end_time),
    }
    
    return render(request, 'survey/session_confirm.html', context)


def session_code_entry(request):
    """Page where users enter session code to join"""
    if request.method == 'POST':
        session_code = request.POST.get('session_code', '').strip().upper()
        
        if not session_code:
            messages.error(request, 'Please enter a session code')
            return render(request, 'survey/session_code_entry.html')
        
        try:
            session = ClassSession.objects.get(session_code=session_code)
            
            # Check if session is valid (not expired)
            from django.utils import timezone
            now = timezone.localtime(timezone.now())
            
            if now > session.end_time:
                messages.error(request, f'Session "{session.title}" has already ended')
                return render(request, 'survey/session_code_entry.html')
            
            # Store session in session
            request.session['pending_session_id'] = session.id
            request.session['pending_session_code'] = session_code
            
            # Redirect to participant identification
            return redirect('participant_identify')
            
        except ClassSession.DoesNotExist:
            messages.error(request, 'Invalid session code. Please check and try again.')
            return render(request, 'survey/session_code_entry.html')
    
    return render(request, 'survey/session_code_entry.html')


def participant_identify(request):
    """Identify if participant is registered or new"""
    pending_session_id = request.session.get('pending_session_id')
    
    if not pending_session_id:
        messages.error(request, 'Please enter a session code first')
        return redirect('session_code_entry')
    
    try:
        session = ClassSession.objects.get(id=pending_session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('session_code_entry')
    
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        name = request.POST.get('name', '').strip()
        
        if not phone or not name:
            messages.error(request, 'Please enter both phone number and name')
            return render(request, 'survey/participant_identify.html', {'session': session})
        
        # Check if participant exists with this phone and name
        attendee = Attendee.objects.filter(
            phone=phone,
            name__iexact=name
        ).first()
        
        if attendee:
            # Existing participant - go to login page
            request.session['identified_attendee_id'] = attendee.id
            request.session['identified_phone'] = phone
            request.session['identified_name'] = name
            messages.info(request, f'Welcome back, {attendee.name}! Please enter your password to continue.')
            return redirect('participant_login')
        else:
            # New participant - go to registration page
            request.session['new_participant_phone'] = phone
            request.session['new_participant_name'] = name
            messages.info(request, 'Welcome! Please complete your registration.')
            return redirect('participant_register')
    
    context = {
        'session': session,
    }
    
    return render(request, 'survey/participant_identify.html', context)


def participant_register(request):
    """Registration page for new participants"""
    pending_session_id = request.session.get('pending_session_id')
    phone = request.session.get('new_participant_phone')
    name = request.session.get('new_participant_name')
    
    if not pending_session_id or not phone or not name:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('session_code_entry')
    
    try:
        session = ClassSession.objects.get(id=pending_session_id)
    except ClassSession.DoesNotExist:
        messages.error(request, 'Session not found')
        return redirect('session_code_entry')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            messages.error(request, 'Email and password are required')
            return render(request, 'survey/participant_register.html', {
                'session': session,
                'phone': phone,
                'name': name
            })
        
        # Create new attendee
        from django.contrib.auth.hashers import make_password
        attendee = Attendee.objects.create(
            name=name,
            phone=phone,
            email=email,
            age=None,  # No longer collecting age
            place='',  # No longer collecting place
            password=make_password(password),
            class_session=session
        )
        
        # Send welcome email with session code
        try:
            from .email_utils import send_session_code_email, send_welcome_email
            
            # Send welcome email
            send_welcome_email(attendee.email, attendee.name)
            
            # Send session code email
            send_session_code_email(
                email=attendee.email,
                name=attendee.name,
                session_code=session.session_code,
                session_title=session.title,
                teacher=session.teacher
            )
            messages.success(request, f'Registration successful! Check your email for session details.')
        except Exception as e:
            # Don't fail registration if email fails
            print(f"Email sending failed: {e}")
            messages.success(request, f'Registration successful! Welcome to {session.title}')
        
        # Log them in
        request.session['attendee_id'] = attendee.id
        request.session['class_session_id'] = session.id
        request.session['class_title'] = session.title
        
        # Clear temporary session data
        for key in ['pending_session_id', 'new_participant_phone', 'new_participant_name', 'pending_session_code']:
            if key in request.session:
                del request.session[key]
        
        return redirect('session_home')
    
    context = {
        'session': session,
        'phone': phone,
        'name': name,
    }
    
    return render(request, 'survey/participant_register.html', context)


def participant_login(request):
    """Login page for existing participants"""
    pending_session_id = request.session.get('pending_session_id')
    attendee_id = request.session.get('identified_attendee_id')
    
    if not pending_session_id or not attendee_id:
        messages.error(request, 'Session expired. Please start again.')
        return redirect('session_code_entry')
    
    try:
        session = ClassSession.objects.get(id=pending_session_id)
        attendee = Attendee.objects.get(id=attendee_id)
    except (ClassSession.DoesNotExist, Attendee.DoesNotExist):
        messages.error(request, 'Session or participant not found')
        return redirect('session_code_entry')
    
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        
        if not password:
            messages.error(request, 'Please enter your password')
            return render(request, 'survey/participant_login.html', {
                'session': session,
                'attendee': attendee
            })
        
        # Verify password
        from django.contrib.auth.hashers import check_password
        if check_password(password, attendee.password):
            # Update attendee's session
            attendee.class_session = session
            attendee.save()
            
            # Log them in
            request.session['attendee_id'] = attendee.id
            request.session['class_session_id'] = session.id
            request.session['class_title'] = session.title
            
            # Clear temporary session data
            for key in ['pending_session_id', 'identified_attendee_id', 'identified_phone', 'identified_name', 'pending_session_code']:
                if key in request.session:
                    del request.session[key]
            
            messages.success(request, f'Welcome back, {attendee.name}!')
            return redirect('session_home')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return render(request, 'survey/participant_login.html', {
                'session': session,
                'attendee': attendee
            })
    
    context = {
        'session': session,
        'attendee': attendee,
    }
    
    return render(request, 'survey/participant_login.html', context)


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
                        
                        # Clear pending session if exists
                        if 'pending_session_id' in request.session:
                            del request.session['pending_session_id']
                        
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
                        
                        # Clear pending session if exists
                        if 'pending_session_id' in request.session:
                            del request.session['pending_session_id']
                        
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
                
                # Clear pending session if exists
                if 'pending_session_id' in request.session:
                    del request.session['pending_session_id']
                
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
        
        # Pre-select session if coming from session_confirm
        pending_session_id = request.session.get('pending_session_id')
        if pending_session_id:
            try:
                pending_session = ClassSession.objects.get(id=pending_session_id)
                form.fields['class_session'].initial = pending_session
            except ClassSession.DoesNotExist:
                pass

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

    # ✅ Get or create quiz progress for this session
    quiz_progress, created = QuizProgress.objects.get_or_create(
        attendee=attendee,
        class_session=class_session
    )

    # Ensure progress/completion is up-to-date before computing stats
    quiz_progress.update_completion_status()
    progress_stats = quiz_progress.get_progress_stats()
    
    # Debug: Print progress stats
    print(f"DEBUG - Progress Stats: {progress_stats}")
    print(f"DEBUG - Answered IDs: {quiz_progress.get_answered_question_ids()}")

    # Get only unanswered questions (allows answering newly added questions)
    unanswered_questions = quiz_progress.get_unanswered_questions()
    
    # If all questions are answered and session is marked complete, show completion page
    if quiz_progress.is_fully_completed and progress_stats['pending'] == 0:
        return render(request, 'survey/already_submitted.html', {
            'attendee': attendee,
            'class_session': class_session,
            'progress_stats': progress_stats
        })
    
    # If no unanswered questions but not marked complete, update status
    if not unanswered_questions.exists():
        quiz_progress.update_completion_status()
        return render(request, 'survey/already_submitted.html', {
            'attendee': attendee,
            'class_session': class_session,
            'progress_stats': progress_stats
        })

    # ✅ POST branch - Quiz submission (only for unanswered questions)
    if request.method == "POST":
        print("POST data:", dict(request.POST))  # Debug

        saved_count = 0
        for q in unanswered_questions:
            # Handle both multiple choice and text response questions
            if q.question_type == 'text_response':
                key = f"text_question_{q.id}"
                text_answer = request.POST.get(key, '').strip()
                
                # Text responses are optional - only save if student provided an answer
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
                # Multiple choice question - required
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

        # Handle feedback/review submission (optional)
        feedback_content = request.POST.get('feedback_content', '').strip()
        if feedback_content:
            # Check if review already exists for this attendee and session
            existing_review = Review.objects.filter(
                attendee=attendee,
                content=feedback_content
            ).exists()
            
            if not existing_review:
                Review.objects.create(
                    attendee=attendee,
                    content=feedback_content,
                    feedback_type='quiz'  # Mark as quiz feedback
                )
                print(f"DEBUG - Quiz feedback saved: {feedback_content[:50]}...")

        if saved_count > 0:
            # Update quiz progress
            quiz_progress.update_completion_status()
            
            # Check if there are still more questions to answer
            remaining_unanswered = quiz_progress.get_unanswered_questions()
            
            if remaining_unanswered.exists():
                # Still have questions to answer
                messages.success(
                    request, 
                    f"✅ Saved {saved_count} answer(s)! You still have {remaining_unanswered.count()} question(s) remaining."
                )
                return redirect('quiz')
            else:
                # All questions answered
                return render(request, 'survey/thank_you.html', {
                    'attendee': attendee,
                    'class_session': class_session,
                    'saved_count': saved_count,
                    'progress_stats': quiz_progress.get_progress_stats()
                })

        # If nothing saved but feedback was provided, that's okay
        if feedback_content:
            messages.info(request, "✅ Feedback submitted successfully!")
            return redirect('quiz')
        
        # If nothing saved, show a clear message
        return render(request, 'survey/quiz.html', {
            'questions': unanswered_questions,
            'attendee': attendee,
            'class_session': class_session,
            'progress_stats': progress_stats,
            'error': "Please answer at least one question before submitting."
        })

    # ✅ GET branch - Display quiz (only unanswered questions)
    # Record quiz start time if not already recorded
    if not attendee.quiz_started_at:
        attendee.quiz_started_at = now
        attendee.save()

    # Calculate remaining time: 5 minutes per question
    MINUTES_PER_QUESTION = 5
    total_questions = Question.objects.filter(class_session=class_session).count()  # Total questions in the session
    quiz_allowed_seconds = total_questions * MINUTES_PER_QUESTION * 60
    
    time_elapsed = (now - attendee.quiz_started_at).total_seconds()
    time_remaining = max(0, int(quiz_allowed_seconds - time_elapsed))

    # If time has run out, auto-submit any pending answers and mark complete
    if time_remaining <= 0:
        quiz_progress.is_fully_completed = True
        quiz_progress.save()
        return render(request, 'survey/already_submitted.html', {
            'attendee': attendee,
            'class_session': class_session,
            'message': 'Time expired! Quiz auto-submitted.',
            'progress_stats': quiz_progress.get_progress_stats()
        })

    # Refresh progress stats right before rendering
    progress_stats = quiz_progress.get_progress_stats()
    
    # Debug: Print final progress stats
    print(f"DEBUG - Final Progress Stats before render: {progress_stats}")

    return render(request, 'survey/quiz.html', {
        'questions': unanswered_questions,
        'attendee': attendee,
        'class_session': class_session,
        'progress_stats': progress_stats,
        'time_remaining_seconds': time_remaining,
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
                content=content,
                feedback_type='review'  # Mark as general review
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

    now = timezone.now()  # Use UTC for comparison
    
    # Get or create quiz progress for this session
    quiz_progress, created = QuizProgress.objects.get_or_create(
        attendee=attendee,
        class_session=class_session
    )
    
    # Get progress statistics
    progress_stats = quiz_progress.get_progress_stats()
    
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
        'now': timezone.localtime(now),  # Send local time for display
        'start_time': timezone.localtime(class_session.start_time),
        'end_time': timezone.localtime(class_session.end_time),
        'progress_stats': progress_stats,
        'quiz_progress': quiz_progress,
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
    
    # Add attended sessions and submit status to each attendee
    from .models import SessionAttendance
    for attendee in recent_attendees:
        # Get all sessions this attendee has attended OR submitted responses for
        attended_via_attendance = SessionAttendance.objects.filter(attendee=attendee).values_list('class_session_id', flat=True)
        submitted_sessions = Response.objects.filter(attendee=attendee).values_list('question__class_session_id', flat=True).distinct()
        
        # Combine both to get all unique sessions
        all_session_ids = set(list(attended_via_attendance) + list(submitted_sessions))
        
        # Get the actual session objects
        attendee.attended_sessions_list = ClassSession.objects.filter(id__in=all_session_ids).order_by('-start_time')
        
        # Check if they have submitted responses for their CURRENT session
        if attendee.class_session:
            attendee.has_responses = Response.objects.filter(
                attendee=attendee,
                question__class_session=attendee.class_session
            ).exists()
        else:
            attendee.has_responses = False
    
    # Get recent reviews (last 5) with search - ONLY general reviews, NOT quiz feedback
    recent_reviews = Review.objects.filter(feedback_type='review').order_by('-submitted_at')
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
    
    # Calculate statistics (only for multiple choice questions)
    total_mc_questions = Question.objects.filter(
        class_session=attendee.class_session,
        question_type='multiple_choice'
    ).count() if attendee.class_session else 0
    
    total_responses = responses.count()
    
    # Only count correct answers for multiple choice questions
    correct_answers = sum(1 for r in responses if r.question.question_type == 'multiple_choice' and r.is_correct)
    
    # Calculate score based only on multiple choice questions
    score = round((correct_answers / total_mc_questions * 100) if total_mc_questions > 0 else 0, 2)
    
    # Separate responses by type
    mc_responses = [r for r in responses if r.question.question_type == 'multiple_choice']
    text_responses = [r for r in responses if r.question.question_type == 'text_response']
    
    # Check if student has submitted review
    has_reviewed = Review.objects.filter(attendee=attendee).exists()
    user_review = Review.objects.filter(attendee=attendee).first() if has_reviewed else None
    
    context = {
        'student_name': attendee.name,
        'attendee': attendee,
        'responses': responses,
        'mc_responses': mc_responses,
        'text_responses': text_responses,
        'total_mc_questions': total_mc_questions,
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
    
    # Get all sessions this attendee has participated in
    from .models import SessionAttendance
    attended_sessions = SessionAttendance.objects.filter(attendee=attendee).select_related('class_session')
    
    # Group responses by session
    sessions_data = []
    for attendance in attended_sessions:
        session = attendance.class_session
        
        # Get responses for this session
        session_responses = Response.objects.filter(
            attendee=attendee,
            question__class_session=session
        ).select_related('question')
        
        # Calculate session statistics
        total_mc_questions = Question.objects.filter(
            class_session=session,
            question_type='multiple_choice'
        ).count()
        
        mc_responses = [r for r in session_responses if r.question.question_type == 'multiple_choice']
        text_responses = [r for r in session_responses if r.question.question_type == 'text_response']
        
        correct_answers = sum(1 for r in mc_responses if r.is_correct)
        score = round((correct_answers / total_mc_questions * 100) if total_mc_questions > 0 else 0, 2)
        
        # Check submission status using QuizProgress
        quiz_progress = QuizProgress.objects.filter(
            attendee=attendee,
            class_session=session
        ).first()
        
        is_completed = quiz_progress.is_fully_completed if quiz_progress else False
        
        # Get feedback/reviews for this attendee (not session-specific)
        # We'll show all reviews but could filter by session if Review model had session field
        feedback = Review.objects.filter(attendee=attendee).order_by('-submitted_at')
        
        sessions_data.append({
            'session': session,
            'total_mc_questions': total_mc_questions,
            'mc_responses': mc_responses,
            'text_responses': text_responses,
            'correct_answers': correct_answers,
            'score': score,
            'is_completed': is_completed,
            'total_responses': len(mc_responses) + len(text_responses),
        })
    
    # Get all feedback/reviews from this attendee - ONLY quiz feedback
    attendee_feedback = Review.objects.filter(attendee=attendee, feedback_type='quiz').order_by('-submitted_at')
    
    context = {
        'attendee': attendee,
        'sessions_data': sessions_data,
        'attendee_feedback': attendee_feedback,
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


