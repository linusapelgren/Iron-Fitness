from django.db import models
from django.contrib.auth.models import User
from subscription.models import SubscriptionPlan

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    gym_visits = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/blank_profile.png')
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, null=True, blank=True, on_delete=models.SET_NULL)
    subscription_start_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
