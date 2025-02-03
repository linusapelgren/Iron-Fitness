from django.shortcuts import render, redirect
from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required


def contact_us(request):
    """ A view to return the contact us page and handle newsletter signup """
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email is already in the database
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.error(
                    request, "Already subscribed.", extra_tags='newsletter'
                )
            else:
                # Save the email to the database
                subscriber = NewsletterSubscriber(email=email)
                subscriber.save()

                # Send an email to the registered email
                subject = "Thank You for Signing Up!"
                message = (
                    f"Hi there,\n\n"
                    f"Thank you for signing up for our newsletter.\n\n"
                    f"We're excited to keep you updated\n\n"
                    f"on the latest news and updates.\n\n"
                    f"Best regards,\nThe Iron Fitness Team"
                )
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]

                try:
                    send_mail(subject, message, from_email, recipient_list)
                    messages.success(
                        request, "Signed up!", extra_tags="newsletter"
                    )
                except Exception as e:
                    print(f"Email error: {e}")

            form = NewsletterSignupForm()  # Clear the form if no errors
        else:
            messages.error(request, "Error.", extra_tags="newsletter")
    else:
        form = NewsletterSignupForm()

    return render(request, 'contact/contact.html', {'form': form})


@staff_member_required
def send_newsletter(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        # Get all subscriber emails
        subscribers = NewsletterSubscriber.objects.all()
        recipient_list = [subscriber.email for subscriber in subscribers]
        # Send the email
        if recipient_list:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            messages.success(request, "Newsletter sent successfully!")
            return render(request, 'send_newsletter.html')
        else:
            messages.error(request, "No subscribers found.")

    return render(request, 'contact/newsletter.html')
