""" Tasks URLs """

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter
# Views
from tasks.views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls))
]