from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from core.models import Post


class SigningUpTestCase(APITestCase):
    
    def test_new_user_can_sign_up(self):
        self.assertEqual(len(User.objects.filter(username='user1')), 0)

        response = self.client.post(
            reverse('signup'),
            {'username': 'user1', 'password': 'password123'}
        )
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.filter(username='user1')), 1)
        
        response = self.client.post(
            reverse('signup'),
            {'username': 'user1', 'password': 'password123'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginingTestCase(APITestCase):

    def test_user_can_log_in(self):
        credentials = {'username': 'user1', 'password': 'password123'}
        self.client.post(reverse('signup'), credentials)
        response = self.client.post(
            reverse('token_obtain_pair'),
            credentials
        )
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('access' in response.data, True)
        self.assertEqual(len(response.data['access']) > 0, True)


class UserActivityTestCase(APITestCase):

    def setUp(self):
        credentials = {'username': 'user1', 'password': 'password123'}
        self.client.post(reverse('signup'), credentials)
        response = self.client.post(
            reverse('token_obtain_pair'),
            credentials
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_user_can_create_post(self):
        self.assertEqual(Post.objects.count() == 0, True)
        
        response = self.client.post(
            reverse('post'),
            {'body': 'Hello'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count() == 1, True)
