from django.shortcuts import render, redirect
from .forms import NewsletterSignupForm
from django.contrib import messages

def contact(request):
    """A view that displays the contact page"""
    return render(request, "contact/contact.html")

def contact_us(request):
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Here you would typically save the email to a database or send it somewhere
            messages.success(request, 'Thank you for signing up for our newsletter!')
            return redirect('contact_us')  # Redirect to avoid form resubmission on refresh
    else:
        form = NewsletterSignupForm()
    
    return render(request, 'contact.html', {'form': form})