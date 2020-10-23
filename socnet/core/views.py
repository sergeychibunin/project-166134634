from datetime import datetime
from itertools import zip_longest
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from django.utils.timezone import make_aware
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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
        likes_queryset = PostLike.objects.order_by('datetime__date', 'post').all()
        dislikes_queryset = PostDislike.objects.order_by('datetime__date', 'post').all()
        
        date_from = self.request.query_params.get('date_from', None)
        if date_from:
            likes_queryset = likes_queryset.filter(datetime__gte=date_from)
            dislikes_queryset = dislikes_queryset.filter(datetime__gte=date_from)
        
        date_to = self.request.query_params.get('date_to', None)
        if date_to:
            date_to = make_aware(datetime.strptime(date_to, '%Y-%m-%d'))  # TODO check
            likes_queryset = likes_queryset.filter(datetime__lte=date_to)
            dislikes_queryset = dislikes_queryset.filter(datetime__lte=date_to)
        
        dates = []
        for like in likes_queryset:
            dates.append(like.datetime.date())
        for dislikes in dislikes_queryset:
            dates.append(dislikes.datetime.date())
        dates = set(dates)
        
        rows = []
        for d in dates:
            likes = likes_queryset.filter(datetime__date=d).values('datetime__date', 'post').annotate(total=Count('id'))
            dislikes = dislikes_queryset.filter(datetime__date=d).values('datetime__date', 'post').annotate(total=Count('id'))
            for p_likes, p_dislikes in zip_longest(likes, dislikes):
                row = {'date': d}
                if p_likes:
                    row['post_id'] = p_likes['post']
                    row['likes'] = p_likes['total']
                else:
                    row['post_id'] = p_dislikes['post']
                if p_dislikes:
                    if p_likes and p_likes['post'] == p_dislikes['post']:
                        row['dislikes'] = p_dislikes['total']
                        rows.append(row)
                        continue
                    elif p_likes:
                        row['dislikes'] = 0
                        rows.append(row)
                        row = {'date': d, 'post_id': p_dislikes['post'], 'likes': 0, 'dislikes': p_dislikes['total']}
                        rows.append(row)
                        continue
                    else:
                        row['likes'] = 0
                        row['dislikes'] = p_dislikes['total']
                        rows.append(row)
                else:
                    row['dislikes'] = 0
                    rows.append(row)

        serializer = PostLikeAnalyticsSerializer(data=rows, many=True)
        assert serializer.is_valid()
        return Response(serializer.data)
