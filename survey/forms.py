from django import forms
import re
from .models import Attendee, Question, Review
from .models import ClassSession
from django import forms
from django.contrib.auth.hashers import make_password



class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'phone', 'email', 'age', 'place', 'class_session', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'class_session': forms.Select(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.fullmatch(r'\d{10}', phone):
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if not pwd or len(pwd) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        # Hash the password before saving to model instance
        self.instance.password = make_password(pwd)
        return pwd


class StudentLoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    class_session = forms.ModelChoiceField(queryset=ClassSession.objects.all())


class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = '__all__'
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }



class ResponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                label=question.text,
                choices=[
                    (1, question.option1),
                    (2, question.option2),
                    (3, question.option3),
                    (4, question.option4),
                ],
                widget=forms.RadioSelect,
                required=True
            )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['attendee', 'content']
        widgets = {
            'attendee': forms.Select(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your feedback'
            }),
        }