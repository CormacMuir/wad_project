from django.shortcuts import render
from django.urls import path
from workitout import views

app_name = 'workitout'

urlpatterns = [
    path('home',views.home,name='home'),
    path('create-workout',views.create_workout,name='create-workout'),
    path('search',views.search,name='search'),
    path('about',views.search,name='about'),
    path('user/<slug:user_id_slug>/',views.user_page,name='user-page'),]