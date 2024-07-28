from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Define a signal receiver function that will be called after a User instance is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a UserProfile instance when a User is saved.

    Args:
        sender: The model class that sent the signal (User in this case).
        instance: The actual instance of the model that was saved.
        created: Boolean; True if a new record was created, False if an existing record was updated.
        **kwargs: Additional keyword arguments.
    """
    if created:
        # If a new User instance was created, also create a corresponding UserProfile
        UserProfile.objects.create(user=instance)
    else:
        # If an existing User instance was updated, ensure there is a corresponding UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=instance)
        # If the UserProfile was not created (i.e., it already exists), save it to ensure it is updated
        if not created:
            user_profile.save()
