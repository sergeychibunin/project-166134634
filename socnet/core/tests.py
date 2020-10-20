from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User


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
