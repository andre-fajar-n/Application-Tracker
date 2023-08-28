from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint

class Platform(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user_id', 'name'], name="unique_platform")
        ]
    
    def __str__(self):
        return self.name

class ApplicationStatus(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user_id', 'name'], name="unique_application_status")
        ]
    
    def __str__(self):
        return self.name

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    platform = models.ForeignKey(Platform, on_delete=models.RESTRICT)
    source_link = models.CharField(max_length=255)
    last_updated = models.DateField()
    last_status = models.ForeignKey(
        ApplicationStatus, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.position


class ApplicationHistory(models.Model):
    status = models.ForeignKey(ApplicationStatus, on_delete=models.RESTRICT)
    note = models.TextField()
    application = models.ForeignKey(Application, on_delete=models.RESTRICT)
    update_status_at = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status
