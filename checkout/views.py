import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import (
    csrf_exempt,
)
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.contrib.auth.decorators import (
    login_required,
)
from subscription.models import SubscriptionPlan
from users.models import UserProfile
import json
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
import logging

# Set the Stripe API key using the one defined in settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


# Define a view to process payments
@login_required
def process_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Load the request body as JSON
        token = data.get("token")  # Get the payment token from the data
        plan_id = data.get("plan_id")  # Get the plan ID from the data

        try:
            plan = get_object_or_404(
                SubscriptionPlan, pk=plan_id
            )  # Get the subscription plan or return 404
            # Convert plan price to cents
            amount_in_cents = int(plan.price * 100)
            # Create a charge using the Stripe API
            charge = stripe.Charge.create(
                amount=amount_in_cents,
                currency="usd",
                description=f"Charge for plan {plan_id}",
                source=token,
            )

            # Update the user profile with the new subscription plan
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            user_profile.subscription_plan = plan
            user_profile.subscription_start_date = timezone.now()
            user_profile.save()

            return JsonResponse({"success": True})  # Return a success response

        except stripe.error.StripeError as e:
            return JsonResponse(
                {"error": str(e)}, status=500
            )  # Return an error response in case of a Stripe error

    return JsonResponse(
        {"error": "Invalid request"}, status=400
    )  # Return an error response for invalid requests


# Define a view for the checkout process
@login_required
def checkout(request, plan_id):
    plan = get_object_or_404(
        SubscriptionPlan, pk=plan_id
    )  # Get the subscription plan or return 404
    user_profile = (
        UserProfile.objects.get(user=request.user)
        if request.user.is_authenticated
        else None
    )  # Get the user profile if authenticated

    context = {
        "STRIPE_TEST_PUBLIC_KEY": settings.STRIPE_TEST_PUBLIC_KEY,
        "plan_id": plan_id,
        "plan": plan,
        "user_profile": user_profile,
    }

    return render(
        request, "checkout/checkout.html", context
    )  # Render the checkout template with context


# Define a view to provide an overview of an order
def order_overview(request, plan_id):
    try:
        plan = SubscriptionPlan.objects.get(
            pk=plan_id
        )  # Get the subscription plan or raise an exception
        data = {
            "name": plan.name,
            "description": plan.description,
            "price": plan.price,
            "image_url": plan.image.url,
            "duration": plan.duration,
            "benefit": plan.benefit,
        }
        return JsonResponse(data)  # Return the plan details as a JSON response
    except SubscriptionPlan.DoesNotExist:
        return JsonResponse(
            {"error": "Plan not found"}, status=404
        )  # Return an error response if the plan does not exist


# Define a view for the success page
def success(request):
    return render(request, "checkout/success.html")


logger = logging.getLogger(__name__)  # Get a logger instance


# Define a view to handle Stripe webhooks
def stripe_webhook(request):
    payload = request.body  # Get the request body
    sig_header = request.META.get(
        "HTTP_STRIPE_SIGNATURE", ""
    )  # Get the Stripe signature header
    endpoint_secret = (
        settings.STRIPE_WEBHOOK_SECRET
    )  # Get the webhook secret from settings

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )  # Construct the event from the payload and signature
        logger.info(f"Received event: {event['type']}")
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.error(f"Webhook error: {e}")
        return HttpResponse(status=400)  # Return a 400 error response

    if (
        event["type"] == "checkout.session.completed"
    ):  # Check if the event is for a completed checkout session
        session = event["data"]["object"]
        handle_checkout_session(session)  # Handle the checkout session

    return HttpResponse(status=200)  # Return a 200 OK response


# Define a function to handle a completed checkout session
def handle_checkout_session(session):
    plan_id = session.get("metadata", {}).get(
        "plan_id"
    )  # Get the plan ID from the session metadata
    email = session.get("metadata", {}).get(
        "email"
    )  # Get the email from the session metadata

    if not plan_id or not email:
        logger.error(
            "Missing plan_id or email in session metadata."
        )  # Log an error if metadata is missing
        return

    try:
        user = User.objects.get(email=email)  # Get the user by email
        plan = SubscriptionPlan.objects.get(
            id=plan_id
        )  # Get the subscription plan by ID

        # Update or create the user profile with the new subscription plan
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.subscription_plan = plan
        user_profile.save()

    except User.DoesNotExist:
        logger.error(
            f"User with email {email} does not exist."
        )  # Log an error if the user does not exist
    except SubscriptionPlan.DoesNotExist:
        logger.error(
            f"Subscription plan with ID {plan_id} does not exist."
        )  # Log an error if the plan does not exist
