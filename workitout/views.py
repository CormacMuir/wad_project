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
from django.contrib.staticfiles import finders
import random

from workitout.forms import CreateWorkoutForm, AddExerciseForm



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
    #workout_list=sorted(get_workout_queryset(query), key=attrgetter('date_published'), reverse=True)
    context_dict['randvar'] = True
    context_dict['workouts'] = Workout.objects.all()
    context_dict['username'] = request.user.username
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
        workout_list = Workout.objects.order_by("creator")
        maxID = 0
        for workout in workout_list:
            if workout.creator == user:
                if workout.id > maxID:
                    maxID = workout.id
        workout = Workout.objects.get(id=(maxID))
        exercises = [(exiw.exercise.title) for exiw in ExInWorkout.objects.filter(workout=workout)]
        if len(exercises) >= 2:
            obj = form.save(commit=False)
            obj.creator = user
            obj.workout = workout
            obj.id = maxID
            obj.save(update_fields=['title','description','isPrivate'])
            
            form = CreateWorkoutForm()
            return redirect('workout/' + obj.creator.username + "/" + str(maxID) + "/")
        else:
            context['error'] = True
    else:
        obj = form.save(commit=False)
        obj.creator = user
        obj.save()
    context['form'] = form


    return render(request, 'workitout/create-workout.html', context)

def add_exercise(request):
    user = request.user
    context_dict={}

    form = AddExerciseForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)

        workout_list = Workout.objects.order_by("creator")
        maxID = 0
        has_created = False

        for workout in workout_list:
            if workout.creator == user:
                has_created = True
                if workout.id > maxID:
                    maxID = workout.id

        obj.workout = Workout.objects.get(id=(maxID))
        obj.save()
        form = AddExerciseForm()
    
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    context_dict['form'] = form

    return render(request, 'workitout/add-exercise.html', context_dict)







def must_authenticate(request):

    return render(request, 'workitout/must_authenticate.html')


def search(request):
    #dont remove the 2 lines below
    context_dict = {}
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True

    top_users = [up.user for up in UserProfile.objects.filter(isVerified=True)]
    
    if len(top_users) >= 5:
        context_dict['top_users'] = random.sample(top_users, 5)
    else:
        context_dict['top_users'] = top_users
    context_dict['user_profiles'] = UserProfile.objects.filter(user__in=top_users)

    top_workouts = Workout.objects.all().order_by('likes')
    if len(top_workouts) >= 5:
        context_dict['top_workouts'] = top_workouts[:5]
    else:
        context_dict['top_workouts'] = top_workouts

    top_exercises = Exercise.objects.all().order_by('usage')
    for ex in top_exercises:
        
        ex.image1 = "images\\exercises\\" + ex.slug + "-1.png"
        ex.image2 = "images\\exercises\\" + ex.slug + "-2.png"
    if len(top_exercises) >= 5:
        context_dict['top_exercises'] = top_exercises[:5]
    else:
        context_dict['top_exercises'] = top_exercises

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
            #user_form = form.save()

            user_form = form.save(commit=False)
            user_form.save()
            
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
        if user1.picture=='':
            context_dict['picture'] = None
        else:
            context_dict['picture']=user1.picture
        

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
    filters  = {'muscle_group':"", 'equipment':"", 'ex_type':"", 'diff':""}
    if request.GET:
        request_parameters = request.GET

        query = request_parameters.get('q',"")
        if query != "":
            context_dict['query'] = str(query)
        filters['muscle_group'] = request_parameters.get('muscle_group',"")
        filters['equipment'] = request_parameters.get('equipment',"")
        filters['ex_type'] = request_parameters.get('ex_type',"")
        filters['diff'] = request_parameters.get('diff',"")

    
    exercise_list, filter_objs = get_exercise_queryset(query, filters)
    context_dict['filter_objs'] = filter_objs

    if filters['muscle_group'] != "":
        context_dict['mg_filter'] = filter_objs['mg_filter']

    if filters['equipment'] != "":
        context_dict['eq_filter'] = filter_objs['eq_filter']

    if filters['ex_type'] != "":
        context_dict['t_filter'] = filter_objs['t_filter']

    if filters['diff'] != "":
        context_dict['diff_filter'] = filters['diff']

    for ex in exercise_list:
        
        ex.image1 = "images\\exercises\\" + ex.slug + "-1.png"
        ex.image2 = "images\\exercises\\" + ex.slug + "-2.png"

    
    
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True
    context_dict['exercises'] = exercise_list
    context_dict['equipment'] = Equipment.objects.all().order_by('name')
    context_dict['muscle_groups'] = MuscleGroup.objects.all().order_by('name')
    context_dict['difficulties'] =  ["beginner", "intermediate", "advanced"]
    context_dict['ex_type'] = ["push", "pull", "upper", "lower"]

    return render(request, 'workitout/exercises.html', context_dict)


def get_exercise_queryset(query=None, filters={}):

    filter_objs = {}

    queries = query.split(" ")
    queryset = Exercise.objects.filter( Q(title__icontains=queries[0]) )
    for query in queries:
        queryset = queryset.intersection(Exercise.objects.filter( Q(title__icontains=query) ))
    
    try:
        mg = MuscleGroup.objects.get(name=filters['muscle_group'])
        filter_objs['mg_filter']= mg
        qs2 = Exercise.objects.filter(muscle_group=mg)
        queryset = queryset.intersection(qs2)
    except MuscleGroup.DoesNotExist:
        pass
    
    try:
        eq = Equipment.objects.get(slug=filters['equipment'])
        filter_objs['eq_filter']= eq
        qs3 = Exercise.objects.filter(equipment__in=[eq])
        queryset = queryset.intersection(qs3)
    except Equipment.DoesNotExist:
        pass

    try:
        t = Tag.objects.get(name=filters['ex_type'])
        filter_objs['t_filter']= t
        qs4 = Exercise.objects.filter(tags__in=[t])
        queryset = queryset.intersection(qs4)
    except Tag.DoesNotExist:
        pass

    if filters['diff'] != "":
        diffs = {"beginner":1, "intermediate":2, "advanced":3}
        qs4 = Exercise.objects.filter(difficulty=diffs[filters['diff']])
        queryset = queryset.intersection(qs4)


    return list(set(queryset)), filter_objs



def workouts(request):

    context_dict={}

    query = ""
    filters  = {'tag':"", 'equipment':"", 'diff':"", 'dur':0}
    if request.GET:
        request_parameters = request.GET

        query = request_parameters.get('workout_q',"")
        if query != "":
            context_dict['query'] = str(query)
        filters['tag'] = request_parameters.get('tag',"")
        filters['equipment'] = request_parameters.get('equipment',"")
        filters['diff'] = request_parameters.get('diff',"")
        filters['dur'] = request_parameters.get('duration', 0)

    
    workout_list, filter_objs = get_workout_queryset(query, filters)
    context_dict['filter_objs'] = filter_objs

    if filters['tag'] != "":
        context_dict['tag_filter'] = filter_objs['tag_filter']

    if filters['equipment'] != "":
        context_dict['eq_filter'] = filter_objs['eq_filter']

    if filters['diff'] != "":
        context_dict['diff_filter'] = filters['diff']

    if filters['dur'] != 0:
        print(filters['dur'])
        context_dict['dur_filter'] = filters['dur']


    
    
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True
    context_dict['workouts'] = workout_list
    context_dict['equipment'] = Equipment.objects.all().order_by('name')
    context_dict['tags'] = Tag.objects.all().order_by('name')
    context_dict['difficulties'] =  ["beginner", "intermediate", "advanced"]




    return render(request, 'workitout/workouts.html', context_dict)


def get_workout_queryset(query=None, filters={}):

    filter_objs = {}

    queries = query.split(" ")
    queryset = Workout.objects.filter( Q(title__icontains=queries[0]) )
    for query in queries:
        queryset = queryset.intersection(Workout.objects.filter( Q(title__icontains=query) ))
    
    try:
        t = Tag.objects.get(name=filters['tag'])
        filter_objs['tag_filter']= t
        qs1 = Workout.objects.filter(tags__in=[t])
        queryset = queryset.intersection(qs1)
    except Tag.DoesNotExist:
        pass
    
    try:
        eq = Equipment.objects.get(slug=filters['equipment'])
        filter_objs['eq_filter']= eq
        qs3 = Workout.objects.filter(equipment__in=[eq])
        queryset = queryset.intersection(qs3)
    except Equipment.DoesNotExist:
        pass

    if filters['diff'] != "":
        diffs = {"beginner":1, "intermediate":2, "advanced":3}
        qs4 = Workout.objects.filter(difficulty=diffs[filters['diff']])
        queryset = queryset.intersection(qs4)

    if filters['dur'] != 0:
        
        qs4 = Workout.objects.filter(duration__lte=filters['dur'])
        queryset = queryset.intersection(qs4)

    


    return list(set(queryset)), filter_objs


def users(request):

    context_dict={}

    query = ""
    verified = False
    if request.GET:
        request_parameters = request.GET
        query = request_parameters.get('user_q',"")
        if query != "":
            context_dict['query'] = str(query)

        if 'verified' in request_parameters.keys():
            verified = True
            context_dict['ver_filter'] = verified

    user_list = get_user_queryset(query, verified)

    context_dict['username'] = request.user.username
    context_dict['randvar'] = True
    context_dict['users'] = user_list
    context_dict['user_profiles'] = UserProfile.objects.filter(user__in=user_list)

    return render(request, 'workitout/users.html', context_dict)


def get_user_queryset(query=None, verified=False):
    
    queryset = User.objects.filter(Q(username__icontains=query))

    user_profiles = UserProfile.objects.filter(user__in=queryset)

    queryset = list(queryset)

    for user_p in user_profiles:
        if verified:
            if not user_p.isVerified:
                queryset.remove(user_p.user)

    return list(set(queryset))





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

class DeleteWorkoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        workout_id = request.GET['workout_id']
    
        try:
            workout = Workout.objects.get(id=workout_id)
            ex_list= ExInWorkout.objects.filter(workout=workout)
            
        except Workout.DoesNotExist:
            return HttpResponse(-1)
        except ExInWorkout.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        for e in ex_list:
            e.delete()
        workout.delete()
        return HttpResponse(1)
        

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
        
        context_dict['difficulty'] = exercise.difficulty
        context_dict['primer'] = exercise.description.primer
        steps_list=exercise.description.steps.split('$$')
        
        class steps_obj:
            def __init__(self, step,num):
                self.step=step
                self.num=num

        steps_obj_list=[]
        for i in range(len(steps_list)):
            steps_obj_list.append(steps_obj(steps_list[i],i+1))

        context_dict['steps'] = steps_obj_list
        context_dict['tips'] = exercise.description.tips.split('$$')
        if context_dict['tips'] == ['']:
            context_dict['tips'] = None



        mg = exercise.muscle_group.__str__()
        
        context_dict['muscle_group'] = mg.capitalize()
        context_dict['muscles'] = [m.name for m in exercise.muscles.all()]
        context_dict['tags'] = [t.name for t in exercise.tags.all()]
        context_dict['equipment'] = [e.name for e in exercise.equipment.all()]
        context_dict['image_paths'] = ["images\\exercises\\" + exercise_title_slug + "-1.png", "images\\exercises\\" + exercise_title_slug + "-2.png"]

       

    except Exercise.DoesNotExist:
        context_dict['exercise'] = None

    return render(request, 'workitout/exercise.html', context=context_dict)



def workout_page(request, workout_id,creator):

    ex_in_workout = []


    context_dict = {}
    context_dict['username'] = request.user.username
    context_dict['randvar'] = True
    try:
        workout = Workout.objects.get(id=workout_id)
        if request.user.is_authenticated:
            currentProfile = UserProfile.objects.get(user=request.user)
            if workout in currentProfile.saved.all():
                
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
        context_dict['equipment'] = [eq.name for eq in workout.equipment.all()]



        

        exercises_temp = [(exiw.exercise, exiw.sets, exiw.reps) for exiw in ExInWorkout.objects.filter(workout=workout)]
        
        class exercise_obj:
            def __init__(self, exercise, sets,reps):
                self.exercise=exercise
                self.sets=sets
                self.reps=reps
                


        exercises=[]
        for e in exercises_temp:
            ex=exercise_obj(e[0],e[1],e[2])
            ex.steps=ex.exercise.description.steps.split('$$')
            ex.tips=ex.exercise.description.tips.split('$$')
            
            if finders.find("images\\exercises\\" + ex.exercise.slug + "-1.png")==None:
                ex.image1="images\\image_not_found.png"
            else:
                ex.image1 = "images\\exercises\\" + ex.exercise.slug + "-1.png"

            if finders.find("images\\exercises\\" + ex.exercise.slug + "-2.png")==None:
                 ex.image2 ="images\\image_not_found.png"
            else:
                ex.image2 = "images\\exercises\\" + ex.exercise.slug + "-2.png"
            exercises.append(ex)


        context_dict['exercises'] = exercises
        context_dict['ex_num']=len(exercises_temp)


    except Workout.DoesNotExist:
        context_dict['workout'] = None

    return render(request, 'workitout/workout.html', context=context_dict)



