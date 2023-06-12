from django.contrib import admin
from .models import Application
from .models import ApplicationHistory


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'last_status', 'last_updated')


class ApplicationHistoryAdmin(admin.ModelAdmin):
    list_display = ('status', 'created_at')


# Register your models here.
admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationHistory, ApplicationHistoryAdmin)
