from django.shortcuts import render, redirect
from .forms import NewsletterSignupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def contact_us(request):
    """ A view to return the contact us page """
    return render(request, 'contact/contact.html')

@login_required  # Ensures the user is logged in
def newsletter_signup(request):
    user = request.user  # Get the logged-in user
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            form.save(user)  # Save the subscription preference for the user
            # Show a success message and redirect
            messages.success(request, "You have successfully updated your newsletter preferences.")
            return redirect('newsletter_success')  # Redirect to a success page or confirmation page
    else:
        form = NewsletterSignupForm()

    return render(request, 'newsletter_signup.html', {'form': form})