from django.shortcuts import render

def welcome_view(request):
    return render(request, 'home/welcome.html')

# Create your views here.
