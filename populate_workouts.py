import json

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_project.settings')
django.setup()
from django.contrib.auth.models import User
from workitout.models import UserProfile, Workout, ExInWorkout
from workitout.models import Muscle, Tag, Equipment
from workitout.models import Exercise, Description, MuscleGroup

def populate():

    users = [{'username':'TheChadinator', 'email': 'chadsmith@hotmail.co.uk', 'password': 'Password2', 'picture':'profile_images/userimage2.jpg','bio':"Chad by name, chad by nature. I love building muscle and being the centre of attention, u guys will LOVE my workouts"},
            {'username': 'SallyJ', 'email': 'sjones100@hotmail.co.uk', 'password': 'Password3', 'picture':'profile_images/userimage3.png','bio': 'Just ur average gym mom'},
            {'username': 'jwilson87', 'email': 'jw1987@gmail.com', 'password': 'Password1', 'picture':'profile_images/userimage1.jpg', 'bio':'i love dogs and losing weight'},
            {'username': 'BobertoShm', 'email': 'bb777@gmail.com', 'password': 'Password1', 'picture':'', 'bio':'Not good with computers'},
            {'username': 'TheFatty343434', 'email': 'fattestman7@gmail.com', 'password': 'Password1', 'picture':'profile_images/userimage5.png', 'bio':'im trying to lose weight as I am the biggest guy, but I have the biggest heart to go with it'},
            {'username': 'Jadeeeyyyyyy', 'email': 'jadethebomb@hotmail.co.uk', 'password': 'Password3', 'picture':'profile_images/userimage6.png','bio': 'Coolest gal in the gym, AT ALL TIMES!'}]

    for user in users:
        username=user['username']
        email=user['email']
        password = user['password']
        u = User.objects.get_or_create(username=username, email=email, password=password)[0]
        if username== 'TheChadinator':
            up = UserProfile.objects.get_or_create(user=u,picture=user['picture'],bio=user['bio'],isVerified=True)[0]
        else:
            up = UserProfile.objects.get_or_create(user=u,picture=user['picture'],bio=user['bio'])[0]

        followUser = User.objects.get(username='TheChadinator')
        if followUser != u:
            up.followers.add(followUser)
            up.following.add(followUser)

    workouts = [{'creator': 'SallyJ', 'title': 'Stronglifts',
    'description': 'A fullbody workout for building strength.',
    'duration': 60,
    'exercises': [['Squats: Barbell',5,5],['Bench Press: Barbell',5,5],['Pull Down: V Bar',5,5]]},

    {'creator': 'TheChadinator', 'title': 'The ultimate lower burn',
    'description': 'A workout dedicated to CRUSHING your lower half. Get ready to get those legs you have always dreamed of!',
    'duration': 30,
    'exercises': [['Squats: Barbell',3,15],['Side Squats: Barbell',2,7],['Pull Down: V Bar',2,17],['Bench Leg Raises',2,11],['Step Ups: Barbell',4,5],['Thigh Abductor',1,5]]},
    
    {'creator': 'TheChadinator', 'title': 'Super quick fat burn',
    'description': 'This is a super quick and simple workout for those with busy lives!',
    'duration': 15,
    'exercises': [['Push Up',3,15],['Bicep Curls: Dumbbell',3,8],['Lying Squat',3,8]]},

    {'creator': 'TheChadinator', 'title': 'Big Arm Builder',
    'description': 'A workout for building big arms.',
    'duration': 45,
    'exercises': [['Bicep Curls: Dumbbell',3,8],['Chin Ups',3,8],['Triceps Pushdown: Cable',3,8]]}]
    
    for workout in workouts:
        creator = User.objects.get(username=workout['creator'])
        title = workout['title']
        description = workout['description']
        duration=workout['duration']
        exercises = workout['exercises']

        w = Workout.objects.get_or_create(creator=creator, title=title, description=description, duration=duration)[0]
        w.likes.add(User.objects.get(username='TheChadinator'))
        for exercise in exercises:
            ex_title = exercise[0]
            sets = exercise[1]
            reps = exercise[2]
            e = Exercise.objects.get(title=ex_title)
            exiw = ExInWorkout.objects.get_or_create(workout=w, exercise=e, sets=sets, reps=reps)[0]

    t_u = User.objects.get(username="TheChadinator")   
    testUser= UserProfile.objects.get(user=t_u)
    
    for w in Workout.objects.all():
        testUser.saved.add(w)

    for u in User.objects.all():
        if u!= t_u:
            up=UserProfile.objects.get(user=u)
            up.following.add(t_u)
            testUser.followers.add(u)
             


if __name__ == '__main__':
    print('Starting workout population script...')
    populate()
