from django.shortcuts import render
from django.contrib.auth.models import User
from workitout.models import Workout , Exercise, UserProfile
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

def about(request):

    return render(request, 'workitout/about.html')
    

def exercises(request):

    exercise_list = Exercise.objects.order_by('title')
    context_dict={}
    context_dict['exercises'] = exercise_list
    return render(request, 'workitout/exercises.html', context_dict)

def user_page(request, user_name):
    context_dict = {}
    try:
        workout_list = []

        user_obj = User.objects.get(username=user_name)
        user1 = UserProfile.objects.get(user=user_obj)


        for w in user1.saved.all():
            workout_list.append(w)
        context_dict['user'] = user1
        context_dict['username'] = user_obj.username
        context_dict['picture'] = user1.picture
        context_dict['bio'] = user1.bio
        context_dict['following'] = len(user1.following.all())
        context_dict['followers'] = len(user1.followers.all())
        context_dict['verified'] = user1.isVerified
        context_dict['private'] = user1.isPrivate
        context_dict['s_workouts'] = workout_list
    except User.DoesNotExist:
        context_dict['user'] = None

    return render(request, 'workitout/user-page.html',context=context_dict)

def show_exercise(request, exercise_title_slug):
    context_dict = {}
    try:

        exercise = Exercise.objects.get(slug=exercise_title_slug)

        # parse exercise object and add individual fields to context dict
        context_dict['title'] = exercise.title
        
        diff_dict = {1:'Easy', 2:'Medium', 3:'Hard'} #can change these
        context_dict['difficulty'] = diff_dict[exercise.difficulty]

        context_dict['primer'] = exercise.description.primer
        context_dict['steps'] = exercise.description.steps.split('$$')
        context_dict['tips'] = exercise.description.tips.split('$$')
        if context_dict['tips'] == ['']:
            context_dict['tips'] = None

        context_dict['muscle_group'] = exercise.muscle_group
        context_dict['muscles'] = [m.name for m in exercise.muscles.all()]
        context_dict['tags'] = [t.name for t in exercise.tags.all()]
        context_dict['equipment'] = [e.name for e in exercise.equipment.all()]
        context_dict['image_paths'] = ["images\\exercises\\" + exercise_title_slug + "-1.png", "images\\exercises\\" + exercise_title_slug + "-2.png"]

       

    except Exercise.DoesNotExist:
        context_dict['exercise'] = None

    return render(request, 'workitout/exercise.html', context=context_dict)
