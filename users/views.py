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
    }
    return render(request, 'users/managesubscription.html', context)

@login_required
def cancel_subscription(request):
    """ A view to handle subscription cancellation locally """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    subscription_plan = user_profile.subscription_plan

    if subscription_plan:
        # If there is an active subscription plan
        user_profile.subscription_plan = None
        user_profile.stripe_subscription_id = None  # Optionally clear the Stripe subscription ID
        user_profile.save()

        messages.success(request, "Subscription cancelled successfully (local update only).")
    else:
        messages.warning(request, "No active subscription found to cancel.")

    return redirect('manage_subscription')
