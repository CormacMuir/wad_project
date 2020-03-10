from django.contrib import admin
from django.urls import path,include
from workitout import views

app_name = 'workitout'

urlpatterns = [
    path('', views.home, name='home'),
    path('create-workout',views.create-workout,name='create-workout'),
    path('search',views.search,name='search'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('user/<slug:user_id_slug>/',views.user-page,name='user-page'),
]
