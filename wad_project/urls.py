from django.contrib import admin
from django.urls import path,include
from workitout import views

urlpatterns = [
    path('', views.home, name='home'),
    path('workitout/', include('workitout.urls')),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls)
]
