from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, URLField
from .models import Platform, ApplicationStatus, Application

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

class CreateApplicationForm(ModelForm):
    source_link = URLField()
    class Meta():
        model = Application
        fields = ('position', 'company', 'platform', 'source_link', 'last_updated', 'last_status')

class UpdateApplicationForm(ModelForm):
    source_link = URLField()
    class Meta():
        model = Application
        fields = ('position', 'company', 'platform', 'source_link')