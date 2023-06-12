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
from . import forms

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


def Home(request):
    return render(request, 'home.html')


def LoginPage(request):
    if request.user.is_authenticated:
        data = {
            'test': 'ini testing',
        }
        return redirect('application_tracker:home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('application_tracker:home')

        messages.info(request, 'username or password is incorrect')

    context = {}
    return render(request, 'authentication/login.html', context)


def RegisterPage(request):
    print("CEK DISINI 1", request.method)
    if request.method == "POST":
        form = forms.NewUserForm(request.POST)
        print("CEK DISINI 2", form.is_valid())
        if form.is_valid():
            print("CEK DISINI 3")
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("application_tracker:home")

        print("CEK DISINI 4")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")

    print("CEK DISINI 5")
    form = forms.NewUserForm()
    return render(request, "authentication/register.html", context={"register_form": form})
