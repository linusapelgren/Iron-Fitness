from django.db import models
from django.contrib.auth.models import User

# Choices for fitness class
CLASS_CHOICES = [
    ("yoga", "Yoga"),
    ("pilates", "Pilates"),
    ("spinning", "Spinning"),
    ("zumba", "Zumba"),
    ("crossfit", "CrossFit"),
    ("boxing", "Boxing"),
    ("hiit", "HIIT (High-Intensity Interval Training)"),
]


# Model for class time
class ClassTime(models.Model):
    fitness_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    time_range = models.CharField(max_length=20)  # Format "HH:MM-HH:MM"
    day_of_week = models.CharField(
        max_length=9,
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
            ("Sunday", "Sunday"),
        ],
    )

    def __str__(self):
        return f"{self.get_fitness_class_display()} - {self.time_range}"


class Booking(models.Model):
    """Model for booking a class."""
    visitor_name = models.CharField(max_length=100)
    visitor_email = models.EmailField()
    visitor_phone = models.CharField(max_length=50)
    fitness_class = models.CharField(max_length=50)
    class_day = models.CharField(max_length=9)  # For example, 'Monday'
    class_time = models.CharField(max_length=50)  # Format "HH:MM-HH:MM"
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="booked_classes"
    )

    def __str__(self):
        return (
            f"{self.visitor_name} - {self.fitness_class} - "
            f"{self.class_day} - {self.class_time}"
        )
