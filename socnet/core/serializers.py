from django.contrib.auth.models import User
from core.models import Post, PostLike, PostDislike
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
        fields = ('post_id',)

    def create(self, validated_data):
        post = Post.objects.get(pk=validated_data['post']['id'])
        like = PostLike(post=post)
        like.save()
        return like


class PostDislikeSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id')

    class Meta:
        model = PostDislike
        fields = ('post_id',)
    
    def create(self, validated_data):
        post = Post.objects.get(pk=validated_data['post']['id'])
        dislike = PostDislike(post=post)
        dislike.save()
        return dislike


class PostLikeAnalyticsSerializer(serializers.Serializer):
    date = serializers.DateField()
    post_id = serializers.IntegerField()
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()


class UserActivitySerializer(serializers.Serializer):
    last_login = serializers.DateTimeField()
    last_request = serializers.DateTimeField()
