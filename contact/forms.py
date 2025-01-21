from django import forms

class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address', 'id': 'newsletter-email', })  # Add the placeholder
    )