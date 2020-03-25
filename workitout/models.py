from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


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
    description = models.OneToOneField(Description, on_delete=models.PROTECT)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT)
    muscles = models.ManyToManyField(Muscle)
    tags = models.ManyToManyField(Tag)
    equipment = models.ManyToManyField(Equipment)
    slug=models.SlugField(unique=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Exercise, self).save(*args, **kwargs)

class Workout(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name='workout_creator', on_delete=models.CASCADE)
    duration = models.IntegerField()
    difficulty = models.IntegerField()
    likes = models.ManyToManyField(User, related_name='workout_likes')
    tags = models.ManyToManyField(Tag)
    isPrivate = models.BooleanField(default=False)
    slug=models.SlugField(unique=False)


    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Workout, self).save(*args, **kwargs)


class ExInWorkout(models.Model):

    workout = models.ForeignKey(Workout,default = 1, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()


class UserProfile(models.Model):
    # Link UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional attributes we wish to include
    bio = models.TextField()
    picture = models.ImageField(upload_to='profile_images', blank=True)
    saved = models.ManyToManyField(Workout)
    followers = models.ManyToManyField(User, related_name='user_followers', blank=True)
    following = models.ManyToManyField(User, related_name='user_following', blank=True)
    isPrivate = models.BooleanField(default=False)  #default is public and they set private
    isVerified = models.BooleanField(default=False) #default user is not verified

    def __str__(self):
        return self.user.username