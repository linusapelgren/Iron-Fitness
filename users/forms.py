from django import forms
from allauth.account.forms import SignupForm
from .models import UserProfile


class CustomSignupForm(SignupForm):
    """Form for custom user signup"""

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for user profile"""

    class Meta:
        model = UserProfile
        fields = [
            "phone_number",
            "picture",
            "street_address",
            "city",
            "postal_code",
            "country",
        ]
