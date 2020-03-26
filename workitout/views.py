from django.shortcuts import render, redirect
from workitout.models import Workout , Exercise, UserProfile
from django.forms.models import model_to_dict

from workitout.forms import CreateWorkoutForm


def home(request):
    workout_list=Workout.objects.order_by('-difficulty')[:3]
    
    for w in workout_list:
        w.numLikes = len(w.likes.all())

    context_dict={}
    context_dict['workouts'] = workout_list
    
    return render(request, 'workitout/home.html', context_dict)






def create_workout(request):

    context = {}

    # if user isnt authenticated then prompt them to login/register
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    # gona be a post request or nothing
    form = CreateWorkoutForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)

        # foreign key needs to be set before committing the save ^
        # get the userprofile ID that matches the email of the user
        creator = UserProfile.objects.filter(email=user.email).first()
        obj.creator = creator
        obj.save()
        form = CreateWorkoutForm()

    context['form'] = form

    return render(request, 'workitout/create-workout.html', context)

def must_authenticate(request):

    return render(request, 'workitout/must_authenticate.html', {})











def search(request):

    return render(request, 'workitout/search.html')

def about(request):

    return render(request, 'workitout/about.html')
    
def user_page(request):

    return render(request, 'workitout/user-page.html')

def exercises(request):

    exercise_list = Exercise.objects.order_by('title')
    context_dict={}
    context_dict['exercises'] = exercise_list
    return render(request, 'workitout/exercises.html', context_dict)

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
