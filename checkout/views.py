import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect
from django.views.generic import TemplateView

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://localhost:8000"  # Replace with your actual domain

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': 'price_1J6aA9LHDzHpXRYjIOl5dxz2',  # Replace with your actual Price ID
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=YOUR_DOMAIN + '/checkout/success/',
                cancel_url=YOUR_DOMAIN + '/checkout/cancel/',
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}), 400

class SuccessView(TemplateView):
    template_name = 'checkout/success.html'

class CancelView(TemplateView):
    template_name = 'checkout/cancel.html'
