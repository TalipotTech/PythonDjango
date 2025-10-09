from django import forms
from .models import Attendee, Question, Review
from .models import ClassSession



class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'phone', 'email', 'age', 'place', 'class_session']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'class_session': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.fullmatch(r'\d{10}', phone):
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone


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