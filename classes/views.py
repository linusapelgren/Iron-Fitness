from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import ClassTime, Booking
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


@login_required
def book_class(request):
    """A view that displays the booking page and handles the booking form"""
    user = request.user  # Get the current logged-in user
    profile = getattr(user, "userprofile", None) or UserProfile.objects.create(
        user=user
    )  # Get or create the user's profile

    # Initialize form and variables
    form = BookingForm(
        initial={
            "visitor_name": user.first_name,
            "visitor_email": user.email,
            "visitor_phone": profile.phone_number if profile else "",
        }
    )

    times = []
    selected_class = ""
    selected_day = ""

    if request.method == "POST":
        if "search_times" in request.POST:
            selected_class = request.POST.get("fitness_class", "")
            selected_day = request.POST.get("class_day", "")
            if selected_class and selected_day:
                times = ClassTime.objects.filter(
                    fitness_class=selected_class, day_of_week=selected_day
                ).order_by("time_range")

        elif "book_now" in request.POST:
            # Extract data directly from request.POST
            visitor_name = request.POST.get("visitor_name", "")
            visitor_email = request.POST.get("visitor_email", "")
            visitor_phone = request.POST.get("visitor_phone", "")
            fitness_class = request.POST.get("fitness_class", "")
            class_day = request.POST.get("class_day", "")
            class_time = request.POST.get("class_time", "")

            # Check if all required fields are filled
            if (
                visitor_name
                and visitor_email
                and visitor_phone
                and fitness_class
                and class_day
                and class_time
            ):
                booking = Booking(
                    visitor_name=visitor_name,
                    visitor_email=visitor_email,
                    visitor_phone=visitor_phone,
                    fitness_class=fitness_class,
                    class_day=class_day,
                    class_time=class_time,
                )  # Create a booking instance from POST data
                booking.save()  # Save the booking to the database
                return redirect("successful_booking")  # Redirect to success page
            else:
                # Log missing data if any required field is missing
                logger.error(
                    "Booking form submission missing required data. Data received: %s",
                    request.POST,
                )

    return render(
        request,
        "classes/classes.html",
        {
            "form": form,
            "times": times,
            "selected_class": selected_class,
            "selected_day": selected_day,
        },
    )


def success_url(request):
    """A view that displays the success page"""
    return render(request, "classes/successful_booking.html")  # Render the success page


def success_url(request):
    """A view that displays the success page"""
    return render(request, "classes/successful_booking.html")  # Render the success page


def load_times(request):
    """A view that loads class times based on selected class and day"""
    fitness_class = request.GET.get(
        "fitness_class"
    )  # Get fitness class from GET parameters
    class_day = request.GET.get("class_day")  # Get class day from GET parameters
    if fitness_class and class_day:
        class_times = ClassTime.objects.filter(
            fitness_class=fitness_class, day_of_week=class_day
        ).order_by("time_range")
        data = [
            {"id": ct.id, "text": str(ct)} for ct in class_times
        ]  # Prepare data for JSON response
        return JsonResponse(data, safe=False)  # Return JSON response with class times
    return JsonResponse(
        [], safe=False
    )  # Return empty JSON response if no class or day specified
