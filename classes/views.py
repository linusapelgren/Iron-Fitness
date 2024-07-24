from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import ClassTime, Booking
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from django.http import JsonResponse

@login_required
def book_class(request):
    user = request.user
    profile = getattr(user, 'userprofile', None) or UserProfile.objects.create(user=user)
    initial_data = {
        'visitor_name': user.first_name,
        'visitor_email': user.email,
        'visitor_phone': profile.phone_number if profile else '',
    }
    
    form = BookingForm(request.POST or None, initial=initial_data)
    
    times = []
    selected_class = ''
    selected_day = ''
    
    if request.method == 'POST':
        if 'search_times' in request.POST:
            selected_class = request.POST.get('fitness_class')
            selected_day = request.POST.get('class_day')
            print(f"Selected class: {selected_class}, Selected day: {selected_day}")
            if selected_class and selected_day:
                times = ClassTime.objects.filter(fitness_class=selected_class, day_of_week=selected_day).order_by('time_range')
                print(f"Times found: {times}")
        
        elif 'book_now' in request.POST:
            if form.is_valid():
                booking = Booking(
                    visitor_name=form.cleaned_data['visitor_name'],
                    visitor_email=form.cleaned_data['visitor_email'],
                    visitor_phone=form.cleaned_data['visitor_phone'],
                    fitness_class=form.cleaned_data['fitness_class'],
                    class_day=form.cleaned_data['class_day'],
                    class_time=form.cleaned_data['class_time']
                )
                booking.save()
                return redirect('successful_booking')
            else:
                selected_class = request.POST.get('fitness_class')
                selected_day = request.POST.get('class_day')
                if selected_class and selected_day:
                    times = ClassTime.objects.filter(fitness_class=selected_class, day_of_week=selected_day).order_by('time_range')
                    print(f"Times found: {times}")

    return render(request, 'classes/classes.html', {
        'form': form,
        'times': times,
        'selected_class': selected_class,
        'selected_day': selected_day
    })

def success_url(request):
    return render(request, 'classes/success.html')

def load_times(request):
    fitness_class = request.GET.get('fitness_class')
    class_day = request.GET.get('class_day')
    if fitness_class and class_day:
        class_times = ClassTime.objects.filter(fitness_class=fitness_class, day_of_week=class_day).order_by('time_range')
        data = [{'id': ct.id, 'text': str(ct)} for ct in class_times]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)