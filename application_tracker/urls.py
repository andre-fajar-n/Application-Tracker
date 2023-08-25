from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from application_tracker.views import authentication, dashboard, platform

app_name = 'application_tracker'
urlpatterns = [
    path('login', authentication.LoginPage, name="login"),
    path('register', authentication.RegisterPage, name="register"),
    path('logout', authentication.Logout, name="logout"),
    path('', dashboard.Home, name='home'),
    path('config/platform', platform.get_all, name="list_platform"),
    path('config/platform/new', platform.create, name="create_platform"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
