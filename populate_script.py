#!/usr/bin/env python

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wad_project.settings')
import json
import django
django.setup()
from django.contrib.auth.models import User
from workitout.models import UserProfile, Workout, ExInWorkout
from workitout.models import Muscle, Tag, Equipment

from workitout.models import Exercise, Description, MuscleGroup, Muscle, Tag, Equipment
import random

def populate():

    
    muscle_groups = read_json("db_data/muscle_groups.json")
    for muscle_group in muscle_groups:
        mg = MuscleGroup.objects.get_or_create(name=muscle_group)[0]

    muscles = read_json("db_data/muscles.json")
    for muscle in muscles:
        m = Muscle.objects.get_or_create(name=muscle)[0]

    tags = read_json("db_data/tags.json")
    for tag in tags:
        t = Tag.objects.get_or_create(name=tag)[0]

    equipment = read_json("db_data/equipment_list.json")   
    for equip in equipment:
        eq = Equipment.objects.get_or_create(name=equip)[0]
    


    exercises = read_json("db_data/everkinetic.json")
    for ex in exercises:
        title = ex['title']
        difficulty = ex['difficulty']
        primer = ex['primer']
        steps = ex['steps_string']
        tips = ex['tips_string']

        muscle_group = ex['category']
        muscles = ex['muscles']
        tags = ex['tags']
        equipment = ex['equipment']
        add_exercise(title, difficulty, primer, steps, tips, muscle_group, muscles, tags, equipment)

    populate_workouts()

def add_exercise(title, difficulty, primer, steps, tips, muscle_group, muscles, tags, equipment):

    d = Description.objects.get_or_create(primer=primer, steps=steps, tips=tips)[0]
    mg = MuscleGroup.objects.get_or_create(name=muscle_group)[0]

    
    ex = Exercise.objects.get_or_create(title=title, difficulty=difficulty, description=d, muscle_group=mg)[0]

    for muscle in muscles:
        m = Muscle.objects.get_or_create(name=muscle)[0]
        ex.muscles.add(m)
        ex.save()

    for tag in tags:
        if len(tag) > 1:
            t = Tag.objects.get_or_create(name=tag)[0]
            ex.tags.add(t)
            ex.save()
    
    for equip in equipment:
        eq = Equipment.objects.get_or_create(name=equip)[0]
        ex.equipment.add(eq)
        ex.save()
    
    return ex


def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def populate_workouts():
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
        if username== 'TheChadinator'or username=='SallyJ':
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


    numUsers=25
    

    for i in range(numUsers):
        str_i=str(i)
       
        temp=User.objects.get_or_create(username=('user'+str_i),email=('user'+str_i+'@mail.com'),password='easypass321','picture':'profile_images/default_user.png')[0]
       
        UserProfile.objects.get_or_create(user=temp,bio='I love just being a generic user!')
        
        create_rand_workout(temp)
        
        


   

    t_u = User.objects.get(username="TheChadinator")   
    testUser= UserProfile.objects.get(user=t_u)
    chad_workout=Workout.objects.get_or_create(title="Big Arm Builder")[0]
    for w in Workout.objects.all():
        testUser.saved.add(w)

    for u in User.objects.all():
        if u!= t_u:
            up=UserProfile.objects.get(user=u)
            up.saved.add(chad_workout)
            up.following.add(t_u)
            testUser.followers.add(u)





def create_rand_workout(user):
    
    numExcercises = random.randint(2, 14)
    w = Workout.objects.get_or_create(creator=user, title=user.username+"'s workout!", description="This workout is a killer!", duration=numExcercises*5)[0]
    exercise_list=list(Exercise.objects.all())
    
    for i in range(numExcercises):
        e=random.choice(exercise_list)
        exercise_list.remove(e)
        ExInWorkout.objects.get_or_create(workout=w,exercise=e,sets=random.randint(1, 5),reps=random.randint(5,15))
        

    

if __name__ == '__main__':
    print('Starting population script...')
    populate()
    