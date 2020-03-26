from django.contrib import admin
from django.urls import path,include
from workitout import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('workitout/', include('workitout.urls')),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
