from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import profile_edit, CustomSignupView, profile_view, CustomPasswordChangeView, manage_subscription, cancel_subscription

urlpatterns = [
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('profile/', login_required(profile_view), name='profile_view'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('manage-subscription/', manage_subscription, name='manage_subscription'),
    path('cancel-subscription/', cancel_subscription, name='cancel_subscription'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


