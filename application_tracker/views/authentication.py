from application_tracker import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from application_tracker.common.errors import getErrorMessageFromForm


def login_request(request):
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


def register(request):
    context = {}
    if request.method == "POST":
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("application_tracker:home")
        else:
            context['form'] = form
            messages.error(request, getErrorMessageFromForm(form))

            return HttpResponseRedirect("/register")

    else:
        form = forms.RegisterUserForm()
        context['form'] = form

    return render(request, "authentication/register.html", context)


def logout_request(request):
    logout(request)
    return redirect("application_tracker:login")