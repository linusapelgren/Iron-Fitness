from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile

class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(label="Your Email Address", widget=forms.EmailInput(attrs={'class': 'form-control'}))

