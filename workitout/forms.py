from django import forms
from workitout.models import Workout, Exercise, ExInWorkout, UserProfile
from django.contrib.auth.models import User


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





