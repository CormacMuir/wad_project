from django import forms
from workitout.models import Workout, Exercise, ExInWorkout, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'picture','isPrivate')


class CreateWorkoutForm(forms.ModelForm):

    # user input
    title           = forms.CharField(max_length=128, help_text="Please enter the workout title.") 
    description     = forms.CharField(max_length=5000, help_text="Please enter a description.") 
    isPrivate       = forms.BooleanField(required=False, help_text="Do you want to make the workout private")

    # hidden fields 
    duration        = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes           = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug            = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Workout
        fields = ['title', 'description', 'isPrivate']


class AddExerciseForm(forms.ModelForm):

    exercise_list = Exercise.objects.order_by('title')  

    # user input
    exercise        = forms.ModelChoiceField(queryset=exercise_list, help_text="Please select an exercise to add to your workout.")
    sets            = forms.IntegerField(min_value=0, help_text="Sets")
    reps            = forms.IntegerField(min_value=0, help_text="Reps")


    class Meta:
        model = ExInWorkout
        
        fields = ['exercise','sets', 'reps']



class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields=(
            'email',

        )

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields = ('bio','picture','isPrivate')


