from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile

class NewsletterSignupForm(forms.Form):
    subscribe = forms.BooleanField(
        label="Subscribe to Newsletter",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'subscribe-checkbox'})
    )

    def save(self, user):
        # Get or create the user's profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.is_subscribed_to_newsletter = self.cleaned_data['subscribe']
        profile.save()
