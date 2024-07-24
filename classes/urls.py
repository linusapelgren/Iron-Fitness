from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_class, name='book_class'),
    path('ajax/load-times/', views.load_times, name='ajax_load_times'),
    path('success/', views.success_url, name='successful_booking'),
]
