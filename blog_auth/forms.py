from django import forms
from django.contrib.auth import get_user_model
from .models import Capture

User = get_user_model()

class SignupForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': 'Username is required',
        'max_length': 'Username cannot exceed 20 characters',
        'min_length': 'Username must be at least 2 characters long'
    })
    email = forms.EmailField(error_messages={
        'required': 'Email is required',
        'invalid': 'Enter a valid email address'
    })
    captcha = forms.CharField(error_messages={
        'required': 'Captcha is required'
    })
    password = forms.CharField(max_length=25, min_length=6, widget=forms.PasswordInput, error_messages={
        'required': 'Password is required',
        'max_length': 'Password cannot exceed 25 characters',
        'min_length': 'Password must be at least 6 characters long'
    })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exist = User.objects.filter(email=email).exists()
        if exist:
            raise forms.ValidationError('Email is already in use')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')
        
        capture = Capture.objects.filter(email=email, code=captcha).first()
        if not capture:
            raise forms.ValidationError('Unmatched email and captcha')
        else:
            capture.delete()
        
        return captcha
