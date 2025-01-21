from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from contact.models import NewsletterSubscriber

@admin.action(description='Send email to selected subscribers')
def send_bulk_email(modeladmin, request, queryset):
    subject = "Your Custom Subject"
    message = "Your Custom Message Body"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [subscriber.email for subscriber in queryset]

    try:
        send_mail(subject, message, from_email, recipient_list)
        modeladmin.message_user(request, f'Email sent to {len(recipient_list)} subscribers.')
    except Exception as e:
        modeladmin.message_user(request, f'Error sending emails: {e}', level='error')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    actions = [send_bulk_email]