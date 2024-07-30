from django import forms

class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(label='Email Address', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
