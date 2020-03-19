from django.shortcuts import render
from workitout.models import Workout 
from django.forms.models import model_to_dict


def home(request):

    
    workout_list=Workout.objects.order_by('-difficulty')[:3]
    
    
    
    for w in workout_list:
        w.numLikes = len(w.likes.all())
        

        
    

    context_dict={}
    context_dict['workouts'] = workout_list
    
    



    return render(request, 'workitout/home.html', context_dict)

def create_workout(request):

    return render(request, 'workitout/create-workout.html')

def search(request):

    return render(request, 'workitout/search.html')
    
def user_page(request):

    return render(request, 'workitout/user-page.html')