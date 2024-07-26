from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'user_first_name', 'user_last_name', 'subscription_plan', 'subscription_start_date')

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    user_first_name.short_description = 'First Name'
    user_last_name.short_description = 'Last Name'

admin.site.register(UserProfile, UserProfileAdmin)

