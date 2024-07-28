from django.shortcuts import render

# Create your views here.

def index(request):
    """A view that displays the index page"""
    context = {
        'user': request.user,
    }
    return render(request, 'home/index.html', context)