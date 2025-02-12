from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from application_tracker.views import authentication, dashboard, platform, application_status, application, application_history
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'application_tracker'

config_platform_url = [
    path('', platform.GetAll.as_view(), name="list_platform"),
    path('/new', platform.Create.as_view(), name="create_platform"),
    path('/<id>/edit', platform.Edit.as_view(), name="edit_platform"),
    path('/<id>/delete', platform.Delete.as_view(), name="delete_platform"),
]

config_application_status_url = [
    path('', application_status.GetAll.as_view(), name="list_application_status"),
    path('/new', application_status.Create.as_view(), name="create_application_status"),
    path('/<id>/edit', application_status.Edit.as_view(), name="edit_application_status"),
    path('/<id>/delete', application_status.Delete.as_view(), name="delete_application_status"),
]

config_url = [
    path("/platform", include(config_platform_url)),
    path("/application-status", include(config_application_status_url)),
]

application_history_url = [
    path('/history/<id>', application_history.Delete.as_view(), name="delete_application_history"),
    path('/history', application_history.Create.as_view(), name="create_application_history"),
]

application_url = [
    path('', application.GetAll.as_view(), name="list_application"),
    path('/new', application.Create.as_view(), name="create_application"),
    path('/<id>/delete', application.Delete.as_view(), name="delete_application"),
    path('/<id>/edit', application.Edit.as_view(), name="edit_application"),
    path('/<id>', application.Detail.as_view(), name="detail_application"),
    path('/<application_id>', include(application_history_url)),
]

urlpatterns = [
    path('login', authentication.Login.as_view(), name="login"),
    path('register', authentication.Register.as_view(), name="register"),
    path('logout', authentication.Logout.as_view(), name="logout"),
    path('', dashboard.Home.as_view(), name='home'),
    path('config', include(config_url)),
    path('application', include(application_url))
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
