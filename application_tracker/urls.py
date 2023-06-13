from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'application_tracker'
urlpatterns = [
    path('login', views.LoginPage, name="login"),
    path('register', views.RegisterPage, name="register"),
    path('logout', views.Logout, name="logout"),
    path('home', views.Home, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
