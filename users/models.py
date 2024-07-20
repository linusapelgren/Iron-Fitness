from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, default='')
    gym_visits = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/blank_profile.png')
    address = models.CharField(max_length=255, blank=True, null=True)  # Correct field name

    def __str__(self):
        return self.user.username

