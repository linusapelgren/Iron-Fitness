import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from subscription.models import SubscriptionPlan
from users.models import UserProfile
import json
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.models import User

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# views.py

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        plan_id = data.get('plan_id')
        
        try:
            plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
            amount_in_cents = int(plan.price * 100)

            # Create a charge
            charge = stripe.Charge.create(
                amount=amount_in_cents,
                currency='usd',
                description=f'Charge for plan {plan_id}',
                source=token,
            )

            # Assuming payment is successful, you may want to create a checkout session for webhook
            # or directly update the user profile here
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            user_profile.subscription_plan = plan
            user_profile.save()

            return JsonResponse({'success': True})

        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def checkout(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    user_profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None

    context = {
        'STRIPE_TEST_PUBLIC_KEY': settings.STRIPE_TEST_PUBLIC_KEY,
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
    
def success(request):
    return render(request, 'checkout/success.html')

import logging

logger = logging.getLogger(__name__)

# views.py

def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        logger.info(f"Received event: {event['type']}")
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.error(f"Webhook error: {e}")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return HttpResponse(status=200)

def handle_checkout_session(session):
    # Extract metadata from the session object
    plan_id = session.get('metadata', {}).get('plan_id')
    email = session.get('metadata', {}).get('email')

    if not plan_id or not email:
        logger.error("Missing plan_id or email in session metadata.")
        return

    try:
        user = User.objects.get(email=email)
        plan = SubscriptionPlan.objects.get(id=plan_id)

        # Update or create the user profile
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.subscription_plan = plan
        user_profile.save()

        logger.info(f"Successfully updated profile for {user.email} with plan {plan.name}")

    except User.DoesNotExist:
        logger.error(f"User with email {email} does not exist.")
    except SubscriptionPlan.DoesNotExist:
        logger.error(f"Subscription plan with ID {plan_id} does not exist.")