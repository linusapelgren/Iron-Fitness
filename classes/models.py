from django.db import models

CLASS_CHOICES = [
    ('yoga', 'Yoga'),
    ('pilates', 'Pilates'),
    ('spinning', 'Spinning'),
    ('zumba', 'Zumba'),
    ('crossfit', 'CrossFit'),
    ('boxing', 'Boxing'),
    ('hiit', 'HIIT (High-Intensity Interval Training)'),
]

class ClassTime(models.Model):
    fitness_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    time_range = models.CharField(max_length=11)  # Format "HH:MM-HH:MM"
    day_of_week = models.CharField(
        max_length=9,
        choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                 ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]
    )

    def __str__(self):
        return f"{self.fitness_class} - {self.time_range}"


class Booking(models.Model):
    visitor_name = models.CharField(max_length=100)
    visitor_email = models.EmailField()
    visitor_phone = models.CharField(max_length=15)
    fitness_class = models.CharField(max_length=20)
    class_day = models.CharField(max_length=9)
    class_time = models.CharField(max_length=11)  # Format "HH:MM-HH:MM"

    def __str__(self):
        return f"{self.visitor_name} - {self.fitness_class} - {self.class_day} - {self.class_time}"