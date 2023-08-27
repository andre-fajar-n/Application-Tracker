from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from application_tracker.views import authentication, dashboard, platform

app_name = 'application_tracker'
urlpatterns = [
    path('login', authentication.Login.as_view(), name="login"),
    path('register', authentication.Register.as_view(), name="register"),
    path('logout', authentication.Logout.as_view(), name="logout"),
    path('', dashboard.Home.as_view(), name='home'),
    path('config/platform', platform.GetAll.as_view(), name="list_platform"),
    path('config/platform/new', platform.Create.as_view(), name="create_platform"),
    path('config/platform/<id>/edit', platform.Edit.as_view(), name="edit_platform"),
    path('config/platform/<id>/delete', platform.Delete.as_view(), name="delete_platform"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
