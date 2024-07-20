from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'user': request.user,
        # Add any other context variables here
    }
    return render(request, 'home/index.html', context)