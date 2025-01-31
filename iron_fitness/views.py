from django.shortcuts import render

def handler404(request, exception):
    print("Custom 404 handler was triggered!")  # Debug message
    print(f"Exception: {exception}")           # Log the exception
    return render(request, '404.html', status=404)
