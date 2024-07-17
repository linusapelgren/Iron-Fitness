from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='supplements/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"
