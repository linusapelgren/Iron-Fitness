from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from allauth.account.views import SignupView as AllauthSignupView
from .forms import UserProfileForm, CustomSignupForm
from .models import UserProfile
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
import stripe
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

@login_required
def profile_view(request):
    """A view to display the user's profile."""
    user_profile = UserProfile.objects.filter(user=request.user).first()
    context = {'user_profile': user_profile, 'user': request.user}
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
    """A view to edit the user's profile."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile_edit.html', {'form': form, 'user_profile': user_profile})

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile_view')  # Update this to your profile view URL
    
    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)
    
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY  # Use your secret key

@login_required
def manage_subscription(request):
    """A view to manage the user's subscription."""
    user_profile = UserProfile.objects.get(user=request.user)
    subscription_plan = user_profile.subscription_plan
    
    # Determine if the subscription can be canceled
    if subscription_plan and subscription_plan.binding_time == 'None':
        can_cancel = True
    else:
        can_cancel = False

    if request.method == 'POST':
        # Handle cancellation logic here
        if can_cancel:
            # Remove subscription
            user_profile.subscription_plan = None
            user_profile.subscription_start_date = None
            user_profile.save()
            return redirect('subscription_success')  # Redirect to a success page or message

    context = {
        'subscription_plan': subscription_plan,
        'user_profile': user_profile,
        'can_cancel': can_cancel,
    }
    return render(request, 'users/managesubscription.html', context)

import re

@login_required
def cancel_subscription(request):
    """A view to handle subscription cancellation with binding period check."""
    print("Reached cancel_subscription view")  # Debug line

    # Fetch the user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)
    subscription_plan = user_profile.subscription_plan

    # Initialize the flag
    can_cancel = True

    if subscription_plan:
        binding_time_str = subscription_plan.binding_time

        # Convert binding_time_str to days
        binding_period_days = convert_binding_time_to_days(binding_time_str)
        if binding_period_days is None:
            messages.error(request, "Invalid binding period format.")
            print(f"Invalid binding_time format: {binding_time_str}")  # Debug line
            return render(request, 'users/managesubscription.html', {'can_cancel': can_cancel, 'subscription_plan': subscription_plan, 'user_profile': user_profile})

        subscription_start_date = user_profile.subscription_start_date

        if subscription_start_date:
            binding_end_date = subscription_start_date + timedelta(days=binding_period_days)
            current_date = timezone.now()

            if current_date < binding_end_date:
                can_cancel = False
                messages.warning(request, "You cannot cancel your subscription during the binding period.")
            elif request.method == 'POST':
                print("POST request received")  # Debug line
                try:
                    user_profile.subscription_plan = None
                    user_profile.subscription_start_date = None
                    user_profile.save()
                    messages.success(request, "Subscription cancelled successfully.")
                    return redirect('manage_subscription')
                except Exception as e:
                    messages.error(request, "An error occurred while canceling your subscription.")
                    print(f"Error canceling subscription: {e}")
        else:
            messages.warning(request, "Subscription start date is not set.")
    else:
        messages.warning(request, "No active subscription found to cancel.")

    # Pass the can_cancel flag to the template
    return render(request, 'users/managesubscription.html', {'can_cancel': can_cancel, 'subscription_plan': subscription_plan, 'user_profile': user_profile})


def convert_binding_time_to_days(binding_time_str):
    """Converts a binding time string to the number of days."""
    if not binding_time_str or binding_time_str.lower() == "none":
        return 0

    binding_time_str = binding_time_str.strip().lower()

    # Match patterns like '12 months', '1 year', etc.
    match = re.match(r"(\d+)\s*(month|year)", binding_time_str)
    if match:
        number = int(match.group(1))
        unit = match.group(2)
        if unit == "year":
            return number * 365
        elif unit == "month":
            return number * 30
        else:
            return None
    else:
        return None