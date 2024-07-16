from django.shortcuts import render
from .models import SubscriptionPlan
# Create your views here.
def plans(request):
    """ A view to show the plans page """
    plans = SubscriptionPlan.objects.all()

    context = {'plans': plans}
    return render(request, 'subscription/plans.html', context)