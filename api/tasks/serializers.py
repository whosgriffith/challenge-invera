"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import authenticate
# Django REST Framework
from rest_framework import serializers
# Models
from tasks.models import Task
# Utilities
from django.utils import timezone


class TaskModelSerializer(serializers.ModelSerializer):

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        """ Meta class. """
        model = Task
        fields = ('pk', 'user', 'title', 'is_completed', 'date', 'limit_date')

    def validate_limit_date(self, data):
        """Verify date is not in the past."""
        current_date = timezone.now()
        if data < current_date.date():
            raise serializers.ValidationError(
                "Limit date can't be in the past."
            )
        return data


class TaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        """ Meta class. """
        model = Task
        fields = ('title',)