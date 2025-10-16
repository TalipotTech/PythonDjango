from django import forms
import re
from .models import Attendee, Question, Review, Admin
from .models import ClassSession
from django.contrib.auth.hashers import make_password


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Admin username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class AttendeeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password'}), 
        min_length=6, 
        required=True,  # Made mandatory
        help_text="At least 6 characters with mix of letters and numbers recommended"
    )
    
    class Meta:
        model = Attendee
        fields = ['name', 'phone', 'email', 'password']  # Removed class_session
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.fullmatch(r'\d{10}', phone):
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        
        # Check for duplicate phone (excluding current instance if editing)
        qs = Attendee.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This phone number is already registered.")
        
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check for duplicate email (excluding current instance if editing)
        qs = Attendee.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already registered.")
        
        return email

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        
        # Password is now mandatory
        if not pwd:
            raise forms.ValidationError("Password is required.")
            
        # Validate password
        if len(pwd) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        
        # Password strength validation
        has_letter = any(c.isalpha() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        
        if not (has_letter and has_digit):
            raise forms.ValidationError("Password should contain both letters and numbers for better security.")
        
        # Return raw here; we'll hash in save() to avoid being overwritten by ModelForm internals
        return pwd

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Always hash the password before saving to DB if provided
        raw_pwd = self.cleaned_data.get('password')
        if raw_pwd:
            instance.password = make_password(raw_pwd)
        if commit:
            instance.save()
        return instance


class StudentLoginForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your full name'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }), min_length=1)
    class_session = forms.ModelChoiceField(queryset=ClassSession.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control'
    }))


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