""" Users models. """

# Django
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ''' Custom User. 
    Created a empty custom user for possible future updates.
    '''
