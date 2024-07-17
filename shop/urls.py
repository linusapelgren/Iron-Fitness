from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplements, name='supplements'),  # Update 'shop' to 'supplements'
]