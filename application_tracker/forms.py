from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Platform, ApplicationStatus

class RegisterUserForm(UserCreationForm):

    class Meta():
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PlatformForm(ModelForm):
    class Meta():
        model = Platform
        fields = ('name', )
        
class ApplicationStatusForm(ModelForm):
    class Meta():
        model = ApplicationStatus
        fields = ('name', )