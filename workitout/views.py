from django.shortcuts import render

# Create your views here.

def home(request):

    return render(request, 'rango/home.html')

def create-workout(request):

    return render(request, 'rango/create-workout.html')

def search(request):

    return render(request, 'rango/search.html')
    
def user-page(request):

    return render(request, 'rango/user-page.html')