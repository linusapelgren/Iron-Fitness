
# checkout/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('<int:plan_id>/', views.checkout, name='checkout'),
    path('order/<int:plan_id>/overview/', views.order_overview, name='order_overview'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
