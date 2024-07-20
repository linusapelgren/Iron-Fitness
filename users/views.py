from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, CustomSignupForm
from allauth.account.views import SignupView as AllauthSignupView
from django.contrib.auth import login, update_session_auth_hash
from .models import UserProfile

class CustomSignupView(AllauthSignupView):
    form_class = CustomSignupForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.user
        phone_number = form.cleaned_data.get('phone_number')
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.phone_number = phone_number
        user_profile.save()
        return response

@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    context = {'user_profile': user_profile, 'user': request.user}
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Debugging output
            print("Form is valid")
            # Check if file is uploaded
            if 'picture' in request.FILES:
                print("File uploaded:", request.FILES['picture'])
            else:
                print("No file uploaded")
            form.save()
            return redirect('profile_view')
        else:
            # Debugging output
            print("Form errors:", form.errors)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile_edit.html', {'form': form, 'user_profile': user_profile})
