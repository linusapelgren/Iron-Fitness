from django.shortcuts import render, redirect
from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber
from django.contrib import messages

def contact_us(request):
    """ A view to return the contact us page and handle newsletter signup """
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email is already in the database
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.error(request, "This email is already subscribed.")
            else:
                # Save the email to the database
                subscriber = NewsletterSubscriber(email=email)
                subscriber.save()

                # Add a success message
                messages.success(request, "Successfully signed up for the newsletter!")

            # Reset the form after submission
            form = NewsletterSignupForm()  # Clear the form if no errors
        else:
            messages.error(request, "There was an error with your submission.")
            print(form.errors)  # Debugging: print form errors to the console
    else:
        form = NewsletterSignupForm()

    return render(request, 'contact/contact.html', {'form': form})
