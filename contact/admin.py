from django.contrib import admin
from .models import NewsletterSubscriber

class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')

admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)