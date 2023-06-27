# profile_page/urls.py
from django.urls import path

from application_tracker.views import index


urlpatterns = [
    path('', index),
]
