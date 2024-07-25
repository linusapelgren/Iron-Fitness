from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.views import SignupView as AllauthSignupView
from .forms import UserProfileForm, CustomSignupForm
from .models import UserProfile
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages


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