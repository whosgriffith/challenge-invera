# Django
from django.test import TestCase

# Python
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
from users.models import User
from tasks.models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        user = User(
            username='testing_login'
        )
        user.set_password('admin123')
        user.save()

        client = APIClient()
        response = client.post(
                '/users/login/', {
                'username': 'testing_login',
                'password': 'admin123',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user


    def test_create_task(self):
        """Test user signup"""

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        test_task = {
            'title': 'Comprar notebook',
        }

        response = client.post(
            '/tasks/', 
            test_task,
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', result)
        self.assertIn('title', result)
        self.assertIn('is_completed', result)
        self.assertIn('date', result)

    
    def test_update_task(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        task = Task.objects.create(
            user=self.user,
            title='Terminar challenge',
            is_completed=False,
            date='02-03-2050'
        )

        test_task_update = {
            'title': 'Comprar silla',
        }

        response = client.put(
            f'/tasks/{task.pk}/', 
            test_task_update,
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'pk' in result:
            del result['pk']

        self.assertEqual(result, test_task_update)

    
    def test_delete_task(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        task = Task.objects.create(
            user=self.user,
            title='Terminar',
            is_completed=False,
            date='02-03-2050'
        )

        response = client.delete(
            f'/tasks/{task.pk}/', 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        task_exists = Task.objects.filter(pk=task.pk)
        self.assertFalse(task_exists)