from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from workitout.models import Workout , Exercise, UserProfile, ExInWorkout, Tag, Equipment, MuscleGroup, Muscle
from django.forms.models import model_to_dict
from workitout.forms import UserProfileForm,EditProfileForm,EditUserProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views import View
from workitout.forms import CreateWorkoutForm



# marty add
from django.db.models import Q
from operator import attrgetter

def home(request):

    context_dict={}

    # marty added code here
    query = ""
    if request.GET:
        query = request.GET['q']
        context_dict['query'] = str(query)

    # queries and returns the newest first
    workout_list=sorted(get_workout_queryset(query), key=attrgetter('date_published'), reverse=True)
    context_dict['randvar'] = True
    context_dict['workouts'] = workout_list
    context_dict['username'] = request.user.username
    return render(request, 'workitout/home.html', context_dict)


def create_workout(request):

    context = {}

    # if user isnt authenticated then prompt them to login/register
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('workitout:must_authenticate'))

    context['username'] = request.user.username
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
    context['randvar'] = True
    return render(request, 'workitout/create-workout.html', context)

def must_authenticate(request):

    return render(request, 'workitout/must_authenticate.html')


def search(request):
    #dont remove the 2 lines below
    context_dict = {}
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True
    return render(request, 'workitout/search.html',context_dict)

def about(request):
    #dont remove the 2 lines below
    context_dict = {}
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True
    return render(request, 'workitout/about.html',context_dict)

@login_required   
def edit_profile(request):
   
    if request.method=='POST':

        form=EditProfileForm(request.POST,instance=request.user)
        profile_form=EditUserProfileForm(request.POST,request.FILES,instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user_form
            profile.save()
            return redirect(reverse('workitout:user_page',args=[request.user.username]))
        
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = EditUserProfileForm(instance=request.user.userprofile)
        
        context_dict={'form':form,'profile_form':profile_form}
        context_dict['randvar'] = True
        context_dict['username'] = request.user.username
        return render(request,'workitout/edit-profile.html',context=context_dict)


def user_page(request, user_name):

    context_dict = {}
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True

    try:
        print("in try")

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
            
        context_dict['isFollower'] = "false"

        for u in user1.followers.all():
            if u == request.user:
                context_dict['isFollower'] = "true"
                break
            
        if request.user!=user_obj:
            context_dict['self_view'] = False
        else:
            context_dict['self_view'] = True



        context_dict['userProfile'] = user1
        context_dict['profile_username'] = user_obj.username
        try:
            context_dict['picture'] = user1.picture
        except user1.picture.DoesNotExist:
            #context_dict_dict['picture'] = None
            context_dict['picture'] = None

        context_dict['bio'] = user1.bio
        context_dict['following'] = len(user1.following.all())
        context_dict['followers'] = len(user1.followers.all())
        context_dict['verified'] = user1.isVerified
        context_dict['private'] = user1.isPrivate
        context_dict['saved'] = saved
        context_dict['created'] = created
        context_dict['current_user'] = request.user
        
    except User.DoesNotExist:
        context_dict['userProfile'] = None
    
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


def exercises(request):

    context_dict={}

    query = ""
    filters  = {'muscle_group':"", 'equipment':"", 'ex_type':""}
    if request.GET:
        request_parameters = request.GET

        query = request_parameters.get('q',"")
        if query != "":
            context_dict['query'] = str(query)
        filters['muscle_group'] = request_parameters.get('muscle_group',"")
        filters['equipment'] = request_parameters.get('equipment',"")
        filters['ex_type'] = request_parameters.get('ex_type',"")
    
    exercise_list, filter_objs = get_exercise_queryset(query, filters)
    context_dict['filter_objs'] = filter_objs

    if filter_objs == []:
        del context_dict['filter_objs']

    for ex in exercise_list:
        
        ex.image1 = "images\\exercises\\" + ex.slug + "-1.png"
        ex.image2 = "images\\exercises\\" + ex.slug + "-2.png"

    
    
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True
    context_dict['exercises'] = exercise_list
    context_dict['equipment'] = Equipment.objects.all()
    context_dict['muscle_groups'] = MuscleGroup.objects.all()
    context_dict['muscles'] = Muscle.objects.all()
    context_dict['ex_type'] = ["push", "pull", "upper", "lower"]

    return render(request, 'workitout/exercises.html', context_dict)


def get_exercise_queryset(query=None, filters={}):

    filter_objs = []

    queries = query.split(" ")
    queryset = Exercise.objects.filter( Q(title__icontains=queries[0]) )
    for query in queries:
        queryset = queryset.intersection(Exercise.objects.filter( Q(title__icontains=query) ))
    
    try:
        mg = MuscleGroup.objects.get(name=filters['muscle_group'])
        filter_objs.append(mg)
        qs2 = Exercise.objects.filter(muscle_group=mg)
        queryset = queryset.intersection(qs2)
    except MuscleGroup.DoesNotExist:
        pass
    
    try:
        eq = Equipment.objects.get(slug=filters['equipment'])
        filter_objs.append(eq)
        qs3 = Exercise.objects.filter(equipment__in=[eq])
        queryset = queryset.intersection(qs3)
    except Equipment.DoesNotExist:
        pass

    try:
        t = Tag.objects.get(name=filters['ex_type'])
        filter_objs.append(t)
        qs4 = Exercise.objects.filter(tags__in=[t])
        queryset = queryset.intersection(qs4)
    except Tag.DoesNotExist:
        pass

    return list(set(queryset)), filter_objs



class LikeWorkoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        workout_id = request.GET['workout_id']
        user_id = request.GET['user_id']
        toLike = request.GET['like']
        try:
            workout = Workout.objects.get(id=workout_id)
            
        except Workout.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        
        if toLike=="true":
            workout.likes.add(User.objects.get(id=user_id))        
            workout.save()
            return HttpResponse(len(workout.likes.all()))
        else:
            workout.likes.remove(User.objects.get(id=user_id))        
            workout.save()
            return HttpResponse(len(workout.likes.all()))

class FollowUserView(View):
    @method_decorator(login_required)
    def get(self, request):
        
        follower_id= request.GET['follower_id']
        user_id = request.GET['user_id']
        to_follow = request.GET['to_follow']

        try:
            follower_user = User.objects.get(id=follower_id)
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        follower_profile = UserProfile.objects.get(user = follower_user)
        user_profile = UserProfile.objects.get(user = user)
        
        if to_follow =="true":
            user_profile.followers.add(follower_user)
            user_profile.save()
            follower_profile.following.add(user)
            follower_profile.save()
            return HttpResponse(len(user_profile.followers.all()))
        else:
            user_profile.followers.remove(follower_user)
            user_profile.save()
            follower_profile.following.remove(user)
            follower_profile.save()
            return HttpResponse(len(user_profile.followers.all()))

class SaveWorkoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        
        workout_id = request.GET['workout_id']
        user_id = request.GET['user_id']
        to_save = request.GET['to_save']

        try:
            user = User.objects.get(id=user_id)
            workout = Workout.objects.get(id=workout_id)
        except Workout.DoesNotExist:
            
            return HttpResponse(-1)
        except ValueError:
            
            return HttpResponse(-1)
        except User.DoesNotExist:
            
            return HttpResponse(-1)
        
        user_profile = UserProfile.objects.get(user = user)
        
        
        if to_save =="true":
        
            user_profile.saved.add(workout)
            return HttpResponse(str(workout.title))
        else:
            user_profile.saved.remove(workout)
            return HttpResponse(str(workout.title))

def exercise_page(request, exercise_title_slug):
    context_dict = {}
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True
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



def workout_page(request, workout_id,creator):
    context_dict = {}
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True
    try:
        workout = Workout.objects.get(id=workout_id)
        if request.user.is_authenticated:
            currentProfile = UserProfile.objects.get(user=request.user)
            if workout in currentProfile.saved.all():
                print("in here")
                context_dict['is_saved'] = True
            else:
                context_dict['is_saved'] = False
                
            if request.user in workout.likes.all():
                context_dict['has_liked'] = True
                
            else:
                context_dict['has_liked'] = False
        
        context_dict['user'] = request.user
        context_dict['workout'] = workout
        context_dict['creator'] = workout.creator.username
        context_dict['likes'] = len(workout.likes.all())
        context_dict['tags'] = [t.name for t in workout.tags.all()]

        exercises = [(exiw.exercise.title, exiw.sets, exiw.reps) for exiw in ExInWorkout.objects.filter(workout=workout)]
        context_dict['exercises'] = exercises

        
    except Workout.DoesNotExist:
        context_dict['workout'] = None

    return render(request, 'workitout/workout.html', context=context_dict)


def get_workout_queryset(query=None):

    queryset = []

    queries = query.split(" ") # 'shoulder workout 2020' becomes ['shoulder', 'workout', '2020']

    for q in queries:
        posts = Workout.objects.filter( 
            Q(title__icontains=q) | 
            Q(description__icontains=q) 
            ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list

    return list(set(queryset)) 


