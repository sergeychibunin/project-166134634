from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField('The body of a post')


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_type = models.BooleanField('Like is the true value')
    datetime = models.DateTimeField('The date of a like', auto_now_add=True)
