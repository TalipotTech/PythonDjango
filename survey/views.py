from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendee, Question, Response, ClassSession, Review
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from .forms import AttendeeForm, StudentLoginForm

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
            request.session['attendee_id'] = attendee.id
            request.session['class_session_id'] = attendee.class_session_id
            request.session['class_title'] = attendee.class_session.title
            return redirect('quiz')
    else:
        form = AttendeeForm()

    sessions = ClassSession.objects.all()
    sessions_json = json.dumps([
        {
            'id': s.id,
            'title': s.title,
            'teacher': s.teacher,
            'start_time': s.start_time.isoformat(),
            'end_time': s.end_time.isoformat()
        } for s in sessions
    ], cls=DjangoJSONEncoder)

    return render(request, 'survey/submit.html', {
        'sessions': sessions,
        'sessions_json': sessions_json,
        'form': form,
    })


def student_login(request):
    # Students log in with name + password + class session
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            class_session = form.cleaned_data['class_session']
            try:
                attendee = Attendee.objects.get(name=name, class_session=class_session)
                if attendee.password and check_password(password, attendee.password):
                    request.session['attendee_id'] = attendee.id
                    request.session['class_session_id'] = class_session.id
                    request.session['class_title'] = class_session.title
                    return redirect('quiz')
            except Attendee.DoesNotExist:
                pass
            # Invalid credentials
            return render(request, 'survey/student_login.html', {'form': form, 'error': 'Invalid credentials'})
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

    # Comment this out temporarily while testing submission, re-enable later
    # if Response.objects.filter(attendee=attendee).exists():
    #     return render(request, 'survey/already_submitted.html')

    questions = Question.objects.filter(class_session=class_session).order_by('id')

    # ✅ POST branch
    if request.method == "POST":
        print("POST data:", dict(request.POST))  # Debug

        saved_count = 0
        for q in questions:
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

    # ✅ GET branch
    return render(request, 'survey/quiz.html', {
        'questions': questions,
        'attendee': attendee,
        'class_session': class_session
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
def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_staff_user)
def admin_dashboard(request):
    attendees_qs = Attendee.objects.select_related('class_session').all()
    attendees = []

    for attendee in attendees_qs:
        responses = list(Response.objects.select_related('question').filter(attendee=attendee))
        total_attempted = len(responses)
        total_correct = sum(1 for r in responses if r.is_correct)
        score_percent = round((total_correct / total_attempted) * 100, 2) if total_attempted else 0

        attendees.append({
            'name': attendee.name,
            'email': attendee.email,
            'class_session': attendee.class_session,
            'responses': responses,
            'total_attempted': total_attempted,
            'total_correct': total_correct,
            'score_percent': score_percent,
        })

    return render(request, 'survey/admin_dashboard.html', {'attendees': attendees})


@login_required
def post_login(request):
    # Redirect users based on role after successful login.
    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('home')
