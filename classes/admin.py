from django.contrib import admin
from .models import ClassTime, Booking
from .forms import ClassTimeAdminForm

class ClassTimeAdmin(admin.ModelAdmin):
    form = ClassTimeAdminForm
    list_display = ('fitness_class', 'day_of_week', 'time_range')
    list_filter = ('fitness_class', 'day_of_week')

admin.site.register(ClassTime, ClassTimeAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('visitor_name', 'visitor_email', 'visitor_phone', 'fitness_class', 'class_day', 'class_time')
    list_filter = ('fitness_class', 'class_day')

admin.site.register(Booking, BookingAdmin)