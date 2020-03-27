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
            {'username': 'jwilson87', 'email': 'jw1987@gmail.com', 'password': 'Password1', 'picture':'profile_images/userimage1.jpg', 'bio':'i love dogs and losing weight'},
            {'username': 'SallyJ', 'email': 'sjones100@hotmail.co.uk', 'password': 'Password3', 'picture':'profile_images/userimage3.png','bio': 'Just ur average gym mom'}]

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
    {'creator': 'TheChadinator', 'title': 'Big Arm Builder',
    'description': 'A workout for building big arms.',
    'duration': 45,
    'exercises': [['Bicep Curls: Dumbbell',3,8],['Chin Ups',3,8],['Triceps Pushdown: Cable',3,8]]}]
    
    for workout in workouts:
        creator = User.objects.get(username=workout['creator'])
        title = workout['title']
        description = workout['description']
        duration=workout['duration']
        #placeholder difficulty
        difficulty = 8
        exercises = workout['exercises']

        w = Workout.objects.get_or_create(creator=creator, title=title, description=description, duration=duration, difficulty=difficulty)[0]
        w.likes.add(User.objects.get(username='TheChadinator'))
        for exercise in exercises:
            ex_title = exercise[0]
            sets = exercise[1]
            reps = exercise[2]
            e = Exercise.objects.get(title=ex_title)
            exiw = ExInWorkout.objects.get_or_create(workout=w, exercise=e, sets=sets, reps=reps)[0]

    u = User.objects.get(username="TheChadinator")   
    testSaveWorkoutUser = UserProfile.objects.get(user=u)
    
    for w in Workout.objects.all():
        testSaveWorkoutUser.saved.add(w)

    testSaveWorkoutUser.saved              


if __name__ == '__main__':
    print('Starting workout population script...')
    populate()
