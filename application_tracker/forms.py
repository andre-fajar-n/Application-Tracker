from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, URLField, CharField, DateTimeField, DateTimeInput
from .models import Platform, ApplicationStatus, Application, ApplicationHistory

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
    source_link = URLField(required=False)
    last_updated = DateTimeField(
        input_formats=['%d/%m/%Y','%d %B %Y','%d %b %Y'],
        widget=DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    class Meta():
        model = Application
        fields = ('position', 'company', 'platform', 'source_link', 'last_updated', 'last_status')

class UpdateApplicationForm(ModelForm):
    source_link = URLField(required=False)
    class Meta():
        model = Application
        fields = ('position', 'company', 'platform', 'source_link')

class CreateNewApplicationHistoryForm(ModelForm):
    note = CharField(required=False)
    update_status_at = DateTimeField(
        input_formats=['%d/%m/%Y','%d %B %Y','%d %b %Y'],
        widget=DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    class Meta():
        model = ApplicationHistory
        fields = ('status', 'note', 'update_status_at')