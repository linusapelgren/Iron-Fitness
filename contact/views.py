from django.shortcuts import render


def contact(request):
    """A view that displays the contact page"""
    return render(request, "contact/contact.html")
