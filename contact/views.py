from django.shortcuts import render, redirect
from .forms import NewsletterSignupForm
from .models import NewsletterSubscription
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def contact_us(request):
    """ A view to return the contact us page """
    return render(request, 'contact/contact.html')

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if the email is already subscribed
            if not NewsletterSubscription.objects.filter(email=email).exists():
                # Save the email to the database
                NewsletterSubscription.objects.create(email=email)
                messages.success(request, 'Successfully subscribed to the newsletter!')
            else:
                messages.info(request, 'You are already subscribed to the newsletter.')

            # Redirect to the same page to avoid resubmission on refresh
            return redirect('newsletter_signup')  # Adjust to your actual URL name if necessary
    else:
        form = NewsletterSignupForm()

    return render(request, 'contact/contact.html', {'form': form})