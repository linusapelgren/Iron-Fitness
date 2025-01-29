from django import forms  # Import forms module from Django
from .models import ClassTime  # Import ClassTime model
from datetime import (
    datetime,
    time,
    timedelta,
)  # Import datetime, time, timedelta for time manipulation


def generate_time_choices(start_hour=8, end_hour=16, interval_minutes=60):
    times = []
    start_time = time(start_hour, 0)
    end_time = time(end_hour, 0)
    current_time = start_time

    while current_time < end_time:
        end_time_option = (
            datetime.combine(datetime.today(), current_time)
            + timedelta(minutes=interval_minutes)
        ).time()
        times.append(
            (
                f"{current_time.strftime('%H:%M')}-{end_time_option.strftime('%H:%M')}",
                f"{current_time.strftime('%H:%M')}-{end_time_option.strftime('%H:%M')}",
            )
        )
        current_time = end_time_option

    return times


TIME_CHOICES = generate_time_choices()  # Generate time choices for form fields


class BookingForm(forms.Form):
    visitor_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Your name", 
                "readonly": "readonly"  # This makes the field read-only
            }
        ),
    )
    visitor_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", 
                "placeholder": "example.email@email.com", 
                "readonly": "readonly"
            }
        ),
    )
    visitor_phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "placeholder": "070-000 0000", 
                "readonly": "readonly"
            }
        ),
    )
    fitness_class = forms.ChoiceField(
        choices=[], required=True, widget=forms.Select(attrs={"class": "form-select"})
    )  # Fitness class field
    class_day = forms.ChoiceField(
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
            ("Sunday", "Sunday"),
        ],
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )  # Class day field
    class_time = forms.ChoiceField(
        choices=[], required=True, widget=forms.Select(attrs={"class": "form-select"})
    )  # Class time field

    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop("initial", {})
        super().__init__(*args, **kwargs)

        # Set fitness class choices
        self.fields["fitness_class"].choices = [
            (choice[0], choice[1])
            for choice in ClassTime._meta.get_field("fitness_class").choices
        ]
        self.initial.update(initial_data)

        # Get class and day from data or initial
        fitness_class = self.data.get("fitness_class") or initial_data.get(
            "fitness_class"
        )
        class_day = self.data.get("class_day") or initial_data.get("class_day")

        # Update class_time choices based on fitness_class and class_day
        if fitness_class and class_day:
            self.fields["class_time"].choices = self.get_class_times_for_day_and_class(
                fitness_class, class_day
            )
        else:
            self.fields["class_time"].choices = []

    def get_class_times_for_day_and_class(self, fitness_class, day_of_week):
        times = ClassTime.objects.filter(
            fitness_class=fitness_class, day_of_week=day_of_week
        ).order_by("time_range")
        return [
            (ct.time_range, ct.time_range) for ct in times
        ]  # Retrieve class times for specific class and day


class ClassTimeAdminForm(forms.ModelForm):
    time_range = forms.ChoiceField(
        choices=TIME_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )  # Time range field with predefined choices
    day_of_week = forms.ChoiceField(
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
            ("Sunday", "Sunday"),
        ],
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )  # Day of week field

    class Meta:
        model = ClassTime  # Specify the model for the form
        fields = "__all__"  # Use all fields from the model
