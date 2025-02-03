from allauth.account.forms import SignupForm
from django import forms
from .models import UserProfile


class CustomSignupForm(SignupForm):
    """Form for custom user signup"""

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    street_address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    postal_code = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)

    def save(self, request):
        # Save the user instance first
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()

        # Create or update the UserProfile instance
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "phone_number": self.cleaned_data["phone_number"],
                "street_address": self.cleaned_data["street_address"],
                "city": self.cleaned_data["city"],
                "postal_code": self.cleaned_data["postal_code"],
                "country": self.cleaned_data["country"],
            },
        )

        return user


class UserProfileForm(forms.ModelForm):
    """Form for user profile"""

    class Meta:
        model = UserProfile
        fields = [
            "phone_number",
            "street_address",
            "city",
            "postal_code",
            "country",
        ]
