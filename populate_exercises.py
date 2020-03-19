import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wad_project.settings')

import django
django.setup()
from workitout.models import Exercise, Description, MuscleGroup, Muscle, Tag, Equipment

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
        image_id = ex['id']
        primer = ex['primer']
        steps = ex['steps_string']
        tips = ex['tips_string']

        muscle_group = ex['category']
        muscles = ex['muscles']
        tags = ex['tags']
        equipment = ex['equipment']
        
        add_exercise(title, difficulty, image_id, primer, steps, tips, muscle_group, muscles, tags, equipment)


def add_exercise(title, difficulty, image_id, primer, steps, tips, muscle_group, muscles, tags, equipment):

    d = Description.objects.get_or_create(primer=primer, steps=steps, tips=tips)[0]
    mg = MuscleGroup.objects.get_or_create(name=muscle_group)[0]

    
    ex = Exercise.objects.get_or_create(title=title, difficulty=difficulty, image_id=image_id, description=d, muscle_group=mg)[0]

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

if __name__ == '__main__':
    print('Starting exercise population script...')
    populate()