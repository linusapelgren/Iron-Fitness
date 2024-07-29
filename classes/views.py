from django.shortcuts import render, redirect  
from .forms import BookingForm 
from .models import ClassTime, Booking  
from django.contrib.auth.decorators import login_required  
from users.models import UserProfile
from django.http import JsonResponse  

@login_required
def book_class(request):
    """A view that displays the booking page and handles the booking form"""
    user = request.user  # Get the current logged-in user
    profile = getattr(user, 'userprofile', None) or UserProfile.objects.create(user=user)  # Get or create the user's profile
    initial_data = {
        'visitor_name': user.first_name,
        'visitor_email': user.email,
        'visitor_phone': profile.phone_number if profile else '',
    }  # Initialize form data with user's info
    
    form = BookingForm(request.POST or None, initial=initial_data)  # Create form instance with initial data
    
    times = []  # Initialize empty list for class times
    selected_class = ''  # Initialize selected class as empty string
    selected_day = ''  # Initialize selected day as empty string
    
    import logging

    logger = logging.getLogger(__name__)

@login_required
def book_class(request):
    """A view that displays the booking page and handles the booking form"""
    user = request.user  # Get the current logged-in user
    profile = getattr(user, 'userprofile', None) or UserProfile.objects.create(user=user)  # Get or create the user's profile
    
    # Initialize form and variables
    form = BookingForm(initial={
        'visitor_name': user.first_name,
        'visitor_email': user.email,
        'visitor_phone': profile.phone_number if profile else '',
    })
    times = []
    selected_class = ''
    selected_day = ''

    if request.method == 'POST':
        if 'search_times' in request.POST:
            selected_class = request.POST.get('fitness_class')
            selected_day = request.POST.get('class_day')
            if selected_class and selected_day:
                times = ClassTime.objects.filter(fitness_class=selected_class, day_of_week=selected_day).order_by('time_range')
        
        elif 'book_now' in request.POST:
            form = BookingForm(request.POST)  # Initialize form with POST data
            if form.is_valid():
                booking = Booking(
                    visitor_name=form.cleaned_data['visitor_name'],
                    visitor_email=form.cleaned_data['visitor_email'],
                    visitor_phone=form.cleaned_data['visitor_phone'],
                    fitness_class=form.cleaned_data['fitness_class'],
                    class_day=form.cleaned_data['class_day'],
                    class_time=form.cleaned_data['class_time']
                )  # Create a booking instance from form data
                booking.save()  # Save the booking to the database
                return redirect('successful_booking')  # Redirect to success page
            else:
                logger.error("Form is invalid. Errors: %s", form.errors)
                logger.info("Form data: %s", request.POST)
                # Update times list based on current POST data
                selected_class = request.POST.get('fitness_class', '')
                selected_day = request.POST.get('class_day', '')
                if selected_class and selected_day:
                    times = ClassTime.objects.filter(fitness_class=selected_class, day_of_week=selected_day).order_by('time_range')
    
    return render(request, 'classes/classes.html', {
        'form': form,
        'times': times,
        'selected_class': selected_class,
        'selected_day': selected_day
    })

def success_url(request):
    """A view that displays the success page"""
    return render(request, 'classes/successful_booking.html')  # Render the success page

def load_times(request):
    """A view that loads class times based on selected class and day"""
    fitness_class = request.GET.get('fitness_class')  # Get fitness class from GET parameters
    class_day = request.GET.get('class_day')  # Get class day from GET parameters
    if fitness_class and class_day:
        class_times = ClassTime.objects.filter(fitness_class=fitness_class, day_of_week=class_day).order_by('time_range')
        data = [{'id': ct.id, 'text': str(ct)} for ct in class_times]  # Prepare data for JSON response
        return JsonResponse(data, safe=False)  # Return JSON response with class times
    return JsonResponse([], safe=False)  # Return empty JSON response if no class or day specified
