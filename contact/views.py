from django.shortcuts import render, redirect
from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def contact_us(request):
    """ A view to return the contact us page and handle newsletter signup """
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email is already in the database
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.error(request, "This email is already subscribed.", extra_tags='newsletter')
            else:
                # Save the email to the database
                subscriber = NewsletterSubscriber(email=email)
                subscriber.save()

                # Send an email to the registered email
                subject = "Thank You for Signing Up!"
                message = (
                    f"Hi there,\n\n"
                    f"Thank you for signing up for our newsletter. We're excited to keep you updated "
                    f"on the latest news and updates.\n\n"
                    f"Best regards,\nThe Iron Fitness Team"
                )
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]

                try:
                    send_mail(subject, message, from_email, recipient_list)
                    messages.success(request, "Successfully signed up for the newsletter! A confirmation email has been sent.", extra_tags='newsletter')
                except Exception as e:
                    messages.error(request, "Sign up successful, but we couldn't send the confirmation email.", extra_tags='newsletter')
                    print(f"Email error: {e}")

            form = NewsletterSignupForm()  # Clear the form if no errors
        else:
            messages.error(request, "There was an error with your submission.", extra_tags='newsletter')
            print(form.errors)  # Debugging: print form errors to the console
    else:
        form = NewsletterSignupForm()

    return render(request, 'contact/contact.html', {'form': form})