from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save


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
    slug=models.SlugField(unique=True)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Equipment, self).save(*args, **kwargs)


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

    # required 
    title = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(max_length=5000, null=False, blank=False)
    
    creator = models.ForeignKey(User, related_name='workout_creator', on_delete=models.CASCADE)
    
    duration = models.IntegerField(default=69)
    difficulty = models.IntegerField(default=1)
    likes = models.ManyToManyField(User, related_name='workout_likes')
    tags = models.ManyToManyField(Tag)
    isPrivate = models.BooleanField(default=False)
    slug=models.SlugField(unique=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="Date Published")


    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Workout, self).save(*args, **kwargs)


class ExInWorkout(models.Model):

    workout = models.ForeignKey(Workout,default = 1, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()

# method to work out the tags and difficulty of the workout from exercises
# uses signal to call method after an exercise is added to the workout
def get_workout_attributes(sender, instance, **kwargs):
    workout = instance.workout
    exercises = [exiw.exercise for exiw in ExInWorkout.objects.filter(workout=workout)]

    difficulty = 0.0
    for ex in exercises:
        tags = ex.tags.all()
        for tag in tags:
            workout.tags.add(tag)
        difficulty += ex.difficulty
    difficulty = difficulty/len(exercises)
    difficulty = (difficulty - 0.5) * 4 # this makes the difficulty a score out of 10, can be changed

    workout.difficulty = int(difficulty)
    workout.save()

post_save.connect(get_workout_attributes, sender=ExInWorkout)



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