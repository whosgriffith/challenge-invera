""" User views """

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.permissions import IsAccountOwner
# Serializers
from users.serializers import UserModelSerializer, UserSignUpSerializer, UserLoginSerializer, ChangePasswordSerializer
# Models
from users.models import User


class UserViewSet(mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """ UserViewSet
    Handle sign up, login, update, retrieve and destroy.
    """

    serializer_class = UserModelSerializer
    lookup_field = 'username'
    queryset = User.objects.all()

    def get_permissions(self):
        """ Assign permissions based on action. """
        if self.action in ['signup', 'login',]:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'current', 'destroy']:
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
        username = UserModelSerializer(user).data['username']
        data = {
            'username': username,
            'access_token': token
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def current(self, request, *args, **kwargs):
        """ Returns current user username. """
        data = {"username": request.user.username}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PUT'])
    def change_password(self, request, *args, **kwargs):
        """ Change user password. """
        serializer = ChangePasswordSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            # Verify current password
            if not user.check_password(request.data.get("password")):
                return Response({"password": ["Old password is incorrect."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Change the user password    
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response(data={"detail": "Password changed."},status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
