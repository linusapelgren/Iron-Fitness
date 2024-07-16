from django.db import models
from django.contrib import admin


# Create your models here.
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='plans/')
    duration = models.CharField(max_length=100)  # e.g., 'Monthly', 'Yearly'
    benefit = models.CharField(max_length=255)   # e.g., 'Regular', 'Senior', '10-times card', '1-time card'

    def __str__(self):
        return self.name
    
admin.site.register(SubscriptionPlan)