from django.shortcuts import render

# Create your views here.
def plans(request):
    """ A view to show the plans page """
    return render(request, 'subscription/plans.html')