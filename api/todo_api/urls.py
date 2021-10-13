"""todo_api URL Configuration"""

# Django
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('tasks.urls', 'tasks'), namespace='tasks')),
]
