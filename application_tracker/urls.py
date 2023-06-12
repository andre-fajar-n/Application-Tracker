from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'application_tracker'
urlpatterns = [
    path('login', views.LoginPage, name="login"),
    path('home', views.Home, name='home'),
    path('register', views.RegisterPage, name="register"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
