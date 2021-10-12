""" User views. """

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from users.permissions import IsAccountOwner
# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
# Serializers
from users.serializers import UserModelSerializer, UserSignUpSerializer, UserLoginSerializer
# Models
from users.models import User


class UserViewSet(mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """ UserViewSet
    Handle sign up, login, update, retrieve and destroy.
    """

    serializer_class = UserModelSerializer
    lookup_field = 'username'
    # Filters
    #filter_backends = (SearchFilter, OrderingFilter)
    #search_fields = ('username', 'email', 'first_name', 'last_name')
    #ordering_fields = ('first_name', 'last_name')
    queryset = User.objects.all()

    def get_permissions(self):
        """ Assign permissions based on action. """
        if self.action in ['signup', 'login',]:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', '', 'destroy']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        """ Handle User Sign up """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """ Handle User login. """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'username': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """ Override list method so it only returns current user username. """
        data = {"username": request.user.username}
        return Response(data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """ Deletes the user from the database. """
        instance.delete()