import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
import json
from subscription.models import SubscriptionPlan
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from users.models import UserProfile

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            # Create a new checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': 'price_XXXXXX',  # Replace with your price ID
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
                metadata={
                    'name': data.get('name'),
                    'email': data.get('email'),
                    'phone': data.get('phone'),
                    'address': data.get('address'),
                },
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def checkout(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    user_profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None

    context = {
        'plan_id': plan_id,
        'plan': plan,
        'user_profile': user_profile,
    }

    return render(request, 'checkout/checkout.html', context)


def order_overview(request, plan_id):
    try:
        plan = SubscriptionPlan.objects.get(pk=plan_id)
        data = {
            'name': plan.name,
            'description': plan.description,
            'price': plan.price,
            'image_url': plan.image.url,
            'duration': plan.duration,
            'benefit': plan.benefit,
        }
        return JsonResponse(data)
    except SubscriptionPlan.DoesNotExist:
        return JsonResponse({'error': 'Plan not found'}, status=404)
    
class SuccessView(TemplateView):
    template_name = 'checkout/success.html'

class CancelView(TemplateView):
    template_name = 'checkout/cancel.html'
