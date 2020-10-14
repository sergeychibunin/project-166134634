from django.contrib.auth.models import User
from core.models import Post, PostLike
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('body', 'id')
    
    def create(self, validated_data):
        post = Post(**validated_data)
        post.user = \
            self.context['request'].user
        post.save()
        return post


class PostLikeSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id')

    class Meta:
        model = PostLike
        fields = ('post_id', 'like_type')

    def create(self, validated_data):
        post = Post.objects.get(pk=validated_data['post']['id'])
        like = PostLike(post=post, like_type=validated_data['like_type'])
        like.save()
        return like


class PostLikeAnalyticsSerializer(serializers.ModelSerializer):
    # date, post_id, likes, dislikes
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    class Meta:
        model = PostLike
        field = ('date_from', 'date_to')
