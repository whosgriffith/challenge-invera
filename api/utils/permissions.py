""" Custom permissions. """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    """ Give permission only to user who created the photo. """

    def has_object_permission(self, request, view, obj):
        """ Check user and obj are the same. """
        return request.user == obj.user


class IsAccountOwner(BasePermission):
    """ Give permission only if is the account owner. """

    def has_object_permission(self, request, view, obj):
        return request.user == obj