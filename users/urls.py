from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import profile_edit, CustomSignupView, profile_view

urlpatterns = [
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('profile/', login_required(profile_view), name='profile_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
