from django.urls import path
from .views import (
    process_payment,
    checkout,
    order_overview,
    success,
    stripe_webhook,
)


urlpatterns = [
    path("process-payment/", process_payment, name="process_payment"),
    path("<int:plan_id>/", checkout, name="checkout"),
    path(
        "order/<int:plan_id>/overview/",
        order_overview,
        name="order_overview",
    ),
    path("success/", success, name="success"),
    path("stripe/webhooks/", stripe_webhook, name="stripe-webhook"),
]
