"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import authenticate
# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
# Models
from users.models import User


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        """ Meta class. """

        model = User
        fields = ('username',)


class UserSignUpSerializer(serializers.Serializer):
    """ Serializer for User sign up.
    Handle sign up data validation and user creation.
    """

    username = serializers.CharField(
        min_length=3,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Password
    password = serializers.CharField(min_length=5, max_length=64)
    password_confirmation = serializers.CharField(min_length=5, max_length=64)

    def create(self, data):
        """Handle user creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """ Serializer for User login.
    Handle the login request.
    """

    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=64)

    def validate(self, data):
        """ Validate login credentials. """
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Incorrect credentials.')

        self.context['user'] = user
        return data

    def create(self, data):
        """ Generate/retrieve token. """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key