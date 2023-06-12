from rest_framework import serializers
from .models import User
from .models import Application
from .models import ApplicationHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'created_at', 'updated_at', 'deleted_at')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('position', 'company', 'platform', 'source_link', 'last_updated',
                  'last_status', 'created_at', 'updated_at', 'deleted_at')


class ApplicationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationHistory
        fields = ('position', 'company', 'platform', 'source_link', 'last_updated',
                  'last_status', 'created_at', 'updated_at', 'deleted_at')
