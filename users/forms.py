from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from allauth.account.forms import SignupForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'picture', 'address']

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    def save(self, request, commit=True):
        user = super().save(request, commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        phone_number = self.cleaned_data['phone_number']
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.phone_number = phone_number
        if commit:
            user_profile.save()

        return user