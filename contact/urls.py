from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('contact/', views.contact_us, name='contact_us'),
    path('send_newsletter/', views.send_newsletter, name='send_newsletter'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
