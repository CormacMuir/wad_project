from django.db import models
from django.contrib.auth.models import User


class MuscleGroup(models.Model):

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Muscle(models.Model):

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Equipment(models.Model):

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Description(models.Model):

    primer = models.CharField(max_length=256)
    # steps/tips lists are stored as strings
    # use .split('$$') to get lists
    steps = models.TextField()
    tips = models.TextField()

class Exercise(models.Model):

    title = models.CharField(max_length=128)
    difficulty = models.IntegerField()
    image_id = models.CharField(max_length=16)
    description = models.OneToOneField(Description, on_delete=models.PROTECT)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT)
    muscles = models.ManyToManyField(Muscle)
    tags = models.ManyToManyField(Tag)
    equipment = models.ManyToManyField(Equipment)

    def __str__(self):
        return self.title

class ExInWorkout(models.Model):

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()

class Workout(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name='workout_creator', on_delete=models.CASCADE)
    duration = models.IntegerField()
    difficulty = models.IntegerField()
    likes = models.ManyToManyField(User, related_name='workout_likes')
    tags = models.ManyToManyField(Tag)
    isPrivate = models.BooleanField(default=False)

    exercises = models.ManyToManyField(Exercise) #use exercise id to find ExInWorkout which has the sets and reps

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # Link UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional attributes we wish to include
    bio = models.TextField()
    picture = models.ImageField(upload_to='profile_images', blank=True)
    saved = models.ManyToManyField(Workout)
    followers = models.ManyToManyField(User, related_name='user_followers')
    following = models.ManyToManyField(User, related_name='user_following')
    isPrivate = models.BooleanField(default=False)  #default is public and they set private
    isVerified = models.BooleanField(default=False) #default user is not verified

    def __str__(self):
        return self.user.username