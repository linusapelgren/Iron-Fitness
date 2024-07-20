from django.shortcuts import render, get_object_or_404
from .models import SubscriptionPlan

def plans(request):
    """ A view to show the plans page """
    plans = SubscriptionPlan.objects.all()
    context = {'plans': plans}
    return render(request, 'subscription/plans.html', context)

def plan_details(request, id):
    """ A view to show the details of a single plan """
    plan = get_object_or_404(SubscriptionPlan, id=id)
    return render(request, 'subscription/plan_details.html', {'plan': plan})
