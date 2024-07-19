from django.urls import path
from .views import profile_edit, CustomSignupView

urlpatterns = [
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
]