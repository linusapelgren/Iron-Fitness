from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from contact.models import NewsletterSubscriber


class Command(BaseCommand):
    help = 'Send bulk emails to all newsletter subscribers'

    def add_arguments(self, parser):
        parser.add_argument('subject', type=str, help='Subject of the email')
        parser.add_argument('message', type=str, help='Body of the email')

    def handle(self, *args, **kwargs):
        subject = kwargs['subject']
        message = kwargs['message']
        from_email = settings.EMAIL_HOST_USER
        subscribers = NewsletterSubscriber.objects.all()

        if not subscribers:
            self.stdout.write(self.style.WARNING('No subscribers found.'))
            return

        recipient_list = [subscriber.email for subscriber in subscribers]

        try:
            send_mail(subject, message, from_email, recipient_list)
            self.stdout.write(self.style.SUCCESS(
                f'Email sent to {len(recipient_list)} subscribers.'
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending emails: {e}'))
