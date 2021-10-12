""" Custom permissions. """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """ Give permission only if is the account owner. """

    def has_object_permission(self, request, view, obj):
        return request.user == obj