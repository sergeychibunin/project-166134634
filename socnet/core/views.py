from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from core.serializers import UserSerializer, PostSerializer, PostLikeSerializer, \
    PostDislikeSerializer, PostLikeAnalyticsSerializer
from core.models import Post, PostLike, PostDislike


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


class PostDislikeCreate(generics.CreateAPIView):
    queryset = PostDislike.objects.all()
    serializer_class = PostDislikeSerializer


class PostLikeAnalyticsList(APIView):

    def get(self, request):
        likes_queryset = PostLike.objects.order_by('datetime').all()
        dislikes_queryset = PostDislike.objects.order_by('datetime').all()
        # select date(datetime), post_id, sum(case when like_type = 1 then 1 else 0 end) likes, sum(case when like_type = 0 then 1 else 0 end) dislikes from core_postlike group by datetime, post_id order by datetime;
        
        date_from = self.request.query_params.get('date_from', None)
        if date_from:
            likes_queryset = likes_queryset.filter(datetime__gte=date_from)
            dislikes_queryset = dislikes_queryset.filter(datetime__gte=date_from)
        
        date_to = self.request.query_params.get('date_to', None)
        if date_to:
            likes_queryset = likes_queryset.filter(datetime__lte=date_to)
            dislikes_queryset = dislikes_queryset.filter(datetime__lte=date_to)
        
        # date, post_id, likes, dislikes
        dates = []
        for like in likes_queryset:
            dates.append(like.datetime.date())
        for dislikes in dislikes_queryset:
            dates.append(dislikes.datetime.date())
        dates = set(dates)
        rows = []
        for d in dates:
            likes = likes_queryset.filter(datetime__date=d).values('post').annotate(total=Count('id'))
            import pdb; pdb.set_trace()
        return rows
