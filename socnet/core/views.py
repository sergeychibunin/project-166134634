from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from core.serializers import UserSerializer, PostSerializer, PostLikeSerializer, \
    PostLikeAnalyticsSerializer
from core.models import Post, PostLike


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostLikeCreate(generics.CreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer


class PostLikeAnalyticsList(generics.ListAPIView):
    serializer_class = PostLikeAnalyticsSerializer

    def get_queryset(self):
        queryset = PostLike.objects.all()
        date_from = self.request.query_params.get('date_from', None)
        if date_from:
            queryset = queryset.filter(datetime__gte=date_from)
        date_to = self.request.query_params.get('date_to', None)
        if date_to:
            queryset = queryset.filter(datetime__lte=date_to)
        return queryset
        
