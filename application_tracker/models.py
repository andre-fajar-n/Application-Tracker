from django.db import models
from django.contrib.auth.models import User

list_status = [
    ('A', 'Applied'),
    ('ST', 'Skill Test'),
    ('IH', 'Interview HR'),
    ('IU', 'Interview User'),
    ('RR', 'Rejected Resume'),
    ('RST', 'Rejected Skill Test'),
    ('RH', 'Rejected HR'),
    ('RU', 'Rejected User'),
    ('TK', 'Tidak Kukerjakan'),
    ('D', 'Dikeep'),
    ('O', 'Offering'),
]

# Create your models here.


class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    source_link = models.CharField(max_length=255)
    last_updated = models.TimeField()
    last_status = models.CharField(max_length=50, choices=list_status)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.position


class ApplicationHistory(models.Model):
    status = models.CharField(max_length=50, choices=list_status)
    note = models.TextField()
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.status
