""" Tasks URLs """

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter
# Views
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'tasks', UserViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls))
]