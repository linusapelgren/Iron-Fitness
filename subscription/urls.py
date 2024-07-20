#subscription/urls.py
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('subscription/', views.plans, name='plans'),
    path('subscription/<int:id>/', views.plan_details, name='plan_details'),
    path('subscribe/<int:id>/', views.subscribe, name='subscribe'),
    path('checkout/', include('checkout.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
