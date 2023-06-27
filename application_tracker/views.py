from django.shortcuts import render, redirect
from rest_framework import viewsets
from .serializers import UserSerializer, ApplicationSerializer, ApplicationHistorySerializer
from .models import User, Application, ApplicationHistory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from . import forms
from application_tracker.common.errors import getErrorMessageFromForm
from django.contrib.auth.decorators import login_required


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


@login_required(login_url='application_tracker:login')
def Home(request):
    return render(request, 'home.html')


def LoginPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('application_tracker:home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('application_tracker:home')
        else:
            messages.error(request, "Username or password invalid")
            return HttpResponseRedirect("/login")

    return render(request, 'authentication/login.html', context)


def RegisterPage(request):
    context = {}
    if request.method == "POST":
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("application_tracker:home")
        else:
            context['form'] = form
            messages.error(request, getErrorMessageFromForm(form))

            return HttpResponseRedirect("/register")

    else:
        form = forms.NewUserForm()
        context['form'] = form

    return render(request, "authentication/register.html", context)


def Logout(request):
    logout(request)
    return redirect("application_tracker:login")
