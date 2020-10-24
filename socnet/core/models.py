from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField('The body of a post')


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    datetime = models.DateTimeField('The date of a like', auto_now_add=True)


class PostDislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    datetime = models.DateTimeField('The date of a dislike', auto_now_add=True)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_request = models.DateTimeField('The date of the last request of a user')
