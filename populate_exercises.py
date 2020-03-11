import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wad_project.settings')

import django
django.setup()
from workitout.models import Exercise, Description, MuscleGroup, Muscle, Tag, Equipment

def populate():


    with open("db_data/everkinetic.json", 'r') as f:
        exercises = json.load(f)

 
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
        t = Tag.objects.get_or_create(name=tag)[0]
        ex.tags.add(t)
        ex.save()
    
    for equip in equipment:
        eq = Equipment.objects.get_or_create(name=equip)[0]
        ex.equipment.add(eq)
        ex.save()
    
    return ex


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()