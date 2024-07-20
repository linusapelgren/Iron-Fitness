from django.urls import path
from . import views

urlpatterns = [
    path('subscription/', views.plans, name='plans'),
    path('subscription/<int:id>/', views.plan_details, name='plan_details'),
    path('subscribe/<int:id>/', views.subscribe, name='subscribe'),
]
