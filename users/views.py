# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, CustomSignupForm
from allauth.account.views import SignupView as AllauthSignupView
from django.contrib.auth import login

class CustomSignupView(AllauthSignupView):
    form_class = CustomSignupForm

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        print(response.context_data)  # Print context data to debug
        return response
    
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'users/profile_edit.html', {'form': form})