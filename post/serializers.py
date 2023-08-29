from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Image, Like, Comment
from django.contrib.auth import get_user_model
import os
import boto3
import uuid

User = get_user_model()


# 파일명이 중복되는 경우를 방지
def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return f'images/{new_filename}'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'post', 'image_url']

    def create(self, validated_data):
        images = self.context['request'].FILES.getlist('images')

        if not images or len(images) == 0:
            return Response(
                {'detail': 'No files for upload.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(images) > 10:
            return Response(
                {'detail': 'Maximum 10 files allowed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        image_urls = []
        for image in images:
            try:
                # S3에 이미지 업로드
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                )
                file_name = unique_filename(image.name)
                bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
                s3.upload_fileobj(
                    image, bucket_name, file_name, ExtraArgs={'ACL': 'public-read'}
                )
                # S3 URL 생성
                image_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
                image_urls.append(image_url)
            except Exception as e:
                return Response(
                    {'detail': f'Image upload failed: {e}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # DB에 이미지 URL 저장
        for url in image_urls:
            Image.objects.create(post=validated_data['post'], image_url=url)

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

    def to_representation(self, instance):
        representation = super(PostSerializer, self).to_representation(instance)
        representation['writer'] = instance.writer.email
        return representation

    def create(self, validated_data):
        writer = self.context.get('writer', None)
        if writer:
            self.validated_data['writer'] = writer
        return super(PostSerializer, self).create(validated_data)


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
