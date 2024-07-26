#subscription/views.py
from django.shortcuts import render, get_object_or_404
from .models import SubscriptionPlan
from django.http import JsonResponse
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from users.models import UserProfile

def plans(request):
    """ A view to show the plans page """
    plans = SubscriptionPlan.objects.all()
    context = {'plans': plans}
    return render(request, 'subscription/plans.html', context)

@login_required
def plan_details(request, id):
    """ A view to show the details of a single plan """
    plan = get_object_or_404(SubscriptionPlan, id=id)
    
    # Check if the user has an active subscription to any plan
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        has_active_subscription = user_profile.subscription_plan is not None
    except UserProfile.DoesNotExist:
        has_active_subscription = False
    
    context = {
        'plan': plan,
        'has_active_subscription': has_active_subscription
    }
    return render(request, 'subscription/plan_details.html', context)

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY  # or settings.STRIPE_SECRET_KEY if you're using live keys

def subscribe(request, id):
    plan = get_object_or_404(SubscriptionPlan, id=id)
    # Create a checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': plan.stripe_price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'id': checkout_session.id})

def order_overview(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    # Prepare the data you need
    data = {
        'plan_id': plan.id,
        'name': plan.name,
        'description': plan.description,
        'price': plan.price,
        'image_url': plan.image.url,
        # Add more fields as needed
    }
    return JsonResponse(data)