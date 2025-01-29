from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import ClassTime, Booking
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)
@login_required
def book_class(request):
    print("----Book class----\n")
    user = request.user

    # Retrieve the existing UserProfile for the logged-in user
    try:
        profile = UserProfile.objects.get(user=user)
        logger.debug(f"Existing profile found for {user.username}.")
    except UserProfile.DoesNotExist:
        logger.error(f"No profile found for {user.username}, but they are logged in.")
        return redirect('profile_creation')  # Redirect to a profile creation page (if necessary)

    # Get the phone number from the profile
    phone_number = profile.phone_number if profile else ''

    # Initialize the form with the user's profile information
    form = BookingForm(initial={
        'visitor_name': f'{user.first_name} {user.last_name}',
        'visitor_email': user.email,
        'visitor_phone': phone_number,  # Ensure the phone number is correctly passed
    })

    selected_class = None
    selected_day = None
    times = []

    if request.method == 'POST':

        print("----Testing----\n")
        print(request.POST)
        if 'search_times' in request.POST:
            print("----First if----\n")
            selected_class = request.POST.get('fitness_class')
            selected_day = request.POST.get('class_day')

            # Get available times based on the selected class and day
            times = ClassTime.objects.filter(fitness_class=selected_class, day_of_week=selected_day)
            request.session['visitor_name'] = request.POST.get('visitor_name')
            request.session['visitor_email'] = request.POST.get('visitor_email')
            request.session['visitor_phone'] = request.POST.get('visitor_phone')

        elif 'book_now' in request.POST:
            print("----Second if----\n")
            visitor_name = request.session['visitor_name']
            visitor_email = request.session['visitor_email']
            visitor_phone = request.session['visitor_phone']
            class_time_id = request.POST.get('class_time')
            
            # Ensure we get the actual ClassTime object by filtering using time_range or other identifier
            try:
                class_time = ClassTime.objects.get(id=class_time_id)
                logger.debug(f"ClassTime selected: {class_time}")
            except ClassTime.DoesNotExist:
                logger.error(f"ClassTime with id {class_time_id} not found.")
                return render(request, 'classes/classes.html', {
                    'form': form,
                    'times': times,
                    'selected_class': selected_class,
                    'selected_day': selected_day,
                    'error': 'Selected class time is invalid.',
                })

            # Create and save the booking
            booking = Booking(
                visitor_name=visitor_name,
                visitor_email=visitor_email,
                visitor_phone=visitor_phone,
                class_time=class_time,
                user=user  # Ensure the user is associated with the booking
            )
            booking.save()

            # Add the booking to the user's profile
            profile.booked_classes.add(booking)
            profile.save()

            # Redirect to success page
            return redirect('successful_booking')

    # If not POST, render the page with the form
    return render(request, 'classes/classes.html', {
        'form': form,
        'times': times,
        'selected_class': selected_class,
        'selected_day': selected_day,
    })


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
