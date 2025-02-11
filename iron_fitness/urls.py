from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import handler404
handler404 = "iron_fitness.views.handler404"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("home.urls")),
    path("subscription/", include("subscription.urls")),
    path("classes/", include("classes.urls")),
    path("users/", include("users.urls")),
    path("checkout/", include("checkout.urls")),
    path("contact/", include("contact.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
