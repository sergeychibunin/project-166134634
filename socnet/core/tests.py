import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils.timezone import now
from django.contrib import auth
from django.contrib.auth.models import User
from core.models import Post, PostLike, PostDislike


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
    
    def test_user_can_like_post(self):
        self.assertEqual(Post.objects.count() == 0, True)
        self.assertEqual(PostLike.objects.count() == 0, True)
        
        response = self.client.post(
            reverse('post'),
            {'body': 'Hello'}
        )
        response = self.client.post(reverse('post_like'), {'post_id': response.data['id']})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PostLike.objects.count() > 0, True)

    def test_user_can_dislike_post(self):
        self.assertEqual(Post.objects.count() == 0, True)
        self.assertEqual(PostDislike.objects.count() == 0, True)
        
        response = self.client.post(
            reverse('post'),
            {'body': 'Hello'}
        )
        response = self.client.post(reverse('post_dislike'), {'post_id': response.data['id']})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PostDislike.objects.count() > 0, True)

    def test_user_can_get_report(self):
        response1 = self.client.post(
            reverse('post'),
            {'body': 'Hello'}
        )
        response2 = self.client.post(
            reverse('post'),
            {'body': 'Hey'}
        )
        response11 = self.client.post(reverse('post_like'), {'post_id': response1.data['id']})
        response12 = self.client.post(reverse('post_like'), {'post_id': response1.data['id']})
        self.client.post(reverse('post_like'), {'post_id': response1.data['id']})
        self.client.post(reverse('post_like'), {'post_id': response1.data['id']})
        self.client.post(reverse('post_dislike'), {'post_id': response1.data['id']})
        self.client.post(reverse('post_like'), {'post_id': response2.data['id']})
        self.client.post(reverse('post_like'), {'post_id': response2.data['id']})
        p_likes = PostLike.objects.filter(post__id=response1.data['id'])
        p_like = p_likes[0]
        p_like.datetime = now() - datetime.timedelta(999)
        p_like.save()
        p_like = p_likes[1]
        p_like.datetime = now() + datetime.timedelta(30)
        p_like.save()
        response = self.client.get(
            reverse('post_report'),
            # {'date_from': (now() - datetime.timedelta(1)).strftime('%Y-%m-%d'),
            { 'date_to': (now() + datetime.timedelta(1)).strftime('%Y-%m-%d')}
        )
        import pdb; pdb.set_trace()
