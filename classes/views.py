from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def classes(request):
    user = request.user
    context = {
        'user_name': user.get_full_name(),  # Assuming 'get_full_name()' gives you the user's full name
        'user_email': user.email,
        'user_phone': user.profile.phone_number if hasattr(user, 'profile') and hasattr(user.profile, 'phone_number') else ''  # Adjust based on your user profile model
    }
    return render(request, 'classes/classes.html', context)
