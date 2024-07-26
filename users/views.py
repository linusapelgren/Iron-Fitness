from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from allauth.account.views import SignupView as AllauthSignupView
from .forms import UserProfileForm, CustomSignupForm
from .models import UserProfile
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from subscription.models import SubscriptionPlan
import stripe
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class CustomSignupView(AllauthSignupView):
    form_class = CustomSignupForm

@login_required
def profile_view(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    context = {'user_profile': user_profile, 'user': request.user}
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
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
    """ A view to manage subscription """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    subscription_plan = user_profile.subscription_plan

    context = {
        'subscription_plan': subscription_plan,
        'user_profile': user_profile,
    }

    return render(request, 'users/managesubscription.html', context)


@login_required
def cancel_subscription(request):
    """ A view to handle subscription cancellation with binding period check """
    # Fetch the user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)
    subscription_plan = user_profile.subscription_plan

    # Initialize a flag to indicate whether the cancel button should be visible
    can_cancel = True

    if subscription_plan:
        # Retrieve binding period and subscription start date
        binding_period_days = subscription_plan.binding_time  # Ensure this field exists
        binding_period_days = int(binding_period_days) 
        subscription_start_date = user_profile.subscription_start_date

        if subscription_start_date:
            # Calculate the end date of the binding period
            binding_end_date = subscription_start_date + timedelta(days=binding_period_days)
            current_date = timezone.now()

            # Check if the current date is within the binding period
            if current_date < binding_end_date:
                can_cancel = False
                messages.warning(request, "You cannot cancel your subscription during the binding period.")
            else:
                # Proceed to cancel the subscription
                if request.method == 'POST':
                    user_profile.subscription_plan = None
                    user_profile.subscription_start_date = None
                    user_profile.save()
                    messages.success(request, "Subscription cancelled successfully.")
                    return redirect('manage_subscription')
        else:
            messages.warning(request, "Subscription start date not found.")
    else:
        messages.warning(request, "No active subscription found to cancel.")

    # Pass the can_cancel flag to the template
    return render(request, 'your_template.html', {'can_cancel': can_cancel})