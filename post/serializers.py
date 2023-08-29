from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Image, Like, Comment
from django.contrib.auth import get_user_model
from .utils import unique_filename
import os
import boto3

User = get_user_model()


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

    # 포스트 조회 시에만 writer 항목을 추가
    def to_representation(self, instance):
        representation = super(PostSerializer, self).to_representation(instance)
        representation['writer'] = instance.writer.email
        return representation

    def create(self, validated_data):
        post_instance = self._create_post(validated_data)
        self._validate_and_save_images(post_instance)
        return post_instance

    # 포스트 생성
    def _create_post(self, validated_data):
        writer = self.context.get('writer')
        if writer:
            validated_data['writer'] = writer
        return super().create(validated_data)

    # 이미지 저장
    def _validate_and_save_images(self, post_instance):
        images_data = self.context['request'].FILES.getlist('images')

        self._check_images_count(images_data)

        image_data_list = [
            {'post': post_instance.id, 'image': image} for image in images_data
        ]
        image_serializer = ImageSerializer(
            data=image_data_list, many=True, context=self.context
        )

        if image_serializer.is_valid():
            image_serializer.save(post=post_instance)
        else:
            raise serializers.ValidationError(image_serializer.errors)

    # 이미지 개수 검증
    def _check_images_count(self, images_data):
        if len(images_data) == 0:
            raise serializers.ValidationError(
                {'detail': 'At least 1 image should be uploaded.'}
            )
        elif len(images_data) > 10:
            raise serializers.ValidationError({'detail': 'Maximum 10 files allowed.'})


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
