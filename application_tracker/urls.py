from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'application_tracker'
urlpatterns = [
    path('login', views.LoginPage, name="login"),
    path('', views.Index, name='index'),
    # path('logout/', views.logoutUser, name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
