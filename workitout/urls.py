from django.shortcuts import render
from django.urls import path
from workitout import views

app_name = 'workitout'

urlpatterns = [
    path('home',views.home,name='home'),
    path('create-workout',views.create_workout,name='create-workout'),
    path('search',views.search,name='search'),
    path('about',views.about,name='about'),
    path('exercises',views.exercises,name='exercises'),
    path('exercise/<slug:exercise_title_slug>/',views.show_exercise, name='show_exercise'),
    path('user/<slug:user_name>/',views.user_page,name='user-page'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('test', views.test, name='test'),
    path('must_authenticate', views.must_authenticate, name='must_authenticate'),
    ]
