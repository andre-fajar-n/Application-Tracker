from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .serializers import UserSerializer
from .serializers import ApplicationSerializer
from .serializers import ApplicationHistorySerializer
from .models import User
from .models import Application
from .models import ApplicationHistory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ApplicationView(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()


class ApplicationHistoryView(viewsets.ModelViewSet):
    serializer_class = ApplicationHistorySerializer
    queryset = ApplicationHistory.objects.all()


def Index(request):
    return render(request, 'index.html')


def LoginPage(request):
    if request.user.is_authenticated:
        data = {
            'test': 'ini testing',
        }
        return redirect('application_tracker:index', data)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('application_tracker:index')

        messages.info(request, 'username or password is incorrect')

    context = {}
    return render(request, 'authentication/login.html', context)
