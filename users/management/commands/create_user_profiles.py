# users/management/commands/create_user_profiles.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile

class Command(BaseCommand):
    # Description of the command to be displayed in the help text
    help = 'Create user profiles for users without one'

    def handle(self, *args, **kwargs):
        # Query the database to find users who do not have a UserProfile
        users_without_profile = User.objects.filter(userprofile__isnull=True)

        # Iterate through each user without a profile
        for user in users_without_profile:
            # Create a UserProfile instance for the user
            UserProfile.objects.create(user=user)

        # Output a success message to the console
        self.stdout.write(self.style.SUCCESS('Successfully created profiles for users without one'))
