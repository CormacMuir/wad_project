from django.contrib import admin
from django.urls import path,include,reverse
from workitout import views
from django.conf.urls.static import static
from django.conf import settings
from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self,user):
        return reverse('workitout:register_profile')



urlpatterns = [
    path('', views.home, name='home'),
    path('workitout/', include('workitout.urls')),
    path('accounts/register/',MyRegistrationView.as_view(),name='registration_register'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
