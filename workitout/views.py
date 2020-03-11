from django.shortcuts import render


def home(request):

    return render(request, 'workitout/home.html')

def create_workout(request):

    return render(request, 'workitout/create-workout.html')

def search(request):

    return render(request, 'workitout/search.html')
    
def user_page(request):

    return render(request, 'workitout/user-page.html')