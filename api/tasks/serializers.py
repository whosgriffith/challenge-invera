"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import authenticate
# Django REST Framework
from rest_framework import serializers
# Models
from tasks.models import Task


class TaskModelSerializer(serializers.ModelSerializer):

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        """ Meta class. """
        model = Task
        fields = ('user', 'title', 'is_completed', 'date')


class TaskUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        """ Meta class. """
        model = Task
        fields = ('title',)