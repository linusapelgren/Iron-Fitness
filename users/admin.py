from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    # Define which fields should be displayed in the admin interface
    list_display = (
        "user",
        "phone_number",
        "user_first_name",
        "user_last_name",
        "subscription_plan",
        "subscription_start_date",
    )

    # Method to display the user's first name in the list view
    def user_first_name(self, obj):
        return obj.user.first_name

    # Method to display the user's last name in the list view
    def user_last_name(self, obj):
        return obj.user.last_name

    # Define the column headers for the custom fields
    user_first_name.short_description = "First Name"
    user_last_name.short_description = "Last Name"


# Register the UserProfile model with the custom admin configuration
admin.site.register(UserProfile, UserProfileAdmin)
