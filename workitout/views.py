from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from workitout.models import Workout , Exercise, UserProfile, ExInWorkout
from django.forms.models import model_to_dict
from workitout.forms import UserProfileForm
from django.contrib.auth.decorators import login_required

from workitout.forms import CreateWorkoutForm


def home(request):
    workout_list=Workout.objects.order_by('-difficulty')
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
        return redirect(reverse('workitout:must_authenticate'))

    # gona be a post request or nothing
    form = CreateWorkoutForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)

        # foreign key needs to be set before committing the save ^
        # get the userprofile ID that matches the email of the user
    
        obj.creator = user
        obj.save()
        obj_id = str(obj.id)
        form = CreateWorkoutForm()
        return redirect('workout/' + obj_id)
    context['form'] = form

    return render(request, 'workitout/create-workout.html', context)

def must_authenticate(request):

    return render(request, 'workitout/must_authenticate.html')


def search(request):

    return render(request, 'workitout/search.html')

def about(request):

    return render(request, 'workitout/about.html')
    

def exercises(request):

    exercise_list = Exercise.objects.order_by('muscle_group')
    context_dict={}
    context_dict['exercises'] = exercise_list

    #context_dict['image_paths'] = ["images\\exercises\\" + exercise_title_slug + "-1.png", "images\\exercises\\" + exercise_title_slug + "-2.png"]
    return render(request, 'workitout/exercises.html', context_dict)

def user_page(request, user_name):
    context_dict = {}
    try:
        saved = []
        created = []
        user_obj = User.objects.get(username=user_name)
        user1 = UserProfile.objects.get(user=user_obj)

        for w in user1.saved.all():
            w.numLikes = len(w.likes.all())
            saved.append(w)
        
        for w in Workout.objects.filter(creator=user_obj):
            w.numLikes = len(w.likes.all())
            created.append(w)


        context_dict['user'] = user1
        context_dict['username'] = user_obj.username
        context_dict['picture'] = user1.picture
        context_dict['bio'] = user1.bio
        context_dict['following'] = len(user1.following.all())
        context_dict['followers'] = len(user1.followers.all())
        context_dict['verified'] = user1.isVerified
        context_dict['private'] = user1.isPrivate
        context_dict['saved'] = saved
        context_dict['created'] = created
    except User.DoesNotExist:
        context_dict['user'] = None

    return render(request, 'workitout/user-page.html',context=context_dict)

@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('workitout:home'))
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'workitout/profile_registration.html', context_dict)



def exercise_page(request, exercise_title_slug):
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



def workout_page(request, workout_id):
    context_dict = {}
    try:
        workout = Workout.objects.get(id=workout_id)

        context_dict['title'] = workout.title
        context_dict['description'] = workout.description
        context_dict['creator'] = workout.creator.username
        context_dict['duration'] = workout.duration
        context_dict['difficulty'] = workout.difficulty
        context_dict['likes'] = len(workout.likes.all())
        context_dict['tags'] = [t.name for t in workout.tags.all()]
        context_dict['date_published'] = workout.date_published

        exercises = [(exiw.exercise.title, exiw.sets, exiw.reps) for exiw in ExInWorkout.objects.filter(workout=workout)]
        context_dict['exercises'] = exercises

    except Workout.DoesNotExist:
        context_dict['workout'] = None

    return render(request, 'workitout/workout.html', context=context_dict)