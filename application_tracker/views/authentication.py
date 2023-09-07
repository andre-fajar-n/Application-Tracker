from application_tracker import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from application_tracker.common.errors import getErrorMessageFromForm
from django.views import View

class Login(View):
    context = {}
    def is_authenticated(self, request):
        if request.user.is_authenticated:
            return redirect('application_tracker:home')
    
    def get(self, request):
        self.is_authenticated(request)
        return render(request, 'page/authentication/login.html', self.context)
    
    def post(self, request):
        self.is_authenticated(request)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('application_tracker:home')
        else:
            messages.error(request, "Username or password invalid")
            return HttpResponseRedirect("/login")

class Register(View):
    context = {}

    def get(self, request):
        form = forms.RegisterUserForm()
        self.context['form'] = form
        return render(request, "page/authentication/register.html", self.context)
    
    def post(self, request):
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("application_tracker:home")
        else:
            self.context['form'] = form
            messages.error(request, getErrorMessageFromForm(form))

            return HttpResponseRedirect("/register")

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("application_tracker:login")
