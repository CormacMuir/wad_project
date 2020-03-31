from django.shortcuts import render
from django.urls import path
from workitout import views
from workitout.views import LikeWorkoutView,FollowUserView,SaveWorkoutView
app_name = 'workitout'

urlpatterns = [
    path('home',views.home,name='home'),
    path('create-workout',views.create_workout,name='create-workout'),
    path('search',views.search,name='search'),
    path('about',views.about,name='about'),
    path('exercises',views.exercises,name='exercises'),
    path('exercise/<slug:exercise_title_slug>/',views.exercise_page, name='exercise_page'),
    path('workout/<creator>/<workout_id>/',views.workout_page, name='workout_page'),
    path('like_workout/', views.LikeWorkoutView.as_view(), name='like_workout'),
    path('follow_user/', views.FollowUserView.as_view(), name='follow_user'),
    path('save_workout/', views.SaveWorkoutView.as_view(), name='save_workout'),
    path('user/<user_name>/',views.user_page,name='user_page'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('must_authenticate', views.must_authenticate, name='must_authenticate'),
    path('edit-profile',views.edit_profile, name = "edit_profile")
    ]
