""" Tasks views """

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
# Permissions
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsObjectOwner
# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
# Serializers
from tasks.serializers import TaskModelSerializer, TaskUpdateSerializer
from tasks.models import Task


class TaskViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """ TaskViewSet
    Handle create, completion ,update, retrieve and destroy.
    """
    
    # Filters
    # Filter by title, date, and completed status. 
    # Using search, is_completed and ordering params.
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('title', 'date', 'limit_date')
    ordering_fields = ('is_completed', 'date', 'limit_date')
    ordering = ('is_completed', 'limit_date')
    filter_fields = ('is_completed', 'limit_date')

    def get_queryset(self):
        """
        Sets the queryset so it returns only the current user tasks.
        """
        user = self.request.user
        return Task.objects.filter(user=user)

    def get_serializer_class(self):
        """
        Change the serializer for updating only the title of a task.
        """
        if self.action == 'update':
            return TaskUpdateSerializer
        return TaskModelSerializer

    def get_permissions(self):
        """ Assign permissions based on action. """
        if self.action in ['retrieve', 'update', 'list', 'destroy']:
            permissions = [IsAuthenticated, IsObjectOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=True, methods=['POST'])
    def complete(self, request, *args, **kwargs):
        """ Mark a task as completed. """
        task = self.get_object()
        task.is_completed = True
        task.save()
        data = TaskModelSerializer(task).data
        return Response(data=data, status=status.HTTP_200_OK)
        