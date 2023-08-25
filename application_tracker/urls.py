from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from application_tracker.views import authentication, dashboard, platform

app_name = 'application_tracker'
urlpatterns = [
    path('login', authentication.login_request, name="login"),
    path('register', authentication.register, name="register"),
    path('logout', authentication.logout_request, name="logout"),
    path('', dashboard.home, name='home'),
    path('config/platform', platform.get_all, name="list_platform"),
    path('config/platform/new', platform.create, name="create_platform"),
    path('config/platform/<id>/edit', platform.Edit.as_view(), name="edit_platform"),
    path('config/platform/<id>/delete', platform.Delete.as_view(), name="delete_platform"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
