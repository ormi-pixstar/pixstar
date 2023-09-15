from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Image, Like, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'post', 'image_url']

    def create(self, validated_data):
        images = self.context['request'].FILES.getlist('images')

        return validated_data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'created_at',
            'updated_at',
            'images',
            'likes',
        ]

    # 포스트 조회 시에만 writer 항목을 추가
    def to_representation(self, instance):
        representation = super(PostSerializer, self).to_representation(instance)
        representation['writer'] = instance.writer.email
        return representation

    def create(self, validated_data):
        post_instance = self._create_post(validated_data)
        return post_instance


class UserPostSerializer(serializers.ModelSerializer):
    written_posts = PostSerializer(source='post_set', many=True, read_only=True)
    liked_posts = LikeSerializer(source='like_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'written_posts',
            'liked_posts',
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
