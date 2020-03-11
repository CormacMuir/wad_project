from django.contrib import admin
from workitout.models import Exercise
from workitout.models import UserProfile
from workitout.models import Workout
from workitout.models import MuscleGroup
from workitout.models import Muscle
from workitout.models import Tag
from workitout.models import Equipment


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class MuscleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(MuscleGroup, MuscleGroupAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(UserProfile)
admin.site.register(Workout, WorkoutAdmin)
