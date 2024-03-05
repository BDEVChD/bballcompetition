from django.shortcuts import render

# Create your views here.
def home(request):
    # Logic for your view goes here
    # context = {
    #     'message': 'Hello, World!'
    # }
    return render(request, 'bballcompapp/home.html')
