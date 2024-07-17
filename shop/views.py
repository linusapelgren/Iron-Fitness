from django.shortcuts import render
from .models import Product  # Adjust import as per your project structure

def supplements(request):
    products = Product.objects.all()  # Ensure Product is assigned here
    return render(request, 'shop/supplements.html', {'products': products})