# Django
from django.test import TestCase

# Python
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
from users.models import User


class UserTestCase(TestCase):
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


    def test_signup_user(self):
        """Test user signup"""

        client = APIClient()
        response = client.post(
                '/users/signup/', {
                'username': 'test_signup',
                'password': 'rc{4@qHjR>!b`yAV',
                'password_confirmation': 'rc{4@qHjR>!b`yAV',
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {"username":"test_signup"})

    
    def test_login_user(self):

        client = APIClient()
        response = client.post(
                '/users/login/', {
                'username': 'testing_login',
                'password': 'admin123',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        result = json.loads(response.content)
        self.assertIn('access_token', result)


    def test_update_user(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        response = client.get(
                f'/users/{self.user.pk}/', {
                'username': 'testing_update',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(json.loads(response.content), {"username":"testing_update"})


    def test_update_user(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        response = client.put(
            f'/users/{self.user.pk}/', 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(json.loads(response.content), {"username":"testing_update"})


    def test_delete_user(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        response = client.delete(
            f'/education/{self.user.pk}/', 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user_exists = User.objects.filter(pk=self.user.pk)
        self.assertFalse(user_exists)
